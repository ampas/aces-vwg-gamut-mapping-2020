# ACES - Virtual Working Group - Gamut Mapping - 2020

This repository hosts, in a version controlled location, a snapshot of the research and development effort of the [ACES Virtual Working Group on Gamut Mapping - 2020](https://community.acescentral.com/t/new-aces-working-group-gamut-mapping/).

The Virtual Working Group proposal can be read in this [document](https://community.acescentral.com/uploads/short-url/kax9E4X8dTMd9PkASqL7bz7S4qU.pdf).

A [Dropbox Workspace](https://aces.mp/GamutVWGDocs) is available as the central location for sharing resources.

## Model

The gamut mapping model selected by the Virtual Working Group is based on
[Smith (2020) - RGB Saturation Study Model](#smith-2020---rgb-saturation-study-model).

The following implementations are expected to be available in the [model](model)
directory:

- DCTL for [Davinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve/)
- BlinkScript Kernel for [The Foundry Nuke](https://www.foundry.com/products/nuke)
- CTL for [The Color Transformation Language](https://github.com/ampas/CTL)

## Research

The [research](research) directory contains a mix of useful resources pertaining
to research, experimentation and analysis conducted by the Virtual Working Group.

### Gamut Mapping Study Models

#### Smith (2020) - RGB Saturation Study Model

[Smith (2020) - RGB Saturation Study Model](https://community.acescentral.com/t/rgb-saturation-gamut-mapping-approach-and-a-comp-vfx-perspective/) is built on top of the [RGB colourspace](https://en.wikipedia.org/wiki/Color_spaces_with_RGB_primaries) with the following approach:

- An achromatic axis is computed for the scene-referred RGB exposure values.
- The pseudo-distance between the individual 𝑅, 𝐺 and 𝐵 components and the achromatic axis is compressed with a cherry-picked compression function.

The model is extremely simple and elegant while offering good computational speed.

The following implementations are available:

##### [jedypod/gamut-compress](research/repositories/jedypod/gamut-compress)

Provides DCC implementation for [The Foundry Nuke](https://www.foundry.com/products/nuke) and [Davinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve/).

Please refer to the repository [README.md](https://github.com/jedypod/gamut-compress/README.md) file for more information.

![Collage Gamut Compressed](https://raw.githubusercontent.com/jedypod/gamut-compress/master/images/collage_compressed.rrt.jpg)

![Resolve UI](https://raw.githubusercontent.com/jedypod/gamut-compress/master/images/screenshots/GamutCompress_resolve-ui.png)

##### [colour-science/gamut-mapping-ramblings](research/repositories/colour-science/gamut-mapping-ramblings)

Provides Python implementation via Jupyter Notebooks.

Please refer to the repository [README.rst](https://github.com/colour-science/gamut-mapping-ramblings/README.rst) file for more information.

![Gamut Medicina 05](https://raw.githubusercontent.com/colour-science/gamut-mapping-ramblings/master/resources/images/Gamut_Medicina_05.png)

#### Mansencal and Scharfenberg (2020) HSV Control Based Study Model

[Mansencal and Scharfenberg (2020) HSV Control Based Study Model](https://community.acescentral.com/t/gamut-mapping-in-cylindrical-and-conic-spaces/) is built on top of the
[HSV colourspace](https://en.wikipedia.org/wiki/HSL_and_HSV) with the following
approach:

- Scene-referred RGB exposure values are converted to HSV.
- The saturation component 𝑆 is compressed with a cherry-picked compression function.
- The hue component 𝐻 is warped according to user defined control values.
- The HSV values are converted back to scene-referred RGB exposure values and then blended with the original scene-referred RGB exposure values function through a smoothstep function.

The model is much more complex and slower but offers direct controls over hue.

The following implementations are available:

##### [colour-science/gamut-mapping-ramblings](research/repositories/colour-science/gamut-mapping-ramblings)

Provides Python implementation via Jupyter Notebooks.

Please refer to the repository [README.rst](https://github.com/colour-science/gamut-mapping-ramblings/README.rst) file for more information.

![Gamut Medicina 01](https://raw.githubusercontent.com/colour-science/gamut-mapping-ramblings/master/resources/images/Gamut_Medicina_01.png)

#### Johnson (2020) ARRI Gamut Mapping Study Model

[Johnson (2020) ARRI Gamut Mapping Study Model](https://community.acescentral.com/t/gamut-mapping-method-nuke-script-example/) is focusing on ARRI colourspaces
while adopting some principles from Smith (2020) model.

The following implementations are available:

##### [johnson322/ArriGamutMapping](research/repositories/johnson322/ArriGamutMapping)

Provides DCC implementation for [The Foundry Nuke](https://www.foundry.com/products/nuke).

Please refer to the repository [README.md](https://github.com/johnson322/ArriGamutMapping/blob/master/README.md) file for more information.

### Notebooks & Scripts

#### Simplistic Gamut Mapping Approaches in Nuke

A [The Foundry Nuke script](research/resources/scripts/Matthias Scharfenberg - gamut_mapping_demo_v02.nk) illustrating some examples of simplistic approaches to the gamut mapping problem by
[Matthias Scharfenberg](https://community.acescentral.com/t/simplistic-gamut-mapping-approaches-in-nuke/).

#### Sketches of Hue

A [Jupyter Notebook](research/repositories/scoopxyz/aces_vwg_gamutmapping_1)
exploring the concept of camera-referred "hue lines" by
[Sean Cooper](https://community.acescentral.com/t/notebook-sketches-of-hue).

![Sketches of Hue](https://i.imgur.com/dhYJBRU.png)

The notebook is directly viewable at this [url](https://seancooper.xyz/aces_vwg_gamutmapping_1/) and an online [Google Colab](https://colab.research.google.com/drive/1LTZEVQWsSJTcKll4VqYnY93RoNpyEh1u)
implementation is also available.

#### Virtual Camera Primaries Rendering of Spectral Locus

An online [Google Colab](https://colab.research.google.com/drive/1rSXtsBkucIn5Z8Jtm-tZ3lv7P8qPmsVk)
showcasing the distortions of camera spectral sensitivities upon projection in
the CIE 1931 Chromaticity Diagram by [Troy Sobotka](https://community.acescentral.com/t/virtual-camera-primaries-rendering-of-spectral-locus/).

![Virtual Camera Primaries Rendering of Spectral Locus](https://community.acescentral.com/uploads/default/original/2X/2/23346b664185a57e500ec39649e24d51f1954a88.gif)

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
