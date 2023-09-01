
import librosa
import numpy as np
import os
from technob.audio.features.utils import ProcessorUtils
from technob.audio.features.librosa_features import LibrosaFeaturesExtractor

class Extractor:
    """
    Class Usage: This class will be used for extracting features from audio files.
    """
    def __init__(self, audio_file, sample_rate=None, extract_midi=False, verbose=True, extractor="librosa"):
        if isinstance(audio_file, str):
            self.audio_file_path = audio_file
            self.audio_data, self.sample_rate = librosa.load(self.audio_file_path, sr=None)
        elif isinstance(audio_file, np.ndarray):
            self.audio_file_path = None 
            self.audio_data = audio_file
            self.sample_rate = sample_rate

        self.processor = ProcessorUtils(bit_depth=16, default_silence_threshold=-80.8)
        self.extract_midi = extract_midi
        self.verbose = verbose

        self.song_duration = librosa.get_duration(y=self.audio_data, sr=self.sample_rate)
        if extractor == "librosa":
            self.features = LibrosaFeaturesExtractor()  # Using Librosa as the default extractor
        else:
            raise NotImplementedError(f"Extractor {extractor} is not implemented.")

    def _log(self, message):
        """Helper function to print messages only if verbose mode is on."""
        if self.verbose:
            print(message)

    def set_feature_extractor(self, extractor):
        """Set a different feature extractor if needed."""
        self.features = extractor

    def extract(self):
        """Main function to extract audio features."""
        try:
            self._log("1/8 Segment the audio")
            #segments_boundaries, segments_labels = self.features.get_segments(self.audio_data, self.sample_rate)
            
            self._log("2/8 Extract pitch over time")
            frequency_frames = self.features.get_pitch(self.audio_data, self.sample_rate)
            avg_pitch, key = self.features.get_average_pitch(frequency_frames)

            self._log("3/8 Separate harmonic and percussive")
            y_harmonic, y_percussive = librosa.effects.hpss(self.audio_data)
            
            self._log("4/8 Track beats")
            onset_env = librosa.onset.onset_strength(y=y_percussive, sr=self.sample_rate)
            tempo, beats = librosa.beat.beat_track(sr=self.sample_rate, onset_envelope=onset_env, trim=False)
            
            self._log("5.1/8 Extract features beat-synchronously")
            CQT_sync = self.features.get_intensity(self.audio_data, self.sample_rate, beats)
            M_sync = self.features.get_timbre(self.audio_data, self.sample_rate, beats)
            C_sync = self.features.get_pitch_librosa(y_harmonic, self.sample_rate, beats)

            self._log('5.2 Aggregate features')
            intensity_frames = np.matrix(CQT_sync).getT()
            pitch_frames = np.matrix(C_sync).getT()
            timbre_frames = np.matrix(M_sync).getT()

            self._log("6/8 Get loudness, volume, and trim silence")
            volume, avg_volume, loudness = self.processor.get_volume(self.audio_file_path)
            
            self._log("7/8 Extract stems")
            destination = self.audio_file_path
            model_name = 'htdemucs_6s'
            # Assuming dnn_features is a class attribute; if not, adjust accordingly.
            self.features.extract_stems(destination, model_name)

            if self.extract_midi:
                self._log("8/8 Extract MIDI data")

            # Aggregate features
            features = {
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
                "beats": librosa.frames_to_time(beats, sr=self.sample_rate),
                "segments_boundaries": segments_boundaries,
                "segments_labels": segments_labels,
                "frequency_frames": frequency_frames,
                # "frequency": avg_frequency,  # Uncomment if needed
            }

            return features

        except Exception as e:
            if self.verbose:
                print(f"Error extracting features: {e}")
            return None


if __name__ == "__main__":
    # This is a dummy demonstration for the newly added methods.
    demo_audio = librosa.tone(440, duration=5)
    sample_rate = 22050

    extractor = Extractor(demo_audio, sample_rate=sample_rate)
    features = extractor.extract()
