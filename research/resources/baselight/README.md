# BLG Display Transforms for Baselight for Nuke

Included here is the set of BLG files demonstrated by Nick Shaw during [Gamut Mapping VWG #16](https://transcripts.gotomeeting.com/#/s/091620f84e8b78a625576072028307f19740ae308a9ce78bab1ad33bc81d9001) (at about 45 minutes).

The idea is that these will allow people to view the output of the gamut mapper through a variety of display transforms, and therefore hopefully judge its affect on image appearance in a way which is not tied to the ACES Output Transform. We want to avoid making “corrections” to the behaviour of the gamut mapper to compensate for e.g. hue skewing which is in fact a result of the display transform.

## Files

The names of the BLG files should be self-explanatory:

- `ACEScg_to_ACES_Rec709.blg.exr` (the standard ACES Rec.709 Output Transform)
- `ACEScg_to_ARRI_K1S1.blg.exr` (Baselight's **ARRI Photometric v2** DRT)
- `ACEScg_to_ALF-2_Rec709.blg.exr` (ARRI's **ALEXA Look File v2** DRT)
- `ACEScg_to_IPP2_Rec709.blg.exr` (RED's **IPP2** DRT)
- `ACEScg_to_TCAM_Rec709.blg.exr` (Baselight's **Truelight CAM** DRT)

These can be used in [Baselight for Nuke](http://filmlight.ltd.uk/support/customer-login/baselight_ed/baselight_nuke_v5.php) in free mode. This does require a Nuke license, as Nuke Non-Commercial does not support 3rd party plugins.

##Brief instructions

- Use a Baselight node as your View Transform. Nuke’s VLUT should therefore be set to ***None*** or ***RAW***.
- Chose ***from blg*** for both ***set input colour space*** and ***set output colour space***.
- Select one of the BLG files in the ***blg file*** field.
- Confirm that once the BLG has loaded, ***input colour space*** is set to ***ACEScg: Linear / AP1*** and ***output colour space*** is set to ***Rec.1886: 2.4 Gamma / Rec.709***.
- Change output colour space if required for your display to ***sRGB: ~2.2 Gamma / Rec.709*** or ***Apple: ~2.2 Gamma / P3 D65*** (Apple Display P3).

Your node tree should now look something like this:
![Example Nuke setup](https://raw.githubusercontent.com/colour-science/aces-vwg-gamut-mapping-2020/master/research/resources/baselight/images/BLG_Nuke_setup.png)
