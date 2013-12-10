from scipy.ndimage import gaussian_filter
from scipy.ndimage import gaussian_laplace
from scipy.ndimage import gaussian_filter1d
from math import cos, sin, pi


def generate_filters():
    filters = {}
    # scales for edge and bar filters
    scales = [(1,3), (2,6), (4,12)]
    
    # Gaussian filter
    gauss = lambda x: gaussian_filter(x, 10)
    # Laplacian of Gaussian filter
    laplacian = lambda x: gaussian_laplace(x, 10)
    
    
    
