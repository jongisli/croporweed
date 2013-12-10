from scipy.ndimage import gaussian_filter
from scipy.ndimage import gaussian_laplace
from scipy.ndimage import gaussian_filter1d
from math import cos, sin, pi


def generate_filters():
    filters = {}
    # scales and orientations for edge and bar filters
    scales = [(1,3), (2,6), (4,12)]
    orientations = [pi/6, pi/3, pi/2, 2*pi/3, 5*pi/6]
    
    # Gaussian filter
    gauss_filter = lambda I: gaussian_filter(I, 10)
    filters.append(gauss_filter)
    # Laplacian of Gaussian filter
    laplacian_filter = lambda I: gaussian_laplace(I, 10)
    filters.append(laplacian_filter)
    # Edge filters (first order Gaussian derivative)
    for scale in scales:
        break

    return filters


def max_edge_filter(I, scale, angles):
    sigma_x, sigma_y = scale
    F_x = gaussian_filter1d(I, sigma_x, axis=-1, order=1)
    F_y = gaussian_filter1d(I, sigma_y, axis=0, order=1)

    responses = []
    for angle in angles:
        response = cos(angle) * F_x + sin(angle) * F_y)
        responses.append(response)

    aggr_responses = np.dstack(responses)
    return np.max(A, axis=2)
        
    
