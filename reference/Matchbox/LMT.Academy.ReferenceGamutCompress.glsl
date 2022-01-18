  
// <ACEStransformID>urn:ampas:aces:transformId:v1.5:LMT.Academy.ReferenceGamutCompress.a1.v1.0</ACEStransformID>
// <ACESuserName>ACES 1.3 Look - Reference Gamut Compress</ACESuserName>

//
// Gamut compression algorithm to bring out-of-gamut scene-referred values into AP1
//

uniform sampler2D frontTex, matteTex, selectiveTex;
uniform float adsk_result_w, adsk_result_h;
uniform int direction;
uniform int inout_colorspace;

// --- Gamut Compress Parameters --- 
// Distance from achromatic which will be compressed to the gamut boundary
// Values calculated to encompass the encoding gamuts of common digital cinema cameras
const float LIM_CYAN =  1.147;
const float LIM_MAGENTA = 1.264;
const float LIM_YELLOW = 1.312;

// Percentage of the core gamut to protect
// Values calculated to protect all the colors of the ColorChecker Classic 24 as given by
// ISO 17321-1 and Ohta (1997)
const float THR_CYAN = 0.815;
const float THR_MAGENTA = 0.803;
const float THR_YELLOW = 0.880;

// Aggressiveness of the compression curve
const float PWR = 1.2;

// ACES primaries conversion matrices
const mat3 AP0_to_AP1 = mat3(
   1.4514393161, -0.0765537734,  0.0083161484,
  -0.2365107469,  1.1762296998, -0.0060324498,
  -0.2149285693, -0.0996759264,  0.9977163014
);

const mat3 AP1_to_AP0 = mat3(
   0.6954522414,  0.0447945634, -0.0055258826,
   0.1406786965,  0.8596711185,  0.0040252103,
   0.1638690622,  0.0955343182,  1.0015006723
);

// convert acescg to acescct
float lin_to_acescct(float val) {
  if (val <= 0.0078125) {
    return 10.5402377416545 * val + 0.0729055341958355;
  } else {
    return (log2(val) + 9.72) / 17.52;
  }
}

// convert acescct to acescg
float acescct_to_lin(float val) {
  if (val > 0.155251141552511) {
    return pow( 2.0, val*17.52 - 9.72);
  } else {
    return (val - 0.0729055341958355) / 10.5402377416545;
  }
}


// calculate compressed distance
float compress(float dist, float lim, float thr, bool invert, float pwr) {
  float comprDist, scl, nd, p;

  if (dist < thr) {
    comprDist = dist; // No compression below threshold
  }
  else {
    // Calculate scale factor for y = 1 intersect
    scl = (lim - thr) / pow(pow((1.0 - thr) / (lim - thr), -pwr) - 1.0, 1.0 / pwr);

    // Normalize distance outside threshold by scale factor
    nd = (dist - thr) / scl;
    p = pow(nd, pwr);

    if (!invert) {
      comprDist = thr + scl * nd / (pow(1.0 + p, 1.0 / pwr)); // Compress
    }
    else {
      if (dist > (thr + scl)) {
        comprDist = dist; // Avoid singularity
      }
      else {
        comprDist = thr + scl * pow(-(p / (p - 1.0)), 1.0 / pwr); // Uncompress
      }
    }
  }

  return comprDist;
}

void main() {
  vec3 thr;
  thr = vec3(THR_CYAN, THR_MAGENTA, THR_YELLOW);

  vec3 lim;
  lim = vec3(LIM_CYAN, LIM_MAGENTA, LIM_YELLOW);

  // source pixels
  vec2 coords = gl_FragCoord.xy / vec2( adsk_result_w, adsk_result_h );
  vec3 rgb = texture2D(frontTex, coords).rgb;
  float alpha = texture2D(matteTex, coords).g;
  float select = texture2D(selectiveTex, coords).g;

  if (inout_colorspace == 1) {
    rgb.x = acescct_to_lin(rgb.x);
    rgb.y = acescct_to_lin(rgb.y);
    rgb.z = acescct_to_lin(rgb.z);
  }

  if (inout_colorspace == 2) {
    rgb = AP0_to_AP1 * rgb;
  }

  // achromatic axis 
  float ach = max(rgb.x, max(rgb.y, rgb.z));

  // distance from the achromatic axis for each color component aka inverse rgb ratios
  vec3 dist;
  dist.x = ach == 0.0 ? 0.0 : (ach - rgb.x) / abs(ach);
  dist.y = ach == 0.0 ? 0.0 : (ach - rgb.y) / abs(ach);
  dist.z = ach == 0.0 ? 0.0 : (ach - rgb.z) / abs(ach);

  // compress distance with parameterized shaper function
  float sat;
  vec3 csat, comprDist;
  comprDist = vec3(
    compress(dist.x, lim.x, thr.x, (direction == 1), PWR),
    compress(dist.y, lim.y, thr.y, (direction == 1), PWR),
    compress(dist.z, lim.z, thr.z, (direction == 1), PWR));

  // recalculate rgb from compressed distance and achromatic
  vec3 crgb = vec3(
    ach - comprDist.x * abs(ach),
    ach - comprDist.y * abs(ach),
    ach - comprDist.z * abs(ach));

  if (inout_colorspace == 1) {
    crgb.x = lin_to_acescct(crgb.x);
    crgb.y = lin_to_acescct(crgb.y);
    crgb.z = lin_to_acescct(crgb.z);
  }

  if (inout_colorspace == 2) {
    crgb = AP1_to_AP0 * crgb;
  }

  crgb = mix(rgb, crgb, select);

  gl_FragColor = vec4(crgb, alpha);
}
