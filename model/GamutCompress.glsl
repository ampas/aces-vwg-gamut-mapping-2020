uniform sampler2D frontTex, matteTex, selectiveTex;
uniform float power, cyan, magenta, yellow, adsk_result_w, adsk_result_h;
uniform int working_colorspace;
uniform bool invert, overlay;
uniform vec3 threshold;

// Convert acescg to acescct
float lin_to_acescct(float val) {
  if (val <= 0.0078125) {
    return 10.5402377416545 * val + 0.0729055341958355;
  } else {
    return (log2(val) + 9.72) / 17.52;
  }
}

// Convert acescct to acescg
float acescct_to_lin(float val) {
  if (val > 0.155251141552511) {
    return pow( 2.0, val*17.52 - 9.72);
  } else {
    return (val - 0.0729055341958355) / 10.5402377416545;
  }
}

// Convert acescg to acescc
float lin_to_acescc(float val) {
  if (val <= 0.0) {
    return -0.3584474886; // =(log2( pow(2.,-16.))+9.72)/17.52
  } else if (val < pow(2.0, -15.0)) {
    return (log2(pow(2.0, -16.0)+val*0.5)+9.72)/17.52;
  } else { // (val >= pow(2.,-15))
    return (log2(val)+9.72)/17.52;
  }
}

// Convert acescc to acescg
float acescc_to_lin(float val) {
  if (val < -0.3013698630) { // (9.72-15)/17.52
    return (pow(2.0, val*17.52-9.72) - pow(2.0, -16.0))*2.0;
  } else if (val < (log2(65504.0)+9.72)/17.52) {
    return pow(2.0, val*17.52-9.72);
  } else { // (val >= (log2(HALF_MAX)+9.72)/17.52)
    return 65504.0;
  }
}

// calculate compressed distance
float compress(float dist, float lim, float thr, bool invert, float power) {
  float cdist, s;
  if (dist < thr) {
    cdist = dist;
  } else {
    // power(p) compression function plot https://www.desmos.com/calculator/54aytu7hek
    if (lim < 1.0001) {
      return dist; // disable compression, avoid nan
    }
    s = (lim-thr)/pow(pow((1.0-thr)/(lim-thr),-power)-1.0,1.0/power); // calc y=1 intersect
    if (!invert) {
      cdist = thr+s*((dist-thr)/s)/(pow(1.0+pow((dist-thr)/s,power),1.0/power)); // compress
    } else {
      if (dist > (thr + s)) {
        cdist = dist; // avoid singularity
      } else {
        cdist = thr+s*pow(-(pow((dist-thr)/s,power)/(pow((dist-thr)/s,power)-1.0)),1.0/power); // uncompress
      }
    }
  }
  return cdist;
}

void main() {
  vec2 coords = gl_FragCoord.xy / vec2( adsk_result_w, adsk_result_h );
  // source pixels
  vec3 rgb = texture2D(frontTex, coords).rgb;
  float alpha = texture2D(matteTex, coords).g;
  float select = texture2D(selectiveTex, coords).g;

  if (working_colorspace == 1) {
    rgb.x = acescct_to_lin(rgb.x);
    rgb.y = acescct_to_lin(rgb.y);
    rgb.z = acescct_to_lin(rgb.z);
  } else if (working_colorspace == 2) {
    rgb.x = acescc_to_lin(rgb.x);
    rgb.y = acescc_to_lin(rgb.y);
    rgb.z = acescc_to_lin(rgb.z);
  } 

  // thr is the percentage of the core gamut to protect.
  vec3 thr = vec3(
    min(0.9999, threshold.x),
    min(0.9999, threshold.y),
    min(0.9999, threshold.z));

  // lim is the max distance from the gamut boundary that will be compressed
  // 0 is a no-op, 1 will compress colors from a distance of 2.0 from achromatic to the gamut boundary
  vec3 lim;
  lim = vec3(cyan+1.0, magenta+1.0, yellow+1.0);

  // achromatic axis 
  float ach = max(rgb.x, max(rgb.y, rgb.z));

  // distance from the achromatic axis for each color component aka inverse rgb ratios
  vec3 dist;
  dist.x = ach == 0.0 ? 0.0 : (ach-rgb.x)/abs(ach);
  dist.y = ach == 0.0 ? 0.0 : (ach-rgb.y)/abs(ach);
  dist.z = ach == 0.0 ? 0.0 : (ach-rgb.z)/abs(ach);

  // compress distance with user controlled parameterized shaper function
  float sat;
  vec3 csat, cdist;
  cdist = vec3(
    compress(dist.x, lim.x, thr.x, invert, power),
    compress(dist.y, lim.y, thr.y, invert, power),
    compress(dist.z, lim.z, thr.z, invert, power));

  // recalculate rgb from compressed distance and achromatic
  // effectively this scales each color component relative to achromatic axis by the compressed distance
  vec3 crgb = vec3(
    ach-cdist.x*abs(ach),
    ach-cdist.y*abs(ach),
    ach-cdist.z*abs(ach));

  // Graph overlay method based on one by Paul Dore
  // https://github.com/baldavenger/DCTLs/tree/master/ACES%20TOOLS
  if (overlay) {
    vec3 cramp = vec3(
      compress(2.0 * coords.x, lim.x, thr.x, invert, power),
      compress(2.0 * coords.x, lim.y, thr.y, invert, power),
      compress(2.0 * coords.x, lim.z, thr.z, invert, power));
    bool overlay_r = abs(2.0 * coords.y - cramp.x) < 0.004 || abs(coords.y - 0.5) < 0.0005 ? true : false;
    bool overlay_g = abs(2.0 * coords.y - cramp.y) < 0.004 || abs(coords.y - 0.5) < 0.0005 ? true : false;
    bool overlay_b = abs(2.0 * coords.y - cramp.z) < 0.004 || abs(coords.y - 0.5) < 0.0005 ? true : false;
    crgb.x = overlay_g || overlay_b ? 1.0 : crgb.x;
    crgb.y = overlay_b || overlay_r ? 1.0 : crgb.y;
    crgb.z = overlay_r || overlay_g ? 1.0 : crgb.z;
  }

  if (working_colorspace == 1) {
    crgb.x = lin_to_acescct(crgb.x);
    crgb.y = lin_to_acescct(crgb.y);
    crgb.z = lin_to_acescct(crgb.z);
  } else if (working_colorspace == 2) {
    crgb.x = lin_to_acescc(crgb.x);
    crgb.y = lin_to_acescc(crgb.y);
    crgb.z = lin_to_acescc(crgb.z);
  }

  crgb = mix(rgb, crgb, select);

  gl_FragColor = vec4(crgb, alpha);
}
