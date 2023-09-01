'''
Segmenter: Audio and MIDI Segmentation Tool
===========================================

The Segmenter class is designed to automatically detect and segment boundaries in both audio and MIDI data. This 
documentation provides a comprehensive explanation of the tool, its methods, and the underlying algorithms used for 
segmentation.

Why segmentation?
-----------------
Segmentation is the process of dividing a continuous signal (like a song or a piece of music) into distinct sections 
or segments. These segments can correspond to musical events, changes in structure, or any other significant points 
in the signal. Identifying these segments can be crucial for various applications such as music analysis, structure 
visualization, and more.

How does it work?
-----------------
The segmentation process is based on the extraction of certain features from the audio or MIDI data, which are then 
analyzed to detect points of change or novelty. These points of novelty often correspond to segment boundaries.

Steps:
------
1. **Feature Extraction**:
    Before segmentation can begin, we need to extract relevant features from the audio or MIDI data. For audio data, 
    we extract the Pitch Class Profiles (PCP) which represent the distribution of musical pitches at a given time. 

    Why? Features like PCP capture the harmonic content of the audio, which can be useful in detecting boundaries 
    between segments with different harmonic structures.

    For MIDI, we synchronize the piano roll representation to beats.
    Why? Synchronizing the piano roll to beats helps in aligning the MIDI data with the audio, making it easier to 
    compare the two.

    Example: Imagine a simple piano piece transitioning from C major to G major. The PCP will show peaks at C, E, and G 
    for the C major part and peaks at G, B, and D for the G major part.

2. **Embedding**:
    The feature space is embedded to capture more structural information. This is achieved by taking each feature 
    vector and its neighboring feature vectors to create a higher dimensional representation. Embedding is similar to 
    building a projection matrix in singular spectrum analysis. 

    Why? Embedding helps in capturing the context around each feature vector, making the novelty detection more robust.

    Example: For a melody going "C-D-E", instead of treating each note individually, embedding might consider "C-D", 
    "D-E", and "E-F" as features.

3. **Recurrence Matrix Calculation**:
    A recurrence matrix represents the similarity between different points in the feature sequence. It's a way to 
    visualize repeating patterns in the data.

    Why? Musical pieces often have repeating sections. The recurrence matrix helps in highlighting these repetitions.

    Example: For a song with a repeating chorus, the recurrence matrix will show bright squares at the positions where 
    the chorus repeats.

4. **Time-Lag Representation**:
    The recurrence matrix is transformed into a time-lag representation. This step focuses on capturing the diagonal 
    structures in the matrix, which represent repeating patterns.

    Why? Emphasizing these diagonal structures makes it easier to detect boundaries between different segments.

    Example: In the transformed matrix, the start and end of a repeating chorus might be represented by strong diagonal 
    lines.

5. **Structural Feature Extraction**:
    We apply a Gaussian filter to the time-lag representation to extract structural features. These features capture 
    the novelty or change in the data.

    Why? Changes or novelties in these features often correspond to segment boundaries.

    Example: If there's a sudden change from a verse to a chorus, this step will highlight that transition as a peak 
    or point of novelty.

6. **Boundary Detection**:
    Using the structural features, we compute a novelty curve which represents the degree of change at each point 
    in the data. Peaks in this curve are detected as segment boundaries.

    Why? Peaks in the novelty curve represent points of significant change in the data, making them good candidates 
    for segment boundaries.

    Example: In the novelty curve, a peak might appear at the exact point where a verse transitions to a chorus, 
    marking it as a potential boundary.

7. **Labeling (optional)**:
    After detecting the boundaries, an optional step is to label each segment based on its content or structure.

How can you adapt the parameters?
---------------------------------
Several parameters can be adjusted to fine-tune the segmentation process:

- `peak_finder_threshold`: Controls the adaptive threshold for peak picking. Increasing it might result in more 
  boundaries being detected.
- `offset_denom`: An offset coefficient for adaptive thresholding. Adjusting it can shift the threshold up or down.
- `guassian_kernel_size`: Determines the size of the Gaussian kernel used in filtering. A larger size might smooth 
  out smaller changes. -> We seem to be very sensitive to this parameter. 
- `embedded_dimensions`: The number of embedded dimensions can influence the context captured. More dimensions might 
  capture a wider context.
- `k_nearest`: Determines the number of nearest neighbors for the recurrence plot. Adjusting it can make the recurrence 
  plot denser or sparser.
- `bound_norm_feats`: Determines the type of normalization for features. Different norms can emphasize different 
  aspects of the data.

Future Improvements and Expressiveness:
---------------------------------------
1. **Adaptive Gaussian Kernel**: Instead of using a fixed Gaussian kernel size, an adaptive approach that varies the 
   kernel size based on local characteristics might be beneficial.
2. **Alternative Feature Representations**: While PCP is a robust feature for harmonic content, exploring other 
   feature representations like Mel-frequency cepstral coefficients (MFCCs) or Chroma might yield different results.
3. **Deep Learning Approaches**: Modern deep learning architectures, especially those designed for sequence data like 
   RNNs or Transformers, can be explored for segmentation tasks.
4. **Post-processing**: After detecting boundaries, a post-processing step to merge closely spaced boundaries or 
   refine boundary positions might improve accuracy.

Remember, segmentation is both a science and an art. While the algorithm does its best to detect boundaries, the 
perception of musical segments can be subjective. Always trust your ears and intuition!


Computational Time Analysis and Efficiency Recommendations:
==========================================================

The segmentation process involves multiple steps, each contributing to the overall computational time. Below, we break 
down the major computational steps and provide recommendations for improving efficiency:

1. **Feature Extraction**:
    Computational Time: Moderate to High (especially for audio data due to FFT operations in PCP extraction)
    Recommendations:
    - Use a smaller FFT window size for faster computation at the cost of frequency resolution.
    - Consider caching frequently used audio features.

2. **Embedding**:
    Computational Time: Low to Moderate (depends on the dimensions and length of feature sequences)
    Recommendations:
    - Use efficient algorithms or libraries for matrix operations.
    - Reduce the embedded dimensions if precision isn't critical.

3. **Recurrence Matrix Calculation**:
    Computational Time: High (involves pairwise distance computations)
    Recommendations:
    - Consider using `numba` or `Cython` to speed up the distance computations.
    - Use approximate nearest neighbors algorithms to reduce computational time.

4. **Time-Lag Representation and Structural Feature Extraction**:
    Computational Time: Moderate (mostly matrix operations)
    Recommendations:
    - Use optimized libraries like `numpy` or `scipy` for matrix operations.
    - Consider parallelizing operations with tools like `Dask`.

5. **Boundary Detection**:
    Computational Time: Low (finding peaks in a 1D array)
    Recommendations:
    - Use efficient peak finding algorithms.

6. **Labeling (optional)**:
    Computational Time: Moderate (iterative matrix multiplications)
    Recommendations:
    - Vectorize matrix operations where possible.
    - Consider using `numba` for optimizing the labeling algorithm.

Overall Recommendations:
------------------------
- **Vectorization**: Many operations, especially matrix computations, can benefit from vectorization. Ensure that 
  operations are vectorized using `numpy` or similar libraries to leverage fast C/Fortran backends.
  
- **Parallelization**: For systems with multiple cores, parallelizing certain steps, especially the recurrence matrix 
  calculation, can offer significant speed-ups.
  
- **Use JIT Compilation**: Tools like `numba` can significantly speed up loops and mathematical computations by using 
  Just-In-Time (JIT) compilation.
  
- **Optimized Libraries**: Libraries like `scipy` and `numpy` are highly optimized and should be used wherever possible.

- **Algorithmic Improvements**: Consider researching advanced algorithms or approximations that might speed up 
  computationally intensive steps.

By incorporating the above recommendations, it's possible to achieve a balance between computational time and 
segmentation accuracy, making the tool more suitable for real-time applications or processing large datasets.

'''
"""
Some of the code in this file is based on the code from the following repository:
https://github.com/wayne391/sf_segmenter
"""

import numpy as np
import librosa

from miditoolkit.pianoroll import utils as mt_utils
from miditoolkit.midi import parser as mid_parser
from miditoolkit.pianoroll import parser as pr_parser
from technob.math.utils import gaussian_filter, embedded_space, compute_novelty_curve, find_peaks_adaptive_threshold, shift_matrix_circularly, normalize, cummulative_sum_Q, compute_recurrence_matrix


def audio_extract_pcp(audio, sr, n_fft=4096, hop_len=int(4096 * 0.75),
                      pcp_bins=84, pcp_norm=np.inf, pcp_f_min=27.5,
                      pcp_n_octaves=6):
    """
    Extract Pitch Class Profiles (PCP) from audio.

    Args:
    - audio (np.array): Audio waveform.
    - sr (int): Sample rate of the audio.
    - n_fft (int, optional): FFT size. Default is 4096.
    - hop_len (int, optional): Hop length. Default is 75% of n_fft.
    - pcp_bins (int, optional): Number of bins for PCP. Default is 84.
    - pcp_norm (float, optional): Norm value for PCP. Default is infinity.
    - pcp_f_min (float, optional): Minimum frequency for PCP. Default is 27.5Hz.
    - pcp_n_octaves (int, optional): Number of octaves for PCP. Default is 6.

    Returns:
    - pcp (np.array): Extracted Pitch Class Profiles.
    """

    # Separate harmonic component from audio
    audio_harmonic, _ = librosa.effects.hpss(audio)

    # Compute Constant-Q transform of the harmonic component
    pcp_cqt = np.abs(librosa.hybrid_cqt(audio_harmonic, sr=sr, hop_length=hop_len,
                                        n_bins=pcp_bins, norm=pcp_norm, fmin=pcp_f_min)) ** 2

    # Compute PCP from the CQT
    pcp = librosa.feature.chroma_cqt(C=pcp_cqt, sr=sr, hop_length=hop_len,
                                     n_octaves=pcp_n_octaves, fmin=pcp_f_min).T

    return pcp


def midi_extract_beat_sync_pianoroll(pianoroll, beat_resol, is_tochroma=False):
    """
    Synchronize the given piano roll (MIDI representation) to beats.

    Args:
    - pianoroll (np.array): Piano roll representation of MIDI.
    - beat_resol (int): Resolution of beats.
    - is_tochroma (bool, optional): If True, convert pianoroll to chroma. Default is False.

    Returns:
    - beat_sync_pr (np.array): Beat synchronized piano roll.
    """

    # Initialize beat synchronized piano roll
    beat_sync_pr = np.zeros((int(np.ceil(pianoroll.shape[0] / beat_resol)), pianoroll.shape[1]))

    # Synchronize to beats
    for beat in range(beat_sync_pr.shape[0]):
        st = beat * beat_resol
        ed = (beat + 1) * beat_resol
        beat_sync_pr[beat] = np.sum(pianoroll[st:ed, :], axis=0)

    # Normalize the synchronized piano roll
    beat_sync_pr = (beat_sync_pr - beat_sync_pr.mean()) / beat_sync_pr.std()
    beat_sync_pr = (beat_sync_pr - beat_sync_pr.min()) / (beat_sync_pr.max() - beat_sync_pr.min())

    # Convert to chroma if specified
    if is_tochroma:
        beat_sync_pr = mt_utils.tochroma(beat_sync_pr)

    return beat_sync_pr




def run_label(boundaries, R, max_iter=100, return_feat=False):
    """
    Labeling algorithm for audio segments.

    Args:
        boundaries (np.ndarray): Segment boundaries.
        R (np.ndarray): Recurrence matrix.
        max_iter (int, optional): Maximum iterations for label convergence. Defaults to 100.
        return_feat (bool, optional): Return features along with labels. Defaults to False.

    Returns:
        np.ndarray: Labels for each segment.
    """
    n_boundaries = len(boundaries)
    
    # compute S
    S = np.zeros((n_boundaries, n_boundaries))
    for i in range(n_boundaries - 1):
        for j in range(n_boundaries - 1):
            i_st, i_ed = boundaries[i], boundaries[i+1]
            j_st, j_ed = boundaries[j], boundaries[j+1]

            len_i = i_ed - i_st
            len_j = j_ed - j_st
            score = cummulative_sum_Q(R[i_st:i_ed, j_st:j_ed])
            S[i, j] = score / min(len_i, len_j)    
    
    # threshold
    thr = np.std(S) + np.mean(S)
    S[S <= thr] = 0       
    
    # iteration
    S_trans = S.copy()
    
    for i in range(max_iter):
        S_trans = np.matmul(S_trans, S)
        
    S_final = S_trans > 1
    
    # proc output
    n_seg = len(S_trans) - 1
    labs = np.ones(n_seg) * -1
    cur_tag = int(-1)
    for i in range(n_seg):
        print(' >', i)
        if labs[i] == -1:
            cur_tag += 1
            labs[i] = cur_tag
            for j in range(n_seg):
                if S_final[i, j]:
                    labs[j] = cur_tag
    
    if return_feat:
        return labs, (S, S_trans, S_final)
    else:
        return labs


class Segmenter(object):
    def __init__(self, peak_finder_threshold=100, offset_denom=0.1, guassian_kernel_size=100, embedded_dimensions=30, k_nearest=0.04, bound_norm_feats=np.inf):
        """
        Initialize the Segmenter with configuration settings. We seem to be sensitive to the hyperparameters, especially the guassian_kernel_size, peak_finder_threshold, and offset_denom, and embedded_dimensions.
        
        Args:
            peak_finder_threshold (int, optional): Size of the adaptive threshold for peak picking. Defaults to 100.
            offset_denom (float, optional): Offset coefficient for adaptive thresholding. Defaults to 0.1.
            guassian_kernel_size (int, optional): Size of gaussian kernel in beats. Defaults to 100.
            embedded_dimensions (int, optional): Number of embedded dimensions. Defaults to 30.
            k_nearest (float, optional): k*N-nearest neighbors for the recurrence plot. Defaults to 0.04.
            bound_norm_feats (str, optional): Normalization type for features. Defaults to np.inf.

        Returns:
            Segmenter: Initialized Segmenter object.
        """
        # set params 
        self.peak_finder_threshold = peak_finder_threshold  # Size of the adaptive threshold for peak picking
        self.offset_denom = offset_denom  # Offset coefficient for adaptive thresholding
        self.guassian_kernel_size = guassian_kernel_size  # Size of gaussian kernel in beats
        self.embedded_dimensions = embedded_dimensions  # Number of embedded dimensions
        self.k_nearest = k_nearest  # k*N-nearest neighbors for the recurrence plot
        self.bound_norm_feats = bound_norm_feats  # Normalization type for features
       
        self.refresh()

    def refresh(self):
        """Reset all stored features and results."""
        # - segmentation
        self.F = None
        self.E = None
        self.R = None
        self.L = None
        self.SF = None
        self.nc = None

        # - labeling
        self.S = None
        self.S_trans = None
        self.S_final = None

        # - results
        self.boundaries = None
        self.labs = None
        
    def process(self, F, return_labels=False):
        """
        Main segmentation process using provided features.
        
        Args:
            F (np.ndarray): Features for segmentation.
            return_labels (bool, optional): Whether to return segment labels. Defaults to False.
            
        Returns:
            tuple: Segment boundaries and labels.
        """
        self.refresh()

        # Parameters for structural features
        Mp = self.peak_finder_threshold
        od = self.offset_denom
        M = self.guassian_kernel_size
        m = self.embedded_dimensions
        k = self.k_nearest
        norm_type = self.bound_norm_feats

        # Normalize the features
        F = normalize(F, norm_type=norm_type)

        # Check if the track is not too short
        if F.shape[0] > 20:
            # Embed the feature space (shingle)
            E = embedded_space(F, m)
            
            # Compute the recurrence matrix
            #R = librosa.segment.recurrence_matrix(E.T, k=k * int(F.shape[0]), width=1, metric="euclidean", sym=True).astype(np.float32)
            # This is a faster implementation of the recurrence matrix
            R = compute_recurrence_matrix(E, k=k)
            # Obtain a time-lag representation
            L = shift_matrix_circularly(R)

            # Filter the lag matrix to get structural features
            SF = gaussian_filter(L.T, M=M, axis=1)
            SF = gaussian_filter(SF, M=1, axis=0)

            # Compute the novelty curve from structural features
            nc = compute_novelty_curve(SF)

            # Detect boundaries from the novelty curve
            est_bounds = find_peaks_adaptive_threshold(nc, L=Mp, offset_denom=od)

            # Adjust the boundaries for the embedded space
            est_bounds = np.asarray(est_bounds) + int(np.ceil(m / 2.))
        else:
            est_bounds = []

        # Include the start and end as boundaries
        est_idxs = np.concatenate(([0], est_bounds, [F.shape[0] - 1]))
        est_idxs = np.unique(est_idxs)

        assert est_idxs[0] == 0 and est_idxs[-1] == F.shape[0] - 1
        
        # Store the features for later use
        self.F = F
        self.E = E
        self.R = R
        self.L = L
        self.SF = SF
        self.nc = nc

        # If labels are requested, compute and return them
        if return_labels:
            labs, (S, S_trans, S_final) = run_label(est_idxs, R, return_feat=True)
            self.S = S
            self.S_trans = S_trans
            self.S_final = S_final
            
            self.boundaries = est_idxs
            self.labs = labs
            return est_idxs, labs
        else:
            self.boundaries = est_idxs
            return est_idxs, None

    def convert_frame_boundaries_to_time(self, boundaries, sr=22050, hop_length=512):
        """
        Convert frame boundaries to time (seconds).
        
        Args:
            boundaries (list): List of frame boundaries.
            sr (int, optional): Sampling rate for audio loading. Defaults to 22050.
            hop_length (int, optional): Hop length for audio loading. Defaults to 512.
            
        Returns:
            list: List of boundaries in time (seconds).
        """
        boundaries = [boundary * hop_length / sr for boundary in boundaries]
        
        return boundaries
    
    def process_midi(self, path_midi, return_labels=True, time_boundaries=False, hop_length=int(4096 * 0.75)):
        """
        Process MIDI file for segmentation.
        
        Args:
            path_midi (str): Path to the MIDI file.
            return_labels (bool, optional): Whether to return segment labels. Defaults to True.
            time_boundaries (bool, optional): Whether to return boundaries in time (seconds). Defaults to False.
            
        Returns:
            tuple: Segment boundaries and labels.
        """
        # Parse MIDI to get a piano roll representation
        midi_obj = mid_parser.MidiFile(path_midi)
        notes = midi_obj.instruments[0].notes
        pianoroll = pr_parser.notes2pianoroll(notes)

        # Convert the piano roll to beat synchronized representation
        pianoroll_sync = midi_extract_beat_sync_pianoroll(pianoroll, midi_obj.ticks_per_beat)  

        # Process the beat synchronized piano roll
        boundaries, labels = self.process(pianoroll_sync, return_labels=return_labels)
        if time_boundaries:
            boundaries = self.convert_frame_boundaries_to_time(boundaries, sr=midi_obj.sr, hop_length=hop_length)

        return boundaries, labels

    def process_audio(self, audio_data, sr=22050, return_labels=True, time_boundaries=False, hop_length=int(4096 * 0.75)):
        """
        Process audio file for segmentation.
        
        Args:
            path_audio (str): Path to the audio file.
            sr (int, optional): Sampling rate for audio loading. Defaults to 22050.
            return_labels (bool, optional): Whether to return segment labels. Defaults to True.
            time_boundaries (bool, optional): Whether to return boundaries in time (seconds). Defaults to False.
            
        Returns:
            tuple: Segment boundaries and labels.
        """
        pcp = audio_extract_pcp(audio_data, sr, hop_len=hop_length)

        boundaries, labels = self.process(pcp, return_labels=return_labels)
        if time_boundaries:
            boundaries = self.convert_frame_boundaries_to_time(boundaries, sr=sr, hop_length=hop_length)
        
        return boundaries, labels


if __name__ == "__main__":
    
    # Process an audio file to obtain segment boundaries and labels
    audio_path = "technob/docs/examples/cse.WAV"
    audio_data, sr = librosa.load(audio_path)
    
    # TRACK THE RUNTIME

    import time
    start = time.time()
    # Initialize the segmenter 
    segmenter = Segmenter(peak_finder_threshold=100, offset_denom=.1, guassian_kernel_size=100, embedded_dimensions=30, k_nearest=0.04, bound_norm_feats=np.inf)
    boundaries, labels = segmenter.process_audio(audio_data, sr=sr, return_labels=False, time_boundaries=True)
    end = time.time()
    # transform boundaries in seconds to mm:ss format
    import datetime
    boundaries = [str(datetime.timedelta(seconds=boundary)) for boundary in boundaries]
    print(boundaries)  # This will output the segment boundaries in seconds

    print(f"Runtime: {end - start} seconds")
