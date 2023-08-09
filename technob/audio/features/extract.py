import numpy as np
import librosa
from math import log2
from .utils import ProcessorUtils


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
        name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        h = round(12 * log2(freq / C0))
        octave = h // 12
        n = h % 12
        return name[n] + str(octave)

    @staticmethod
    def get_pitch_librosa(y_harmonic, sample_rate, beats):
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

        

class Extractor:
    # TODO: Complete the class 
    """
    Class Uage: This class will be used for extracting features
    """
    def __init__(self, audio_file_path, file_id, extract_midi=False):
        self.processor = ProcessorUtils(bit_depth=16, default_silence_threshold=-80.8)
        self.audio_file_path = audio_file_path
        self.file_id = file_id
        self.extract_midi = extract_midi

        self.audio_data, self.sample_rate = librosa.load(self.audio_file_path, sr=None)
        self.song_duration = librosa.get_duration(y=self.audio_data, sr=self.sample_rate)

    def get_audio_features(self, audio_file, file_id, extract_midi=False):
        """Extract various audio features from the given audio file.

        This analyzes the audio to extract different qualities like timbre,
        pitch, intensity etc. Useful for analyzing and comparing songs.

        Args:
            audio_file (str): Path to the audio file. 
            file_id (str): ID to identify the file.
            extract_midi (bool): Whether to extract MIDI data.

        Returns:
            dict: Dictionary containing the extracted audio features.
        """
        audio_data, sample_rate = self.audio_data, self.sample_rate

        print("1/8 Segment the audio")
        segments_boundaries, segments_labels = self.dnn_features.get_segments(self.audio_file_path)
        
        print("2/8 Extract pitch over time")        
        frequency_frames = self.dnn_features.get_pitch(audio_data, sample_rate)
        avg_pitch, key = self.features.get_average_pitch(frequency_frames)

        print("3/8 Separate harmonic and percussive")
        y_harmonic, y_percussive = librosa.effects.hpss(audio_data)
        
        print("4/8 Track beats")
        onset_env = librosa.onset.onset_strength(y=y_percussive, sr=sample_rate)
        tempo, beats = librosa.beat.beat_track(sr=sample_rate, onset_envelope=onset_env, trim=False)
        
        # TODO: 3 and 4 are also present in the quantizer
         
        print("5.1/8 Extract features beat-synchronously")
        CQT_sync = self.features.get_intensity(audio_data, sample_rate, beats)
        M_sync = self.features.get_timbre(audio_data, sample_rate, beats)
        C_sync = self.features.get_pitch_librosa(y_harmonic, sample_rate, beats)

        print('5.2 Aggregate features')
        intensity_frames = np.matrix(CQT_sync).getT()
        pitch_frames = np.matrix(C_sync).getT()
        timbre_frames = np.matrix(M_sync).getT()

        print("6/8 Get loudness, volume and trim silence")
        volume, avg_volume, loudness = self.processor.get_volume(self.audio_file)
        
        print("7/8 Extract stems")      
        destination = self.audio_file_path
        model_name = 'htdemucs_6s'
        self.dnn_features.extract_stems(destination, model_name)

        if extract_midi:
            print("8/8 Extract MIDI data")

        # Aggregate features
        features = {
            "id": file_id,
            "duration": self.song_duration,
            "tempo": tempo,
            "timbre": np.mean(timbre_frames),
            "timbre_frames": timbre_frames,
            "pitch": np.mean(pitch_frames),
            "pitch_frames": pitch_frames,
            "intensity": np.mean(intensity_frames),
            "intensity_frames": intensity_frames,
            "loudness": loudness,
            "volume": volume,
            "avg_volume": avg_volume,
            "key": key,
            "beats": librosa.frames_to_time(beats, sr=sample_rate),
            "segments_boundaries": segments_boundaries,
            "segments_labels": segments_labels,
            "frequency_frames": frequency_frames,
            "frequency": avg_frequency,
        }

        return features    


