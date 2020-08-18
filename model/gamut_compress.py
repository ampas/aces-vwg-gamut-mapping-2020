# -*- coding: utf-8 -*-
"""
Gamut Compress
==============
"""

from __future__ import division, unicode_literals

import numpy as np

__all__ = ['compression_function', 'gamut_compression_operator']

# *****************************************************************************
# Preserving as much as possible of the "GamutCompress.glsl" file formatting.
# The bisection code could be removed entirely and replaced with "np.solve".
# This is not Pythonic nor great but will make update subsequent easier.
# *****************************************************************************


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


def main(rgb, invert=False, threshold=0.8, cyan=0.09, magenta=0.24, yellow=0.12, power=1.2):
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


def generate_test_images(samples=16):
    try:
        import colour
    except:
        print(
            '"colour-science" must be installed to generate the test images!')
        return

    np.random.seed(4)
    RGB = (np.random.random([samples, samples, 3]) - 0.5) * 4
    name_template = 'Gamut_Compress_{0}.exr'
    colour.write_image(RGB, name_template.format('Reference'))
    colour.write_image(gamut_compression_operator(RGB), name_template.format('PowerP'))


if __name__ == '__main__':
    generate_test_images()
