#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import numpy as np

import colour
from colour.models import (
                           RGB_Colourspace,
                           normalised_primary_matrix,
                           RGB_to_RGB,
                           ACES_2065_1_COLOURSPACE,
                           ACES_CG_COLOURSPACE,
                           ALEXA_WIDE_GAMUT_COLOURSPACE,
                           CINEMA_GAMUT_COLOURSPACE,
                           RED_WIDE_GAMUT_RGB_COLOURSPACE,
                           S_GAMUT3_COLOURSPACE,
                           V_GAMUT_COLOURSPACE
                          )
from colour.colorimetry import ILLUMINANTS
from colour.utilities import tsplit

BMD_WIDE_GAMUT_V4_PRIMARIES = np.array([
    [0.7177, 0.3171],
    [0.2280, 0.8616],
    [0.1006, -0.0820],
])
"""
*BMD Wide Gamut V4* colourspace primaries.

BMD_WIDE_GAMUT_V4_PRIMARIES : ndarray, (3, 2)
"""

BMD_WIDE_GAMUT_V4_WHITEPOINT_NAME = 'D65'
"""
*BMD Wide Gamut V4* colourspace whitepoint name.

BMD_WIDE_GAMUT_V4_WHITEPOINT : unicode
"""

BMD_WIDE_GAMUT_V4_WHITEPOINT = (ILLUMINANTS[
    'CIE 1931 2 Degree Standard Observer'][BMD_WIDE_GAMUT_V4_WHITEPOINT_NAME])
"""
*BMD Wide Gamut V4* colourspace whitepoint.

BMD_WIDE_GAMUT_V4_WHITEPOINT : ndarray
"""

BMD_WIDE_GAMUT_V4_TO_XYZ_MATRIX = (normalised_primary_matrix(
    BMD_WIDE_GAMUT_V4_PRIMARIES, BMD_WIDE_GAMUT_V4_WHITEPOINT))
"""
*BMD Wide Gamut V4* colourspace to *CIE XYZ* tristimulus values matrix.

BMD_WIDE_GAMUT_V4_TO_XYZ_MATRIX : array_like, (3, 3)
"""

XYZ_TO_BMD_WIDE_GAMUT_V4_MATRIX = (
    np.linalg.inv(BMD_WIDE_GAMUT_V4_TO_XYZ_MATRIX))
"""
*CIE XYZ* tristimulus values to *BMD Wide Gamut V4* colourspace matrix.

XYZ_TO_BMD_WIDE_GAMUT_V4_MATRIX : array_like, (3, 3)
"""

BMD_WIDE_GAMUT_V4_COLOURSPACE = RGB_Colourspace(
    'BMD Wide Gamut V4',
    BMD_WIDE_GAMUT_V4_PRIMARIES,
    BMD_WIDE_GAMUT_V4_WHITEPOINT,
    BMD_WIDE_GAMUT_V4_WHITEPOINT_NAME,
    BMD_WIDE_GAMUT_V4_TO_XYZ_MATRIX,
    XYZ_TO_BMD_WIDE_GAMUT_V4_MATRIX,
    None,
    None,
)

# ColorChecker 24 values as per SMPTE 2065-1
CC24 = np.array([[0.11877, 0.08709, 0.05895],
                 [0.40002, 0.31916, 0.23736],
                 [0.18476, 0.20398, 0.31311],
                 [0.10901, 0.13511, 0.06493],
                 [0.26684, 0.24604, 0.40932],
                 [0.32283, 0.46208, 0.40606],
                 [0.38605, 0.22743, 0.05777],
                 [0.13822, 0.13037, 0.33703],
                 [0.30202, 0.13752, 0.12758],
                 [0.0931, 0.06347, 0.13525],
                 [0.34876, 0.43654, 0.10613],
                 [0.48655, 0.36685, 0.08061],
                 [0.08732, 0.07443, 0.27274],
                 [0.15366, 0.25692, 0.09071],
                 [0.21742, 0.0707, 0.0513],
                 [0.58919, 0.53943, 0.09157],
                 [0.30904, 0.14818, 0.27426],
                 [0.14901, 0.23378, 0.35939]])

CC24_AP1 = RGB_to_RGB(CC24, ACES_2065_1_COLOURSPACE, ACES_CG_COLOURSPACE)

ach = np.max(CC24_AP1, axis=-1)[..., np.newaxis]
dist = ((ach - CC24_AP1) / ach)
c, m, y = tsplit(dist)

print 'Thresholds:'
print np.max(c), np.max(m), np.max(y)

unit_cube = np.array([[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1],
                      [0, 1, 1],
                      [1, 0, 1],
                      [1, 1, 0]])

bounds = []

bounds.append(RGB_to_RGB(unit_cube,
              ALEXA_WIDE_GAMUT_COLOURSPACE,
              ACES_CG_COLOURSPACE,
              chromatic_adaptation_transform='CAT02'))

bounds.append(RGB_to_RGB(unit_cube,
              BMD_WIDE_GAMUT_V4_COLOURSPACE,
              ACES_CG_COLOURSPACE,
              chromatic_adaptation_transform='Bradford'))

bounds.append(RGB_to_RGB(unit_cube,
              CINEMA_GAMUT_COLOURSPACE,
              ACES_CG_COLOURSPACE,
              chromatic_adaptation_transform='CAT02'))

bounds.append(RGB_to_RGB(unit_cube,
              RED_WIDE_GAMUT_RGB_COLOURSPACE,
              ACES_CG_COLOURSPACE,
              chromatic_adaptation_transform='Bradford'))

bounds.append(RGB_to_RGB(unit_cube,
              S_GAMUT3_COLOURSPACE,
              ACES_CG_COLOURSPACE,
              chromatic_adaptation_transform='CAT02'))

bounds.append(RGB_to_RGB(unit_cube,
              V_GAMUT_COLOURSPACE,
              ACES_CG_COLOURSPACE,
              chromatic_adaptation_transform='CAT02'))

bounds = np.array(bounds).reshape(-1, 3)

ach = np.max(bounds, axis=-1)[..., np.newaxis]
dist = ((ach - bounds) / ach)
c, m, y = tsplit(dist)

print 'Limits:'
print np.max(c) - 1, np.max(m) - 1, np.max(y) - 1