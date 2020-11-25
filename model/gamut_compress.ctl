
// <ACEStransformID>urn:ampas:aces:transformId:v1.5:LMT.Academy.GamutCompress.a1.0.1</ACEStransformID>
// <ACESuserName>ACES 1.3 Look - Gamut Compress</ACESuserName>

//
// "LMT" for compressing out of gamut scene-referred values into AP1 
// 
// Input and output are ACES2065-1
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
// Percentage of the core gamut to protect.
const float threshold_c = 0.815;
const float threshold_m = 0.803;
const float threshold_y = 0.880;

// Agressiveness of the compression curve
const float power = 1.2;

// Distance from achromatic which will be compressed to the gamut boundary
const float cyan =  1.147;
const float magenta = 1.264;
const float yellow = 1.312;



// calculate compressed distance
float compress(float dist, float lim, float thr, bool invert, float power)
{
    float cdist;
    float s;
    if (dist < thr) {
        cdist = dist;
    }
    else {
        s = (lim - thr) / pow(pow((1.0 - thr) / (lim - thr), -power) - 1.0, 1.0 / power); // calc y=1 intersect
        if (!invert) {
            cdist = thr + s * ((dist - thr) / s) / (pow(1.0 + pow((dist - thr) / s, power), 1.0 / power)); // compress
        }
        else {
            if (dist > (thr + s)) {
                cdist = dist; // avoid singularity
            }
            else {
                cdist = thr + s * pow(-(pow((dist - thr) / s, power) / (pow((dist - thr) / s, power) - 1.0)), 1.0 / power); // uncompress
            }
        }
    }
    return cdist;
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
    // source pixels
    float ACES[3] = {rIn, gIn, bIn};

    // convert to ACEScg
    float lin_AP1[3] = mult_f3_f44(ACES, AP0_2_AP1_MAT);

    // achromatic axis 
    float ach = max_f3(lin_AP1);

    // distance from the achromatic axis for each color component aka inverse RGB ratios
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

    // compress distance with parameterized shaper function
    float cdist[3] = {
        compress(dist[0], cyan, threshold_c, invert, power),
        compress(dist[1], magenta, threshold_m, invert, power),
        compress(dist[2], yellow, threshold_y, invert, power)
    };

    // recalculate RGB from compressed distance and achromatic
    // effectively this scales each color component relative to achromatic axis by the compressed distance
    float cLin_AP1[3] = {
        ach - cdist[0] * fabs(ach),
        ach - cdist[1] * fabs(ach),
        ach - cdist[2] * fabs(ach)
    };

    // convert back to ACES2065-1
    ACES = mult_f3_f44(cLin_AP1, AP1_2_AP0_MAT);

    // write output
    rOut = ACES[0];
    gOut = ACES[1];
    bOut = ACES[2];
    aOut = aIn;
}