# ACES 1.3 Reference Gamut Compression

This folder contains a set of implementations of the ACES 1.3 Reference Gamut Compression algorithm for various DCCs, to make the algorithm available until it has been more widely natively implemented.

These implementations are:
* Baselight - a Matchbox Shader implementation customized so that Truelight automatically handles the required color space conversions.
* Matchbox - a generic Matchbox Shader implementation with a dropdown to select the working color space.
* Nuke - Two implementations, one using BlinkScript, and one in pure Nuke so it can be used in Nuke non-commercial.
* Python - An implementation which operates on NumPy arrays.
* Resolve - A DCTL implementation which can be applied either through the LUT menu or through the DCTL OFX to allow use of the ***direction*** control.

These implementations are intended as a stop-gap, and should be considered deprecated once the algorithm is either implemented natively in a particular DCC, or OCIO 2.1+ is supported.