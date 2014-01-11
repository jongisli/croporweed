#!/usr/bin/python
import glob
import numpy as np

from scipy.cluster.vq import kmeans
from scipy.ndimage import gaussian_filter
from scipy.ndimage import gaussian_laplace
from scipy.ndimage import convolve


def get_texture_data(data_path):
    datafiles = glob.glob(data_path)

    texture_data = []
    for f in datafiles:
        data = np.loadtxt(f)
        texture_data.append(data)
    
    return np.vstack(texture_data)


def compute_textons(texture_data, texton_count):
    textons, _ = kmeans(texture_data, texton_count)
    return textons


def texton_visualization_filters(resolution, sigma, scales):
    impulse = np.zeros((resolution,resolution))
    impulse[resolution/2 + 1][resolution/2 + 1] = 1

    filters = []
    filters.append(gaussian_filter(impulse, sigma))
    filters.append(gaussian_laplace(impulse, sigma))
    for _ord in [1,2]:
        for scale in scales:
            filters.append(gaussian_filter(impulse, scale, order=[_ord,0]))

    return filters


def visualize_textons(textons, filters):
    tex_images = []
    for tex in textons:
        tex_collection = [t*f for t,f in zip(tex, filters)]
        tex_visualization = np.sum(tex_collection, axis=0)
        tex_images.append(tex_visualization)

    return tex_images

    
def generate_model(data, textons):
    dist = lambda x: np.apply_along_axis(np.linalg.norm, 1, textons - x)
    dists = np.apply_along_axis(dist, 1, data)
    nearest = np.argmin(dists, axis=1)
    return np.bincount(nearest)
    

if __name__ == "__main__":
    print "hey textons.py"

