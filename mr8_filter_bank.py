#!/usr/bin/python
import numpy as np

from scipy.ndimage import gaussian_filter
from scipy.ndimage import gaussian_laplace
from scipy.ndimage import convolve

from scipy.ndimage.interpolation import rotate

from math import cos, sin, pi


def generate_filters():
    filters = []
    # scales and angles for edge and bar filters
    scales = [(1,3), (2,6), (4,12)]
    angles = [0, 30, 60, 90, 120, 150]
    
    # Gaussian filter
    gauss_filter = lambda I: gaussian_filter(I, 10)
    filters.append(gauss_filter)
    
    # Laplacian of Gaussian filter
    laplacian_filter = lambda I: gaussian_laplace(I, 10)
    filters.append(laplacian_filter)
    
    # Edge filters (first order Gaussian derivative)
    for scale in scales:
        filters.append(
          lambda I, scale=scale: \
          max_anisotropic_derivative_filter(I, scale, angles, 1))
        
    # Bar filters (second order Gaussian derivative)
    for scale in scales:
        filters.append(
          lambda I, scale=scale: \
          max_anisotropic_derivative_filter(I, scale, angles, 2))

    return filters


def max_anisotropic_derivative_filter(I, scale, angles, order):
    impulse = np.zeros((101,101))
    impulse[50][50] = 1
    gaussian_mask = gaussian_filter(impulse, scale, order=[order,0])

    responses = []
    for angle in angles:
        rotated_mask = rotate(gaussian_mask, angle, reshape=False)
        response = convolve(I, rotated_mask)
        responses.append(response)

    aggr_responses = np.dstack(responses)
    return np.max(aggr_responses, axis=2)


def apply_filter_bank(I, filter_bank):
    responses = [f(I) for f in filter_bank]
    return np.dstack(responses)


if __name__ == "__main__":
    print "hey"
    filters = generate_filters()
    print filters
    
