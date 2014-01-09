#!/usr/bin/python
import glob
import numpy as np

from scipy.ndimage import gaussian_filter
from scipy.ndimage import gaussian_laplace
from scipy.ndimage import convolve
from scipy.ndimage import imread
from scipy.ndimage.interpolation import rotate
from math import cos, sin, pi


"""

Parameters
----------
sigma: scalar
The scale of the Gaussian and the Laplacian of Gaussian filters.
scales: list of tuples
The scales of the anisotropic gaussian derivative filters.
angles: list of scalars
The angles of the anisotropic gaussian derivative filters.

Returns
----------
filters: list of functions
A list of functions which are the filters. These functions
take a single image as parameter and return a filter response.

"""
def generate_filters(sigma, scales, angles):
    filters = []
    
    # Gaussian filter
    gauss_filter = lambda I: gaussian_filter(I, sigma)
    filters.append(gauss_filter)
    
    # Laplacian of Gaussian filter
    laplacian_filter = lambda I: gaussian_laplace(I, sigma)
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
        response = convolve(I, rotated_mask) #TODO: + 180?
        responses.append(response)

    aggr_responses = np.dstack(responses)
    return np.max(aggr_responses, axis=2)


def apply_filter_bank(I, filter_bank):
    responses = [f(I) for f in filter_bank]
    return np.dstack(responses)


def generate_filter_responses(images_path,  dimensions, filter_bank, output_folder):
    image_files = glob.glob(images_path)
    rows,cols,n = dimensions
    for image_file in image_files:
        image = imread(image_file, flatten=True)
        filter_response = apply_filter_bank(image, filter_bank)
        pixel_responses = filter_response.reshape(rows * cols, n)
        np.savetxt(output_folder + image.split("/")[-1] + ".txt", pixel_responses)


if __name__ == "__main__":
    print "hey"
    filters = generate_filters()
    print filters
    
