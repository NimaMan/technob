
import typing
from numba import jit
import numpy as np
import librosa
from scipy import signal
from scipy.ndimage import filters, median_filter
from scipy.spatial import distance
from scipy.signal import find_peaks


def root_mean_square(data):
    """
    Calculate the root mean square of the input data.
    
    Parameters:
        data (numpy.ndarray): Input data as a 1D numpy array.
        
    Returns:
        float: Root mean square value of the input data.
    """
    return float(np.sqrt(np.mean(np.square(data))))


@jit(nopython=True)
def cummulative_sum_Q(R):
    '''
    Calculate the cummulative sum of the input matrix R.

    '''
    len_x, len_y = R.shape
    Q = np.zeros((len_x + 2, len_y + 2))
    for i in range(len_x):
        for j in range(len_y):
            Q[i+2, j+2] = max(
                    Q[i+1, j+1],
                    Q[i, j+1],
                    Q[i+1, j]) + R[i, j]
    return np.max(Q)


@jit(nopython=True)
def min_max_normalize_numba(X, floor=0.0):
    """Numba-optimized min-max normalization."""
    X_min = np.zeros(X.shape[0])
    X_max = np.zeros(X.shape[0])
    
    for i in range(X.shape[0]):
        X_min[i] = X[i, :].min()
        X_max[i] = X[i, :].max()
    
    norm_X = floor + (X - X_min.reshape(-1, 1)) / (X_max.reshape(-1, 1) - X_min.reshape(-1, 1))
    return norm_X


def lognormalize(X, floor=0.0, min_db=-80):
    """
    Optimized version of the logarithmic scaling function for the feature matrix.

    Parameters:
        X (np.array): Feature matrix where each row represents a feature vector.
        floor (float, optional): Value to replace zeros in the matrix. Default is 0.0.
        min_db (float, optional): Minimum decibel level for scaling. Default is -80.

    Returns:
        np.array: Logarithmically scaled feature matrix.
    """
    # Use numpy's where function to replace zeros with the floor value
    X = np.where(X == 0, floor, X)

    # Convert to dB scale using numpy's built-in functions
    X_db = 10 * np.log10(np.abs(X))

    # Clip to the specified minimum dB value using numpy's maximum function
    X_db = np.maximum(X_db, X_db.max() + min_db)

    return X_db


def normalize(X, norm_type="min_max", floor=0.0, min_db=-80):
    """
    Normalizes the given matrix of features.
    Parameters
    ----------
    X: np.array
        Each row represents a feature vector.
    norm_type: {"min_max", "log", np.inf, -np.inf, 0, float > 0, None}
        - `"min_max"`: Min/max scaling is performed
        - `"log"`: Logarithmic scaling is performed
        - `np.inf`: Maximum absolute value
        - `-np.inf`: Mininum absolute value
        - `0`: Number of non-zeros
        - float: Corresponding l_p norm.
        - None : No normalization is performed
    Returns
    -------
    norm_X: np.array
        Normalized `X` according the the input parameters.
    """
    if isinstance(norm_type, str):
        if norm_type == "min_max":
            return min_max_normalize_numba(X, floor=floor)
        if norm_type == "log":
            return lognormalize(X, floor=floor, min_db=min_db)
    return librosa.util.normalize(X, norm=norm_type, axis=1)


def gaussian_filter(X, M=8, axis=0):
    """Gaussian filter along the first axis of the feature matrix X."""
    for i in range(X.shape[axis]):
        if axis == 1:
            X[:, i] = filters.gaussian_filter(X[:, i], sigma=M / 2.)
        elif axis == 0:
            X[i, :] = filters.gaussian_filter(X[i, :], sigma=M / 2.)
    return X


def compute_gaussian_krnl(M):
    """Creates a gaussian kernel following Serra's paper."""
    g = signal.gaussian(M, M / 3., sym=True)
    G = np.dot(g.reshape(-1, 1), g.reshape(1, -1))
    G[M // 2:, :M // 2] = -G[M // 2:, :M // 2]
    G[:M // 2, M // 1:] = -G[:M // 2, M // 1:]
    return G


def embedded_space(X: np.ndarray, m: int) -> np.ndarray:
    """
    Creates an embedded space of the input sequence.

    Args:
        X (np.ndarray): Input sequence of shape (T, D) where T is the number of time steps and D is the feature dimension.
        m (int): Number of embedded dimensions.

    Returns:
        np.ndarray: Embedded sequence of shape (T - m + 1, D * m).
    
    Example:
        >>> X = np.array([[1, 2], [3, 4], [5, 6]])
        >>> embedded_space(X, 2)
        array([[1., 2., 3., 4.],
               [3., 4., 5., 6.]])
    """
    T, D = X.shape
    E = np.zeros((T - m + 1, D * m))
    for i in range(T - m + 1):
        E[i, :] = np.reshape(X[i:i + m, :], (1, D * m))
    return E


'''
def embedded_space(X: np.ndarray, m: int) -> np.ndarray:
    """Time-delay embedding with m dimensions and tau delays."""
    N = X.shape[0] - int(np.ceil(m))
    Y = np.zeros((N, int(np.ceil(X.shape[1] * m))))
    for i in range(N):
        # print X[i:i+m,:].flatten().shape, w, X.shape
        # print Y[i,:].shape
        rem = int((m % 1) * X.shape[1])  # Reminder for float m
        Y[i, :] = np.concatenate((X[i:i + int(m), :].flatten(),
                                 X[i + int(m), :rem]))
    return Y
'''


@jit(nopython=True)
def shift_matrix_circularly(X):
    """
    Shifts the matrix X circularly to get a time-lag matrix.

    Args:
    - X (np.array): Square matrix.

    Returns:
    - L (np.array): Time-lag matrix.

     Examples:
    --------
        X = np.array([[1, 2], [3, 4]])
        shift_matrix_circularly(X)
    array([[1., 4.],
           [3., 2.]])
    """
    N = X.shape[0]
    L = np.zeros(X.shape)
    for i in range(N):
        L[i, :] = np.asarray([X[(i + j) % N, j] for j in range(N)])
    return L


'''
def circular_shift(X):
    """Shifts circularly the X squre matrix in order to get a
        time-lag matrix."""
    N = X.shape[0]
    L = np.zeros(X.shape)
    for i in range(N):
        L[i, :] = np.asarray([X[(i + j) % N, j] for j in range(N)])
    return L
'''


def compute_novelty_curve(X):
    """
    Computes the novelty curve from the structural features using vectorized operations.

    Args:
    - X (np.array): Structural features.

    Returns:
    - nc (np.array): Novelty curve.

    Examples:
    --------
        X = np.array([[1, 2], [3, 4], [5, 6]])
        compute_novelty_curve(X)
    array([1., 1., 0.])
    """
    # Compute Euclidean distance between consecutive feature vectors
    diffs = np.diff(X, axis=0)
    nc = np.linalg.norm(diffs, axis=1)

    # Append a zero at the end to match the size of the original function's output
    nc = np.append(nc, 0)

    # Normalize the novelty curve to a range [0, 1]
    if nc.max() != 0:
        nc -= nc.min()
        nc /= nc.max()
    
    return nc


def find_peaks_adaptive_threshold(nc, L=16, offset_denom=0.1):
    """
    Obtain peaks from a novelty curve using an adaptive threshold.

    Args:
    - nc (np.array): Novelty curve.
    - L (int, optional): Size of the adaptive threshold for peak picking. Default is 16.
    - offset_denom (float, optional): Offset coefficient for adaptive thresholding. Default is 0.1.

    Returns:
    - peaks (list): List of peak positions.

     Examples:
    --------
        novelty_curve = np.array([0, 0.2, 0.5, 0.2, 0])
        pick_peaks(novelty_curve)
    [2]
    """
    
    # Compute the adaptive threshold using median filter and offset
    offset = nc.mean() * float(offset_denom)
    treshold = median_filter(nc, size=L) + offset
    peaks, _ = find_peaks(nc, height=treshold)
    return peaks


def compute_recurrence_matrix(E, k=0.04):
    """
    Compute the recurrence matrix using numpy's optimized linear algebra operations.

    A recurrence matrix provides a binary representation to identify repeated patterns 
    and structures in time series data. In such a matrix, the value 1 indicates that 
    the respective points in the time series recur, while a value of 0 indicates non-recurrence.

    This function constructs a recurrence matrix for the embedded matrix `E`. Point `i` in `E` 
    is recurrent with another point `j` if the Euclidean distance between them is among the 
    k smallest distances for point `i`.

    The matrix can be useful in multiple areas of time series analysis, including identifying 
    periodicities, detecting structural changes, and analyzing dynamic stability.

    Parameters:
    - E (np.array): Embedded matrix representation of the time series. Each row of `E` represents 
                    a point in the embedded space, while each column represents a dimension.
    - k (float, optional): Proportion to determine the k-nearest neighbors. For example, a value of 0.04 
                           implies considering the closest 4% of points. Default is 0.04.

    Returns:
    - R (np.array): The computed binary recurrence matrix. A value of 1 at position (i, j) indicates 
                    that points `i` and `j` are recurrent, and a value of 0 indicates non-recurrence.

    Steps:
    1. For each point `i` in `E`, compute the pairwise Euclidean distances to all other points 
       using numpy's `linalg.norm` method.
    2. Identify the k-nearest neighbors of point `i` by sorting the computed distances and selecting 
       the smallest `k` proportions.
    3. Construct the recurrence matrix by setting the positions of the nearest neighbors to 1, and 
       all other positions to 0.
    """
    N = E.shape[0]
    k_val = int(k * N)
    R = np.zeros((N, N), dtype=np.float32)
    
    for i in range(N):
        # Compute pairwise distances to all other points using numpy's optimized linear algebra operations
        distances = np.linalg.norm(E[i] - E, axis=1)
        
        # Find the k smallest distances
        k_smallest_indices = np.argpartition(distances, k_val)[:k_val]
        
        # Set the recurrence matrix values for these indices
        R[i, k_smallest_indices] = 1
    
    return R


if __name__ == '__main__':
    
    # 
    X = np.array([[1, 2], [3, 4], [5, 6]])
    print(embedded_space(X, m=2))
    X = np.array([[1, 2], [3, 4]])
    print(shift_matrix_circularly(X))