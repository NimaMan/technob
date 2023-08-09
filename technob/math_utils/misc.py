
import numpy as np


def root_mean_square(data):
    """
    Calculate the root mean square of the input data.
    
    Parameters:
        data (numpy.ndarray): Input data as a 1D numpy array.
        
    Returns:
        float: Root mean square value of the input data.
    """
    return float(np.sqrt(np.mean(np.square(data))))

