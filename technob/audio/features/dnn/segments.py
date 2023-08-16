
"""
Some of the code in this file is based on the code from the following repository:
https://github.com/wayne391/sf_segmenter
"""

import numpy as np
import librosa
from scipy import signal
from scipy.spatial import distance
from scipy.ndimage import filters

from miditoolkit.pianoroll import utils as mt_utils
from miditoolkit.midi import parser as mid_parser
from miditoolkit.pianoroll import parser as pr_parser
from technob.math_utils.misc import *


CONFIG = {
    "M_gaussian": 27,
    "m_embedded": 3,
    "k_nearest": 0.04,
    "Mp_adaptive": 28,
    "offset_thres": 0.05,
    "bound_norm_feats": np.inf  # min_max, log, np.inf,
                                # -np.inf, float >= 0, None
    # For framesync features
    # "M_gaussian"    : 100,
    # "m_embedded"    : 3,
    # "k_nearest"     : 0.06,
    # "Mp_adaptive"   : 100,
    # "offset_thres"  : 0.01
}


def audio_extract_pcp(
        audio, 
        sr,
        n_fft=4096,
        hop_len=int(4096 * 0.75),
        pcp_bins=84,
        pcp_norm=np.inf,
        pcp_f_min=27.5,
        pcp_n_octaves=6):

    audio_harmonic, _ = librosa.effects.hpss(audio)
    pcp_cqt = np.abs(librosa.hybrid_cqt(
                audio_harmonic,
                sr=sr,
                hop_length=hop_len,
                n_bins=pcp_bins,
                norm=pcp_norm,
                fmin=pcp_f_min)) ** 2

    pcp = librosa.feature.chroma_cqt(
                C=pcp_cqt,
                sr=sr,
                hop_length=hop_len,
                n_octaves=pcp_n_octaves,
                fmin=pcp_f_min).T
    return pcp


def midi_extract_beat_sync_pianoroll(
        pianoroll,
        beat_resol,
        is_tochroma=False):

    # sync to beat
    beat_sync_pr = np.zeros(
        (int(np.ceil(pianoroll.shape[0] /  beat_resol)),
         pianoroll.shape[1]))

    for beat in range(beat_sync_pr.shape[0]):
        st = beat * beat_resol
        ed = (beat + 1) * beat_resol
        beat_sync_pr[beat] = np.sum(pianoroll[st:ed, :], axis=0)
    
    # normalize
    beat_sync_pr = (
        beat_sync_pr - beat_sync_pr.mean()) / beat_sync_pr.std()
    beat_sync_pr = (
        beat_sync_pr - beat_sync_pr.min()) / (beat_sync_pr.max() - beat_sync_pr.min())

    # to chroma
    if is_tochroma:
        beat_sync_pr = mt_utils.tochroma(beat_sync_pr)
    return beat_sync_pr



def run_label(
        boundaries, 
        R,
        max_iter=100, 
        return_feat=False):

    """Labeling algorithm."""
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



def compute_novelty_curve(X, M=8, axis=0):
    """Computes the novelty curve from the structural features."""
    N = X.shape[0]
    # nc = np.sum(np.diff(X, axis=0), axis=1) # Difference between SF's

    nc = np.zeros(N)
    for i in range(N - 1):
        nc[i] = distance.euclidean(X[i, :], X[i + 1, :])

    # Normalize
    nc += np.abs(nc.min())
    nc /= float(nc.max())
    return nc


def pick_peaks(nc, L=16, offset_denom=0.1):
    """Obtain peaks from a novelty curve using an adaptive threshold."""
    offset = nc.mean() * float(offset_denom)
    th = filters.median_filter(nc, size=L) + offset
    #th = filters.gaussian_filter(nc, sigma=L/2., mode="nearest") + offset
    #import pylab as plt
    #plt.plot(nc)
    #plt.plot(th)
    #plt.show()
    # th = np.ones(nc.shape[0]) * nc.mean() - 0.08
    peaks = []
    for i in range(1, nc.shape[0] - 1):
        # is it a peak?
        if nc[i - 1] < nc[i] and nc[i] > nc[i + 1]:
            # is it above the threshold?
            if nc[i] > th[i]:
                peaks.append(i)
    return peaks


def circular_shift(X):
    """Shifts circularly the X squre matrix in order to get a
        time-lag matrix."""
    N = X.shape[0]
    L = np.zeros(X.shape)
    for i in range(N):
        L[i, :] = np.asarray([X[(i + j) % N, j] for j in range(N)])
    return L


class Segmenter(object):
    def __init__(self, config=CONFIG):
        """
        Initialize the Segmenter with configuration settings.
        
        Args:
            config (dict): A dictionary containing configuration parameters.
        """
        self.config = config
        self.refresh()

    def refresh(self):
        # collect feats
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

        # - res
        self.boundaries = None
        self.labs = None


    def proc_midi(self, path_midi, is_label=True):
        # parse midi to pianoroll
        midi_obj = mid_parser.MidiFile(path_midi)
        notes = midi_obj.instruments[0].notes
        pianoroll = pr_parser.notes2pianoroll(
                            notes)

        # pianoroll to beat sync pianoroll
        pianoroll_sync = midi_extract_beat_sync_pianoroll(
                pianoroll,
                midi_obj.ticks_per_beat)  

        return self.process(pianoroll_sync, is_label=is_label)

    def proc_audio(self, path_audio, sr=22050, is_label=True):
        y, sr = librosa.load(path_audio, sr=sr)
        pcp = audio_extract_pcp(y, sr)
        return self.process(pcp, is_label=is_label)

        
    def process(
            self, 
            F, 
            is_label=False):
        """Main process.
        Returns

        F: feature. T x D
        """
        self.refresh()

        # Structural Features params
        Mp = self.config["Mp_adaptive"]   # Size of the adaptive threshold for
                                          # peak picking
        od = self.config["offset_thres"]  # Offset coefficient for adaptive
                                          # thresholding
        M = self.config["M_gaussian"]     # Size of gaussian kernel in beats
        m = self.config["m_embedded"]     # Number of embedded dimensions
        k = self.config["k_nearest"]      # k*N-nearest neighbors for the
                                          # recurrence plot

        # Normalize
        F = normalize(F, norm_type=self.config["bound_norm_feats"])

        # Check size in case the track is too short
        if F.shape[0] > 20:
            # Emedding the feature space (i.e. shingle)
            E = embedded_space(F, m)
           
            # Recurrence matrix
            R = librosa.segment.recurrence_matrix(
                E.T,
                k=k * int(F.shape[0]),
                width=1,  # zeros from the diagonal
                metric="euclidean",
                sym=True).astype(np.float32)

            # Circular shift
            L = circular_shift(R)

            # Obtain structural features by filtering the lag matrix
            SF = gaussian_filter(L.T, M=M, axis=1)
            SF = gaussian_filter(SF, M=1, axis=0)

            # Compute the novelty curve
            nc = compute_novelty_curve(SF)

            # Find peaks in the novelty curve
            est_bounds = pick_peaks(nc, L=Mp, offset_denom=od)

            # Re-align embedded space
            est_bounds = np.asarray(est_bounds) + int(np.ceil(m / 2.))
        else:
            est_bounds = []

        # Add first and last frames
        est_idxs = np.concatenate(([0], est_bounds, [F.shape[0] - 1]))
        est_idxs = np.unique(est_idxs)

        assert est_idxs[0] == 0 and est_idxs[-1] == F.shape[0] - 1
        
        # collect  feature
        self.F = F
        self.E = E
        self.R = R
        self.L = L
        self.SF = SF
        self.nc = nc

        if is_label:
            labs, (S, S_trans, S_final) = run_label(
                est_idxs, 
                R,
                return_feat=True)

            self.S = S
            self.S_trans = S_trans
            self.S_final = S_final
            
            self.boundaries = est_idxs
            self.labs = labs
            return est_idxs, labs
        else:
            self.boundaries = est_idxs
            return est_idxs