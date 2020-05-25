# ACES - Virtual Working Group - Gamut Mapping - 2020

This repository hosts, in a version controlled location, a snapshot of the research and development effort of the [ACES Virtual Working Group on Gamut Mapping - 2020](https://community.acescentral.com/t/new-aces-working-group-gamut-mapping/).

The Virtual Working Group proposal can be read in this [document](https://community.acescentral.com/uploads/short-url/kax9E4X8dTMd9PkASqL7bz7S4qU.pdf).

A [Dropbox Workspace](https://aces.mp/GamutVWGDocs) is available as the central location for sharing resources.

## Repositories

As of this writing, *colour-science* and *jedypod* implementations do not reach parity and will yield different results because of variation in the parameterisation of the implemented gamut mapping study models.

The following repositories are available in alphabetical order:

### [colour-science/gamut-mapping-ramblings](https://github.com/colour-science/gamut-mapping-ramblings)

![Gamut Medicina 01](https://raw.githubusercontent.com/colour-science/gamut-mapping-ramblings/master/resources/images/Gamut_Medicina_01.png)

Provides various Python Jupyter Notebooks with implementation of the following gamut mapping study model(s):

- [Mansencal and Scharfenberg (2020) HSV Control Based Study Model](https://community.acescentral.com/t/gamut-mapping-in-cylindrical-and-conic-spaces/) built on top of the [HSV colourspace](https://en.wikipedia.org/wiki/HSL_and_HSV)
- [Smith (2020) - RGB Saturation Study Model](https://community.acescentral.com/t/rgb-saturation-gamut-mapping-approach-and-a-comp-vfx-perspective/) built on top of the [RGB colourspace](https://en.wikipedia.org/wiki/Color_spaces_with_RGB_primaries)

Please refer to the repository [README.rst](https://github.com/colour-science/gamut-mapping-ramblings/README.rst) file for more information.

### [jedypod/gamut-compress](https://github.com/jedypod/gamut-compress)

![Resolve UI](https://raw.githubusercontent.com/jedypod/gamut-compress/master/images/screenshots/GamutCompress_resolve-ui.png)

Provides DCC implementation for [The Foundry Nuke](https://www.foundry.com/products/nuke) and [Davinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve/) of the following gamut mapping study model(s):

- [Smith (2020) - RGB Saturation Study Model](https://community.acescentral.com/t/rgb-saturation-gamut-mapping-approach-and-a-comp-vfx-perspective/) built on top of the [RGB colourspace](https://en.wikipedia.org/wiki/Color_spaces_with_RGB_primaries)

![Collage Gamut Compressed](https://raw.githubusercontent.com/jedypod/gamut-compress/master/images/collage_compressed.rrt.jpg)

Please refer to the repository [README.md](https://github.com/jedypod/gamut-compress/README.md) file for more information.

## License

For Third Party license details see [THIRD_PARTY](THIRD_PARTY).

The ACES - Virtual Working Group - Gamut Mapping - 2020 Repository is provided by the Academy under the following terms and conditions:

Copyright © 2020 Academy of Motion Picture Arts and Sciences ("A.M.P.A.S."). Portions contributed by others as indicated. All rights reserved.

A worldwide, royalty-free, non-exclusive right to copy, modify, create derivatives, and use, in source and binary forms, is hereby granted, subject to acceptance of this license. Performance of any of the aforementioned acts indicates acceptance to be bound by the following terms and conditions:

Copies of source code, in whole or in part, must retain the above copyright notice, this list of conditions and the Disclaimer of Warranty.

Use in binary form must retain the above copyright notice, this list of conditions and the Disclaimer of Warranty in the documentation and/or other materials provided with the distribution.

Nothing in this license shall be deemed to grant any rights to trademarks, copyrights, patents, trade secrets or any other intellectual property of A.M.P.A.S. or any contributors, except as expressly stated herein.

Neither the name "A.M.P.A.S." nor the name of any other contributors to this software may be used to endorse or promote products derivative of or based on this software without express prior written permission of A.M.P.A.S. or the contributors, as appropriate.

This license shall be construed pursuant to the laws of the State of California, and any disputes related thereto shall be subject to the jurisdiction of the courts therein.

Disclaimer of Warranty: THIS SOFTWARE IS PROVIDED BY A.M.P.A.S. AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT ARE DISCLAIMED. IN NO EVENT SHALL A.M.P.A.S., OR ANY CONTRIBUTORS OR DISTRIBUTORS, BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, RESITUTIONARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

WITHOUT LIMITING THE GENERALITY OF THE FOREGOING, THE ACADEMY SPECIFICALLY DISCLAIMS ANY REPRESENTATIONS OR WARRANTIES WHATSOEVER RELATED TO PATENT OR OTHER INTELLECTUAL PROPERTY RIGHTS IN THE RAW TO ACES UTILITY REFERENCE IMPLEMENTATION, OR APPLICATIONS THEREOF, HELD BY PARTIES OTHER THAN A.M.P.A.S., WHETHER DISCLOSED OR UNDISCLOSED.
