
// <ACEStransformID>urn:ampas:aces:transformId:v1.5:LMT.VWG.GamutCompress.a1.v1</ACEStransformID>
// <ACESuserName>ACES 1.3 Look - Gamut Compress</ACESuserName>

//
// "LMT" for compressing out of gamut scene-referred values into AP1.
// 
// Input and output are ACES2065-1.
//

//
// Direction:
//    By default this transform operates in the forward direction (compressing the gamut).
//    If instead an inverse operation is needed (undoing a prior gamut compression), there
//    is a runtime flag to do this. In ctlrender, this can be achieved by appending 
//    '-param1 invert 1' after the '-ctl gamut_compress.ctl' string.
//



import "ACESlib.Transform_Common";



/* --- Gamut Compress Parameters --- */
// Distance from achromatic which will be compressed to the gamut boundary
const float lim_cyan =  1.147;
const float lim_magenta = 1.264;
const float lim_yellow = 1.312;

// Percentage of the core gamut to protect
const float thr_cyan = 0.815;
const float thr_magenta = 0.803;
const float thr_yellow = 0.880;

// Agressiveness of the compression curve
const float pwr = 1.2;



// Calculate compressed distance
float compress(float dist, float lim, float thr, float pwr, bool invert)
{
    float compr_dist;
    float scl;
    float nd;
    float p;

    if (dist < thr) {
        compr_dist = dist; // No compression below threshold
    }
    else {
        // Calculate scale factor for y = 1 intersect
        scl = (lim - thr) / pow(pow((1.0 - thr) / (lim - thr), -pwr) - 1.0, 1.0 / pwr);

        // Normalize distance outside threshold by scale factor
        nd = (dist - thr) / scl;
        p = pow(nd, pwr);

        if (!invert) {
            compr_dist = thr + scl * nd / (pow(1.0 + p, 1.0 / pwr)); // Compress
        }
        else {
            if (dist > (thr + scl)) {
                compr_dist = dist; // Avoid singularity
            }
            else {
                compr_dist = thr + scl * pow(-(p / (p - 1.0)), 1.0 / pwr); // Uncompress
            }
        }
    }

    return compr_dist;
}



void main 
(
    input varying float rIn, 
    input varying float gIn, 
    input varying float bIn, 
    input varying float aIn,
    output varying float rOut,
    output varying float gOut,
    output varying float bOut,
    output varying float aOut,
    input uniform bool invert = false
) 
{ 
    // Source values
    float ACES[3] = {rIn, gIn, bIn};

    // Convert to ACEScg
    float lin_AP1[3] = mult_f3_f44(ACES, AP0_2_AP1_MAT);

    // Achromatic axis
    float ach = max_f3(lin_AP1);

    // Distance from the achromatic axis for each color component aka inverse RGB ratios
    float dist[3];
    if (ach == 0.0) {
        dist[0] = 0.0;
        dist[1] = 0.0;
        dist[2] = 0.0;
    }
    else {
        dist[0] = (ach - lin_AP1[0]) / fabs(ach);
        dist[1] = (ach - lin_AP1[1]) / fabs(ach);
        dist[2] = (ach - lin_AP1[2]) / fabs(ach);
    }

    // Compress distance with parameterized shaper function
    float compr_dist[3] = {
        compress(dist[0], lim_cyan, thr_cyan, pwr, invert),
        compress(dist[1], lim_magenta, thr_magenta, pwr, invert),
        compress(dist[2], lim_yellow, thr_yellow, pwr, invert)
    };

    // Recalculate RGB from compressed distance and achromatic
    float compr_lin_AP1[3] = {
        ach - compr_dist[0] * fabs(ach),
        ach - compr_dist[1] * fabs(ach),
        ach - compr_dist[2] * fabs(ach)
    };

    // Convert back to ACES2065-1
    ACES = mult_f3_f44(compr_lin_AP1, AP1_2_AP0_MAT);

    // Write output
    rOut = ACES[0];
    gOut = ACES[1];
    bOut = ACES[2];
    aOut = aIn;
}