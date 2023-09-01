import numpy as np
import librosa
import sys

from ...math.utils import root_mean_square


class ProcessorUtils:
    def __init__(self, bit_depth=16, default_silence_threshold=-80.8):
        """
        Initialize the AudioProcessor class.

        Parameters:
            bit_depth (int): Bit depth of the audio data. Default is 16.
            default_silence_threshold (float): Threshold value for determining silence. Default is -80.8 dB.
        """
        self.bit_depth = bit_depth
        self.default_silence_threshold = default_silence_threshold
    
    def loudness_of(self, audio_data):
        """
        Calculate the loudness of the input audio data.

        Parameters:
            audio_data (numpy.ndarray): Input audio data as a 1D numpy array.

        Returns:
            float: Loudness value of the input audio data.
        """
        return root_mean_square(audio_data)

    def normalized(self, audio_data):
        """
        Normalize the input audio data by scaling it with respect to the loudest value (scaled to 1.0).
        The loudest value is calculated using the root mean square of the input data.

        Parameters:
            audio_data (numpy.ndarray): Input audio data as a 1D numpy array.

        Returns:
            numpy.ndarray: Normalized audio data as a 1D numpy array.
        """
        # todo: check if this is the correct way to normalize audio data.
        #return audio_buffer.astype(np.float32) / float(root_mean_square(audio_buffer))
        return audio_data.astype(np.float32) / float(np.amax(np.abs(audio_data)))

    def _convert_to_threshold(self, threshold):
        """
        Convert threshold to the appropriate value based on the bit depth.

        Parameters:
            threshold (float): Input threshold value.

        Returns:
            float: Converted threshold value.
        """
        if int(threshold) != threshold:
            threshold = threshold * float(2 ** (self.bit_depth - 1))
        return threshold

    def find_start_of_non_silent(self, audio_buffer, threshold=None, samples_before=1):
        """
        Find the starting index of non-silent audio samples.

        Parameters:
            audio_buffer (numpy.ndarray): Input audio buffer as a 1D numpy array.
            threshold (float, optional): Threshold value for determining silence. Default is None (use default_silence_threshold).
            samples_before (int): Number of samples to include before the starting index. Default is 1.

        Returns:
            int: Index of the starting non-silent audio sample.
        """
        if threshold is None:
            threshold = self.default_silence_threshold
        threshold = self._convert_to_threshold(threshold)
        absolute_values = np.absolute(audio_buffer)
        index = np.argmax(absolute_values > threshold)
        return max(0, index - samples_before)

    def find_end_of_non_silent(self, audio_buffer, threshold=None, samples_after=1):
        """
        Find the ending index of non-silent audio samples.

        Parameters:
            audio_buffer (numpy.ndarray): Input audio buffer as a 1D numpy array.
            threshold (float, optional): Threshold value for determining silence. Default is None (use default_silence_threshold).
            samples_after (int): Number of samples to include after the ending index. Default is 1.

        Returns:
            int: Index of the ending non-silent audio sample.
        """
        if threshold is None:
            threshold = self.default_silence_threshold
        threshold = self._convert_to_threshold(threshold)
        absolute_values = np.flipud(np.absolute(audio_buffer))
        index = np.argmax(absolute_values > threshold)
        return min(len(audio_buffer), len(audio_buffer) - index + samples_after)

    def trim_audio(self, audio_data, start_threshold=None, end_threshold=None):
        """
        Trim the audio data by removing silent portions at the beginning and end.

        Parameters:
            audio_data (numpy.ndarray): Input audio data as a 1D numpy array.
            start_threshold (float, optional): Threshold value for determining the start of non-silent audio. Default is None (use default_silence_threshold).
            end_threshold (float, optional): Threshold value for determining the end of non-silent audio. Default is None (use default_silence_threshold).

        Returns:
            numpy.ndarray: Trimmed audio data.
        """
        if start_threshold is None:
            start_threshold = self.default_silence_threshold
        if end_threshold is None:
            end_threshold = self.default_silence_threshold

        start = self.find_start_of_non_silent(audio_data, start_threshold)
        end = self.find_end_of_non_silent(audio_data, end_threshold)
        return audio_data[start:end]
    
    def load_and_trim_silence(self, file):
        """
        Load an audio file, normalize it, and trim the silence.

        Parameters:
            file (str): Path to the audio file.

        Returns:
            tuple: Tuple containing the trimmed audio data as a 1D numpy array and the sample rate.
        """
        y, rate = librosa.load(file, mono=True)
        y = self.normalized(y)
        trimmed = self.trim_audio(y)
        return trimmed, rate

    def get_loudness(self, file):
        """
        Calculate the loudness of an audio file by loading, normalizing, and trimming it.

        Parameters:
            file (str): Path to the audio file.

        Returns:
            float: Loudness value of the audio file.
        """
        # todo: Handle the case when audio is silent or an error occurs during processing.
        loudness = -1
        try:
            audio, rate = self.load_and_trim_silence(file)
            loudness = self.loudness_of(audio)
        except Exception as e:
            sys.stderr.write(f"Failed to run on {file}: {e}\n")
        return loudness

    def get_volume(self, file):
        """
        Calculate the volume, average volume, and loudness of an audio file.

        Parameters:
            file (str): Path to the audio file.

        Returns:
            tuple: Tuple containing the volume, average volume, and loudness of the audio file.
        """
        # todo: Calculate volume using a more appropriate method.
        volume = -1
        avg_volume = -1
        loudness = -1
        try:
            audio, rate = self.load_and_trim(file)
            volume = librosa.feature.rms(y=audio)[0] # todo: check what the defintion of volume is.
            avg_volume = np.mean(volume)
            loudness = self.loudness_of(audio)
        except Exception as e:
            sys.stderr.write(f"Failed to get Volume and Loudness on {file}: {e}\n")
        return volume, avg_volume, loudness
    