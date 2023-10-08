import numpy as np
import pandas as pd
import librosa
from math import log2


class LibrosaFeaturesExtractor:
    """
    Class for extracting audio features from audio data.
    """
    
    @staticmethod
    def get_key(freq):
        """
        Convert a frequency value to its corresponding musical key.

        Parameters:
            freq (float): Frequency value in Hertz.

        Returns:
            str: Corresponding musical key.
        """
        A4 = 440
        C0 = A4 * pow(2, -4.75)
        # key names using Helmholtz pitch notation
        name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        h = round(12 * log2(freq / C0))
        octave = h // 12
        n = h % 12
        return name[n] + str(octave)

    @staticmethod
    def get_pitch(y_harmonic, sample_rate, beats):
        """
        Calculate the pitch (chromagram) of a harmonic audio buffer.

        Parameters:
            y_harmonic (numpy.ndarray): Input harmonic audio buffer as a 1D numpy array.
            sample_rate (int): Sample rate of the audio buffer.
            beats (numpy.ndarray): Beat frames obtained from beat tracking.

        Returns:
            numpy.ndarray: Beat-synchronous chroma (pitch) values.
        """
        C = librosa.feature.chroma_cqt(y=y_harmonic, sr=sample_rate)
        C_sync = librosa.util.sync(C, beats, aggregate=np.median)
        return C_sync

    @staticmethod
    def get_average_pitch(pitch, confidences_thresh = 0.8):
        """
        Calculate the average pitch and key of an array of pitch values.

        Parameters:
            pitch (list): List of pitch values.
            confidences_thresh (float): Confidence threshold for determining whether a pitch value is valid. Default is 0.8.

        Returns:
            tuple: Tuple containing the average frequency and average key.
        """
        pitches = []
        i = 0
        while i < len(pitch):
            if pitch[i][2] > confidences_thresh:
                pitches.append(pitch[i][1])
            i += 1
        if len(pitches) > 0:
            average_frequency = np.array(pitches).mean()
            average_key = LibrosaFeaturesExtractor.get_key(average_frequency)
        else:
            average_frequency = 0
            average_key = "A0"
        return average_frequency, average_key

    @staticmethod
    def get_intensity(audio_data, sample_rate, beats):
        """
        Calculate the intensity (beat-synchronous loudness) of an audio buffer.

        Parameters:
            audio_data (numpy.ndarray): Input audio buffer as a 1D numpy array.
            sr (int): Sample rate of the audio buffer.
            beats (numpy.ndarray): Beat frames obtained from beat tracking.

        Returns:
            numpy.ndarray: Beat-synchronous intensity values.
        """
        CQT = librosa.cqt(y=audio_data, sr=sample_rate, fmin=librosa.note_to_hz('A1'))
        freqs = librosa.cqt_frequencies(CQT.shape[0], fmin=librosa.note_to_hz('A1'))
        perceptual_CQT = librosa.perceptual_weighting(CQT**2, freqs, ref=np.max)
        CQT_sync = librosa.util.sync(perceptual_CQT, beats, aggregate=np.median)
        
        return CQT_sync

    @staticmethod
    def get_timbre(audio_data, sample_rate, beats, n_mfcc=13, n_mels=128):
        """
        Calculate the timbre (MFCC) of an audio buffer.

        Parameters:
            audio_data (numpy.ndarray): Input audio buffer as a 1D numpy array.
            sr (int): Sample rate of the audio buffer.
            beats (numpy.ndarray): Beat frames obtained from beat tracking.
            n_mfcc (int): Number of MFCC coefficients to return. Default is 13.
            n_mels (int): Number of mel bands to generate. Default is 128.

        Returns:
            numpy.ndarray: Beat-synchronous MFCC (timbre) values.
        """
        # Calculate mel spectrogram of the audio buffer
        S = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate, n_mels=n_mels)

        # Convert to dB scale (decibels)
        log_S = librosa.power_to_db(S, ref=np.max)

        # Calculate MFCC (Mel-frequency cepstral coefficients)
        mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=n_mfcc)

        # Calculate delta and delta-delta MFCC (first and second-order differences)
        delta_mfcc = librosa.feature.delta(mfcc)
        delta2_mfcc = librosa.feature.delta(mfcc, order=2)

        # Stack MFCC, delta, and delta-delta to get the final timbre feature
        M = np.vstack([mfcc, delta_mfcc, delta2_mfcc])

        # Synchronize the MFCC frames with beat frames
        M_sync = librosa.util.sync(M, beats)

        return M_sync

    @staticmethod
    def get_segments(audio_data, sr):
        """
        Segment the audio data using librosa.

        Parameters:
            audio_data (numpy.ndarray): Input audio data.
            sr (int): Sample rate.

        Returns:
            tuple: Tuple containing the segment boundaries and segment labels.
        """
        # Calculate the onset strength
        onset_env = librosa.onset.onset_strength(y=audio_data, sr=sr)

        # Calculate the onset events
        onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)

        # Convert the onset frames to segment boundaries
        segment_boundaries = librosa.frames_to_time(frames=onset_frames, sr=sr)

        # Calculate the segment labels
        segment_labels = librosa.segment.agglomerative(data=onset_env, k=None, axis=0)

        return segment_boundaries, segment_labels

        
    @staticmethod
    def get_rhythm(y, sr):
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr)
        return tempogram

    @staticmethod
    def get_tonnetz(y, sr):
        return librosa.feature.tonnetz(y=y, sr=sr)

    @staticmethod
    def get_spectral_contrast(y, sr):
        return librosa.feature.spectral_contrast(y=y, sr=sr)

    @staticmethod
    def get_zero_crossing_rate(y):
        return librosa.feature.zero_crossing_rate(y)

    @staticmethod
    def scale_features(features):
        scaled_features = {}
        for key, value in features.items():
            scaled_value = (value - value.min()) / (value.max() - value.min())
            scaled_features[key] = scaled_value
        return scaled_features

    @staticmethod
    def save_features_to_parquet(features, file_name):
        df = pd.DataFrame(features)
        df.to_parquet(file_name)


if __name__ == "__main__":
    # This is a dummy demonstration for the newly added methods.
    demo_audio = librosa.tone(440, duration=5)
    sample_rate = 22050

    example_features = {
        "rhythm": LibrosaFeaturesExtractor.get_rhythm(demo_audio, sample_rate),
        "tonnetz": LibrosaFeaturesExtractor.get_tonnetz(demo_audio, sample_rate),
        "spectral_contrast": LibrosaFeaturesExtractor.get_spectral_contrast(demo_audio, sample_rate),
        "zero_crossing_rate": LibrosaFeaturesExtractor.get_zero_crossing_rate(demo_audio)
    }

    # Scaling the features
    scaled_features = LibrosaFeaturesExtractor.scale_features(example_features)

    scaled_features
