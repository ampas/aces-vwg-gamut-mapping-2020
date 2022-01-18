# -*- coding: utf-8 -*-
"""
ACES 1.3 Reference Gamut Compression
==============
Gamut compression algorithm to bring out-of-gamut scene-referred values into the ACEScg gamut (AP1).

Based on https://github.com/ampas/aces-dev/blob/dev/transforms/ctl/lmt/LMT.Academy.ReferenceGamutCompress.ctl

<ACEStransformID>urn:ampas:aces:transformId:v1.5:LMT.Academy.ReferenceGamutCompress.a1.v1.0</ACEStransformID>
<ACESuserName>ACES 1.3 Look - Reference Gamut Compress</ACESuserName>
"""

from __future__ import division, unicode_literals

import numpy as np

__all__ = ['compression_function', 'gamut_compression_operator']


# yapf: disable
# calculate compressed distance
def compress(dist, lim, thr, invert, power):
    # power(p) compression function plot https://www.desmos.com/calculator/54aytu7hek
    s = (lim-thr)/np.power(np.power((1-thr)/(lim-thr),-power)-1,1/power) # calc y=1 intersect
    if not invert:
	    cdist = thr+s*((dist-thr)/s)/(np.power(1+np.power((dist-thr)/s,power),1/power)) # compress
    else:
	    cdist = thr+s*np.power(-(np.power((dist-thr)/s,power)/(np.power((dist-thr)/s,power)-1)),1/power) # uncompress

    cdist = np.nan_to_num(cdist)

    cdist[dist < thr] = dist[dist < thr]

    return cdist


def main(rgb, invert=False, threshold=[0.815, 0.803, 0.88], cyan=0.147, magenta=0.264, yellow=0.312, power=1.2):
    rgb = np.asarray(rgb)
    threshold = np.asarray(threshold)
    if not threshold.shape:
        threshold = np.tile(threshold, 3)

    # thr is the percentage of the core gamut to protect.
    thr = np.clip(threshold, -np.inf, 0.9999).reshape(
        [1] * (rgb.ndim - 1) + [3])

    # lim is the max distance from the gamut boundary that will be compressed
    # 0 is a no-op, 1 will compress colors from a distance of 2 from achromatic to the gamut boundary
    lim = np.array([cyan+1, magenta+1, yellow+1])

    # achromatic axis
    ach = np.max(rgb, axis=-1)[..., np.newaxis]

    # distance from the achromatic axis for each color component aka inverse rgb ratios
    dist = np.where(ach == 0.0, 0.0, (ach-rgb)/np.abs(ach))

    # compress distance with user controlled parameterized shaper function
    cdist = compress(dist, lim, thr, invert, power)

    crgb = ach-cdist*np.abs(ach)

    return crgb
# yapf: enable

compression_function = compress
gamut_compression_operator = main
