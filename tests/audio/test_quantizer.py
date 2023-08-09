import unittest
import numpy as np
from ...technob.audio.quantize import Quantizer


class TestQuantizer(unittest.TestCase):
    def setUp(self):
        # Initialize test audio data, sample rate, and other parameters
        self.audio_data = ...  # Replace with actual audio data
        self.sample_rate = ...  # Replace with actual sample rate
        self.target_bpm = ...  # Replace with actual target BPM
        self.pitch_shift_first = ...  # Replace with actual value
        self.quantizer = Quantizer(self.audio_data, self.sample_rate)

    def test_extract_beats(self):
        tempo, beats, beat_frames = self.quantizer.extract_beats(self.audio_data, self.sample_rate)
        self.assertIsInstance(tempo, float)
        self.assertIsInstance(beats, np.ndarray)
        self.assertIsInstance(beat_frames, np.ndarray)
        # Add more assertions as needed

    def test_calculate_fixed_beat_frames(self):
        quantizer = Quantizer(self.audio_data, self.sample_rate)
        beat_frames = ...  # Replace with actual beat frames
        original_bpm = ...  # Replace with actual original BPM
        fixed_beat_frames = quantizer.calculate_fixed_beat_frames(beat_frames, original_bpm, self.target_bpm)
        self.assertIsInstance(fixed_beat_frames, np.ndarray)
        # Add more assertions as needed

    def test_pitch_shift_audio(self):
        quantizer = Quantizer(self.audio_data, self.sample_rate)
        audio_data = ...  # Replace with actual audio data
        original_bpm = ...  # Replace with actual original BPM
        target_bpm = ...  # Replace with actual target BPM
        pitch_shifted_audio = quantizer.pitch_shift_audio(audio_data, self.sample_rate, original_bpm, target_bpm)
        # Add assertions to check if pitch shifting works correctly

    # Add more test methods for other individual methods

    def test_quantization_process(self):
        quantizer = Quantizer(self.audio_data, self.sample_rate, self.target_bpm, self.pitch_shift_first, verbose=False)
        quantized_audio = quantizer()  # This will call __call__ method
        self.assertIsInstance(quantized_audio, np.ndarray)
        # Add more assertions to check if the quantization process works correctly

if __name__ == '__main__':
    unittest.main()
