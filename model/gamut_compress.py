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
# compression function which gives the y=1 x in tersect at y=0
def f(x, k, thr, method):
    if method == 0:
        # natural logarithm compression method
        return (np.exp((1-thr+thr*np.log(1-x)-x*thr*np.log(1-x))/(thr*(1-x))))*thr+x*thr-k
    elif method == 1 or method == 2:
        return k
    elif method == 3:
        # natural exponent compression method
        return -np.log((-x+1)/(thr-x))*(-thr+x)+thr-k
    elif method == 4:
        # arctangent compression method
        return (2*np.tan( (np.pi*(1-thr))/(2*(x-thr)))*(x-thr))/np.pi+thr-k
    elif method == 5:
        # hyperbolic tangent compression method
        return np.arctanh((1-thr)/(x-thr))*(x-thr)+thr-k


def bisect(k, thr, method):
    # use a simple bisection algorithm to bruteforce the root of f
    # returns an approximation of the value of limit
    # such that the compression function intersects y=1 at desired value k
    # this allows us to specify the max distance we will compress to the gamut boundary

    tol = 0.0001 # accuracy of estimate
    nmax = 100 # max iterations

    # set up reasonable initial guesses for each method given output ranges of each function
    if method == 0:
        # natural logarithm needs a limit between -inf (linear), and 1 (clip)
        a = -15
        b = 0.98
    elif method == 5:
        # tanh needs more precision
        a = 1.000001
        b = 5
    else:
        a = 1.0001
        b = 5

    if np.sign(f(a, k, thr, method)) == np.sign(f(b, k, thr, method)):
        # bad estimate. return something close to linear
        if method == 0 or method == 3:
            return -100
        else:
            return 1.999999

    c = (a+b)/2
    y = f(c, k, thr, method)
    if abs(y) <= tol:
        return c # lucky guess

    n = 1
    while abs(y) > tol and n <= nmax:
        if np.sign(y) == np.sign(f(a, k, thr, method)):
            a = c
        else:
            b = c

        c = (a+b)/2
        y = f(c, k, thr, method)
        n += 1

    return c


# calculate compressed distance
def compress(dist, lim, thr, invert, method, power):
    if method == 0:
        # natural logarithm compression method: https://www.desmos.com/calculator/hmzirlw7tj
        # inspired by ITU-R BT.2446 http://www.itu.int/pub/R-REP-BT.2446-2019
        if not invert:
            cdist = thr*np.log(dist/thr-lim)-lim*thr*np.log(dist/thr-lim)+thr-thr*np.log(1-lim)+lim*thr*np.log(1-lim)
        else:
            cdist = np.exp((dist-thr+thr*np.log(1-lim)-lim*thr*np.log(1-lim))/(thr*(1-lim)))*thr+lim*thr
    elif method == 1:
        # simple Reinhard type compression method: https://www.desmos.com/calculator/lkhdtjbodx
        if not invert:
            cdist = thr + 1/(1/(dist - thr) + 1/(1 - thr) - 1/(lim - thr))
        else:
            cdist = thr + 1/(1/(dist - thr) - 1/(1 - thr) + 1/(lim - thr))
    elif method == 2:
        # power(p) compression function plot https://www.desmos.com/calculator/54aytu7hek
        s = (lim-thr)/np.power(np.power((1-thr)/(lim-thr),-power)-1,1/power) # calc y=1 intersect
        if not invert:
            cdist = thr+s*((dist-thr)/s)/(np.power(1+np.power((dist-thr)/s,power),1/power)) # compress
        else:
            cdist = thr+s*np.power(-(np.power((dist-thr)/s,power)/(np.power((dist-thr)/s,power)-1)),1/power) # uncompress
    elif method == 3:
        # natural exponent compression method: https://www.desmos.com/calculator/s2adnicmmr
        if not invert:
            cdist = lim-(lim-thr)*np.exp(-(((dist-thr)*((1*lim)/(lim-thr))/lim)))
        else:
            cdist = -np.log((dist-lim)/(thr-lim))*(-thr+lim)/1+thr
    elif method == 4:
        # arctangent compression method: plot https://www.desmos.com/calculator/olmjgev3sl
        if not invert:
            cdist = thr + (lim - thr) * 2 / np.pi * np.arctan(np.pi/2 * (dist - thr)/(lim - thr))
        else:
            cdist = thr + (lim - thr) * 2 / np.pi * np.tan(np.pi/2 * (dist - thr)/(lim - thr))
    elif method == 5:
        # hyperbolic tangent compression method: https://www.desmos.com/calculator/xiwliws24x
        if not invert:
            cdist = thr + (lim - thr) * np.tanh( ( (dist - thr)/( lim - thr)))
        else:
            cdist = thr + (lim - thr) * np.arctanh( dist/( lim - thr) - thr/( lim - thr))

    cdist = np.nan_to_num(cdist)

    cdist[dist < thr] = dist[dist < thr]

    return cdist


def main(rgb, method=2, invert=False, hexagonal=False, threshold=0.8, cyan=0.09, magenta=0.24, yellow=0.12, power=1.2, shd_rolloff=0):
    rgb = np.asarray(rgb)
    threshold = np.asarray(threshold)
    if not threshold.shape:
        threshold = np.tile(threshold, 3)

    # thr is the percentage of the core gamut to protect.
    thr = np.clip(threshold, -np.inf, 0.9999).reshape(
        [1] * (rgb.ndim - 1) + [3])

    # lim is the max distance from the gamut boundary that will be compressed
    # 0 is a no-op, 1 will compress colors from a distance of 2 from achromatic to the gamut boundary
    # if method is Reinhard, use the limit as-is
    if method == 1 or method == 2:
        lim = np.array([cyan+1, magenta+1, yellow+1])
    else:
        # otherwise, we have to bruteforce the value of limit
        # such that lim is the value of x where y=1 - also enforce sane ranges to avoid nans

        # Not sure of a way to pre-calculate a constant using the values from the ui parameters in GLSL...
        # This approach might have performance implications
        lim = np.array([
            bisect(np.clip(cyan, 0.0001, np.inf)+1, np.float(np.squeeze(thr[..., 0])), method),
            bisect(np.clip(magenta, 0.0001, np.inf)+1, np.float(np.squeeze(thr[..., 1])), method),
            bisect(np.clip(yellow, 0.0001, np.inf)+1, np.float(np.squeeze(thr[..., 2])), method)])

    # achromatic axis
    ach = np.max(rgb, axis=-1)[..., np.newaxis]

    # achromatic with shadow rolloff below shd_rolloff threshold
    ach_shd = 1-np.where((1-ach)<(1-shd_rolloff),1-ach,(1-shd_rolloff)+shd_rolloff*np.tanh((((1-ach)-(1-shd_rolloff))/shd_rolloff)))

    # distance from the achromatic axis for each color component aka inverse rgb ratios
    dist = np.where(ach_shd == 0, 0, (ach-rgb)/ach_shd)

    # compress distance with user controlled parameterized shaper function
    if hexagonal:
        # Based on Nick Shaw's variation on the gamut mapping algorithm
        # https://community.acescentral.com/t/a-variation-on-jeds-rgb-gamut-mapper/3060
        sat = np.concatenate([x[..., np.newaxis] for x in [np.max(dist, axis=-1)]*3], axis=-1)
        csat = compress(sat, lim, thr, invert, method, power)
        cdist = np.where(sat == 0, dist, dist* csat / sat)
    else:
        cdist = compress(dist, lim, thr, invert, method, power)

    crgb = ach-cdist*ach_shd

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
    for method in range(0, 6):
        colour.write_image(
            gamut_compression_operator(RGB, method=method),
            name_template.format('GM_Method_{0}'.format(method)))

        colour.write_image(
            gamut_compression_operator(RGB, method=method, hexagonal=True),
            name_template.format('GM_Method_{0}_Hexagonal'.format(method)))

        colour.write_image(
            gamut_compression_operator(
                RGB, threshold=[0.2, 0.4, 0.6], method=method),
            name_template.format(
                'GM_Method_{0}_DecoupledThreshold'.format(method)))

        colour.write_image(
            gamut_compression_operator(
                RGB, threshold=[0.2, 0.4, 0.6], method=method, hexagonal=True),
            name_template.format(
                'GM_Method_{0}_Hexagonal_DecoupledThreshold'.format(method)))


if __name__ == '__main__':
    generate_test_images()
