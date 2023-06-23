# ACES 1.3 Reference Gamut Compression

This folder contains a set of implementations of the ACES 1.3 Reference Gamut Compression algorithm for various DCCs, to make the algorithm available until it has been more widely natively implemented. These differ slightly from the CTL implementation, in that they do not all take ACES2065-1 input (see below).

These implementations are:
* Baselight - a Matchbox Shader implementation customized so that Truelight automatically handles the required color space conversions.
* Matchbox - a generic Matchbox Shader implementation with a dropdown to select the in/out color space.
* Nuke - Two implementations, one using BlinkScript, and one in pure Nuke. These implementations expect and produce ACEScg image data, since this is the default ACES working space in Nuke.
* Python - An implementation which operates on NumPy arrays. This implementation expects and produces ACEScg image data.
* Resolve - A DCTL implementation which can be applied either through the LUT menu or through the DCTL OFX to allow use of the ***direction*** control. This implementation expects and produces ACEScct image data, since this is the default ACES working space in Resolve.

These implementations are intended only as a stop-gap, and should be considered deprecated once the algorithm is either implemented natively in a particular DCC, or OCIO 2.1+ is supported.