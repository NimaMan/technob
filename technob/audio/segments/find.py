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
The current feature extraction method is much costlier in comparison to the other steps.
Using some other features may result in the other parts of the algorithm becoming the bottleneck.
This is left as a future improvement.

Source paper: 
J. Serrà, M. Müller, P. Grosche and J. L. Arcos, "Unsupervised Music Structure Annotation by Time Series Structure Features and Segment Similarity," in IEEE Transactions on Multimedia, vol. 16, no. 5, pp. 1229-1240, Aug. 2014, doi: 10.1109/TMM.2014.2310701.

Similar implementations:
https://github.com/wayne391/sf_segmenter
'''


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


class AudioSegmenter(object):
    def __init__(self, adaptive_threshold_size=100, offset_coefficient=0.1, gaussian_filter_size=100, embedding_dimension=30, nearest_neighbors_fraction=0.04, feature_normalization=np.inf):
        """
        Initialize the AudioSegmenter with configuration settings.
        Args:
            adaptive_threshold_size (int, optional): Size of the adaptive threshold for peak picking. Defaults to 100.
            offset_coefficient (float, optional): Offset coefficient for adaptive thresholding. Defaults to 0.1.
            gaussian_filter_size (int, optional): Size of gaussian filter in beats. Defaults to 100.
            embedding_dimension (int, optional): Number of embedding dimensions. Defaults to 30.
            nearest_neighbors_fraction (float, optional): Fraction of nearest neighbors for the recurrence plot. Defaults to 0.04.
            feature_normalization (str, optional): Normalization type for features. Defaults to np.inf.
        Returns:
            AudioSegmenter: Initialized AudioSegmenter object.
        """
        # Set hyperparameters
        self.adaptive_threshold_size = adaptive_threshold_size
        self.offset_coefficient = offset_coefficient
        self.gaussian_filter_size = gaussian_filter_size
        self.embedding_dimension = embedding_dimension
        self.nearest_neighbors_fraction = nearest_neighbors_fraction
        self.feature_normalization = feature_normalization
       
        self.reset_internal_states()

    def reset_internal_states(self):
        """Clear all stored features and results."""
        self.features = None
        self.embedded_features = None
        self.recurrence_matrix = None
        self.time_lag_matrix = None
        self.structural_features = None
        self.novelty_curve = None

        # Labeling
        self.segment_matrix = None
        self.transformed_segment_matrix = None
        self.final_segment_matrix = None

        # Results
        self.segment_boundaries = None
        self.segment_labels = None
    
    def embed_feature_space(self, F):
        m = self.embedding_dimension
        E = embedded_space(F, m)
        return E

    def compute_recurrence_matrix(self, E):
        # Compute the recurrence matrix
        k = self.nearest_neighbors_fraction
        #R = librosa.segment.recurrence_matrix(E.T, k=k * int(F.shape[0]), width=1, metric="euclidean", sym=True).astype(np.float32)
        # This is a faster implementation of the recurrence matrix
        R = compute_recurrence_matrix(E, k=k)
        return R
            
    def compute_time_lag_representation(self, R):
        # Obtain a time-lag representation
        L = shift_matrix_circularly(R)
        return L
        
    def filter_structural_features(self, L):
        # Filter the lag matrix to get structural features
        M = self.gaussian_filter_size
        SF = gaussian_filter(L.T, M=M, axis=1)
        SF = gaussian_filter(SF, M=1, axis=0)
        return SF
    
    def compute_novelty_from_features(self, SF):
        # Compute the novelty curve from structural features
        nc = compute_novelty_curve(SF)
        return nc
        
    def detect_segment_boundaries(self, nc):
        # Detect boundaries from the novelty curve
        Mp = self.adaptive_threshold_size
        od = self.offset_coefficient
        est_bounds = find_peaks_adaptive_threshold(nc, L=Mp, offset_denom=od)
        return est_bounds 
        
    def adjust_boundaries(self, est_bounds):
        """
        Adjusts the detected segment boundaries to align with the original time series context.

        When embedding the feature space to higher dimensions, the effective size of the time series 
        is reduced by the embedding dimensions. As a result, the boundaries detected in this embedded 
        space are offset from the original time series context. This method corrects the boundary 
        indices to ensure they align correctly with the original time series.

        Parameters:
        - est_bounds (list): List of detected segment boundaries in the embedded feature space.

        Returns:
        - list: Adjusted segment boundaries that align with the original time series context.

        Example:
        --------
        If the embedding dimension is 2, then a boundary detected at index 5 in the embedded space 
        would be adjusted to index 6 in the original time series context.
        """
        m = self.embedding_dimension
        est_bounds = np.asarray(est_bounds) + int(np.ceil(m / 2.))
        # Include the start and end as boundaries
        est_idxs = np.concatenate(([0], est_bounds, [self.feature_shape[0] - 1]))
        est_idxs = np.unique(est_idxs)

        assert est_idxs[0] == 0 and est_idxs[-1] == self.feature_shape[0] - 1
        
        return est_bounds
    
    def label_segments(self, R, est_bounds):
        """
        Label segments based on the recurrence matrix and detected boundaries.

        Parameters:
        - R (np.ndarray): Recurrence matrix.
        - est_bounds (list): List of detected segment boundaries.

        Returns:
        - list: List of segment labels.
        """
        labs, = run_label(est_bounds, R)
        return labs

    def segment_features(self, F, include_labels=False):
        self.reset_internal_states()
        
        # Normalize the features
        F = normalize(F, norm_type=self.feature_normalization)
        
        if F.shape[0] > 20:
            self.E = self.embed_feature_space(F)
            self.R = self.compute_recurrence_matrix(self.E)
            self.L = self.compute_time_lag_representation(self.R)
            self.SF = self.filter_structural_features(self.L)
            self.nc = self.compute_novelty_from_features(self.SF)
            est_bounds = self.detect_segment_boundaries(self.nc)
            est_bounds = self.adjust_boundaries(est_bounds)
        else:
            est_bounds = []

        self.boundaries = est_bounds
        if include_labels:
            self.labs = self.label_segments(self.R, est_bounds)
            return est_bounds, self.labs
        return est_bounds, None

    def convert_boundaries_to_time_format(self, boundaries, sr=22050, hop_length=512):
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
    
    def segment_midi_file(self, path_midi, include_labels=True, time_boundaries=False, hop_length=int(4096 * 0.75)):
        """
        Process MIDI file for segmentation.
        
        Args:
            path_midi (str): Path to the MIDI file.
            include_labels (bool, optional): Whether to return segment labels. Defaults to True.
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
        boundaries, labels = self.segment_features(pianoroll_sync, include_labels=include_labels)
        if time_boundaries:
            boundaries = self.convert_boundaries_to_time_format(boundaries, sr=midi_obj.sr, hop_length=hop_length)

        return boundaries, labels

    def segment_from_audio_data(self, audio_data, sr=22050, include_labels=True, convert_to_time=True, hop_length=int(4096 * 0.75)):
        """
        Segment an audio waveform.
        Args:
            audio_data (np.array): Audio waveform.
            sr (int, optional): Sample rate. Defaults to 22050.
            include_labels (bool, optional): If True, segment labels are returned. Defaults to True.
            convert_to_time (bool, optional): If True, segment boundaries are converted to time (seconds). Defaults to False.
            hop_length (int, optional): Hop length for feature extraction. Defaults to int(4096 * 0.75).
        Returns:
            tuple: Segment boundaries and optionally labels.
        """
        pcp_features = audio_extract_pcp(audio_data, sr, hop_len=hop_length)
        self.feature_shape = pcp_features.shape
        boundaries, labels = self.segment_features(pcp_features, include_labels=include_labels)
        if convert_to_time:
            boundaries = self.convert_boundaries_to_time_format(boundaries, sr=sr, hop_length=hop_length)
        return boundaries, labels


if __name__ == "__main__":
    
    # Process an audio file to obtain segment boundaries and labels
    audio_path = "technob/docs/examples/cse.WAV"
    audio_data, sr = librosa.load(audio_path)
    
    # TRACK THE RUNTIME

    import time
    start = time.time()
    # Initialize the segmenter 
    segmenter = AudioSegmenter(adaptive_threshold_size=100, offset_coefficient=0.1, gaussian_filter_size=100, embedding_dimension=30, nearest_neighbors_fraction=0.04, feature_normalization=np.inf)
    boundaries, labels = segmenter.segment_from_audio_data(audio_data, sr=sr, include_labels=False, convert_to_time=True)
    end = time.time()
    # transform boundaries in seconds to mm:ss format
    import datetime
    boundaries = [str(datetime.timedelta(seconds=boundary)) for boundary in boundaries]
    print(boundaries)  # This will output the segment boundaries in seconds

    print(f"Runtime: {end - start} seconds")
