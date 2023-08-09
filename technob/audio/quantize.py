
from typing import Any
import librosa
import numpy as np
import soundfile as sf
import pyrubberband as pyrb
import sys
from math import log2


class Quantizer:
    """
    Quantize the audio to the desired BPM.
    The code is trying to "quantize" audio, which means adjusting the audio to a specific BPM like a metronome. To do that, it follows these steps:

    1. Adjust the audio to the desired BPM (optional):
    If you want to keep the original BPM of the song, you can do that, or you can "pitch shift" the audio to match the target BPM.
    Pitch shifting involves changing the audio's speed to make it faster or slower without affecting its pitch (how high or low the sound is).

    2. Extract the beats:
    The code analyzes the audio to find the positions of the beats, which are the moments when the rhythm emphasizes a sound.

    3. Calculate fixed beat frames based on the target BPM:
    The code calculates the times when the metronome should click based on the target BPM. 
    For example, if the target BPM is 120, it will generate the times for the metronome clicks, like 0 seconds, 0.5 seconds, 1 second, and so on.

    4. Create a time map for stretching the audio:
    Using the beat frames and fixed beat frames, the code creates a "time map."
    This map tells the code how to adjust the audio to match the metronome clicks, allowing it to stretch or compress the audio in specific places to fit the desired BPM.

    5. Stretch the audio using the time map:
    Finally, the code uses the time map to "stretch" the audio. 
    It resizes specific parts of the audio to fit the metronome clicks, effectively aligning the audio to the desired BPM.
    This process keeps the audio sounding natural without changing the pitch or making it sound strange.

    """
    def __init__(self, audio_data, sample_rate, target_bpm=120, pitch_shift_first=False, verbose=True):
        """
        Initialize the AudioQuantizer.
        Parameters:
            audio_file (str): Path to the audio file to quantize.
            target_bpm (float): Target BPM (Beats Per Minute) for quantization. Default is 120.
            keep_original_bpm (bool): If True, the original BPM of the audio will be preserved. Default is False.
            pitch_shift_first (bool): If True, the audio will be pitch-shifted to the desired BPM before quantization. Default is False.
            extract_midi (bool): If True, MIDI data will be extracted from the quantized audio. Default is False.   
        """
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        self.target_bpm = target_bpm
        self.pitch_shift_first = pitch_shift_first

        # Extract beats from audio data
        tempo, beats, beat_frames = self.extract_beats(audio_data, sample_rate)
        self.original_bpm = tempo

        # Pitch shift audio to target BPM if pitch_shift_first is True
        if pitch_shift_first:
            audio_data = self.pitch_shift_audio(audio_data, sample_rate, tempo, target_bpm)
            tempo, beats, beat_frames = self.extract_beats(audio_data, sample_rate)
        
        if verbose:
            print(f"Quantize Audio with current BPM: {self.original_bpm} to target BPM: {self.target_bpm} with pitch_shift_first: {self.pitch_shift_first}")
        
        # Calculate fixed beat frames based on target BPM
        fixed_beat_frames = self.calculate_fixed_beat_frames(beat_frames, original_bpm=tempo, target_bpm=target_bpm)
        # Create time map for stretching audio to target BPM
        time_map = self.create_time_map(beat_frames, fixed_beat_frames, target_bpm, tempo)
        # Stretch audio to target BPM using time map
        self.quantized_audio = self.stretch_audio(audio_data, sample_rate, time_map)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.quantized_audio
    
    def extract_beats(self, audio_data, sample_rate):
        """
        extract beat frames from audio data

        Parameters:
            audio_data (np.ndarray): Audio data as a numpy array.
            sample_rate (int): Sample rate of the audio.

        Returns:
            np.ndarray: Beat frames as a numpy array.
            np.ndarray: Beats as a numpy array.
            float: Tempo of the audio.
        """

        # separate harmonic and percussive components
        y_harmonic, y_percussive = librosa.effects.hpss(audio_data) 

        # calculate onset strength envelope for percussive component (onset envelope)
        onset_env = librosa.onset.onset_strength(y=y_percussive, sr=sample_rate) 
        
        # calculate tempo and beat frames from onset envelope
        tempo, beats = librosa.beat.beat_track(sr=sample_rate, onset_envelope=onset_env, trim=False)

        # convert beat frames to sample indices
        beat_frames = librosa.frames_to_samples(beats)
        
        return tempo, beats, beat_frames
    
    def calculate_fixed_beat_frames(self, beat_frames, original_bpm, target_bpm=120):
        """
        Calculate fixed beat frames based on target BPM and beat frames from audio data 
        Fix Beat Frames is defined as the beat frames that will be used to stretch the audio to the desired BPM. 
        The beat frames are calculated by multiplying the beat frames from the audio data by the ratio of the target BPM to the original BPM.
        For example, if the target BPM is 120 and the original BPM is 100, then the fixed beat frames will be 1.2 times the original beat frames.

        Parameters:
            beat_frames (np.ndarray): Beat frames as a numpy array.
            target_bpm (float): Target BPM (Beats Per Minute) for quantization.
            default_bpm (float): Default BPM (Beats Per Minute) for quantization. Default is 120.

        Returns:
            np.ndarray: Fixed beat frames as a numpy array.
        """
        # generate metronome
        fixed_beat_times = []
        for i in range(len(beat_frames)):
            fixed_beat_times.append(i * original_bpm / target_bpm)
        fixed_beat_frames = librosa.time_to_samples(fixed_beat_times)

        return fixed_beat_frames
    
    def pitch_shift_audio(self, audio_data, sample_rate, original_bpm, target_bpm):
        """
        Pitch shift the audio to the desired BPM.

        Parameters:
            audio_data (np.ndarray): Audio data as a numpy array.
            sample_rate (int): Sample rate of the audio.
            original_bpm (float): Original BPM (Beats Per Minute) of the audio.
            target_bpm (float): Target BPM (Beats Per Minute) for quantization.
            
        Returns:
            np.ndarray: Pitch-shifted audio data as a numpy array.
        """

        # TODO: implement pitch shifting
        """Pitch shifting options:
            1. librosa.effects.pitch_shift
            2. pysox: https://pysox.readthedocs.io/en/latest/api.html#sox.transform.Transformer.pitch
            3. pyrubberband: https://pyrubberband.readthedocs.io/en/latest/generated/pyrubberband.pyrb.pitch_shift.html

        """
        return None 
    
    
    def create_time_map(self, beat_frames, fixed_beat_frames, original_bpm, target_bpm):
        """
        Create a time map for stretching the audio to the desired BPM. 
        The time map is a list of tuples, where each tuple contains the original beat frame and the fixed beat frame.
        For example, if the original beat frames are [0, 100, 200, 300] and the fixed beat frames are [0, 120, 240, 360], 
        then the time map will be [(0, 0), (100, 120), (200, 240), (300, 360)].

        Parameters:
            beat_frames (np.ndarray): Beat frames as a numpy array.
            fixed_beat_frames (np.ndarray): Fixed beat frames as a numpy array.

        Returns:
            list: Time map as a list of tuples.
        """
        # construct time map
        time_map = []
        for i in range(len(beat_frames)):
            new_member = (beat_frames[i], fixed_beat_frames[i])
            time_map.append(new_member)

        # calculate and add ending to time map
        original_length = len(self.audio_data) # TODO: check why does the original code use len(y+1)
        orig_end_diff = original_length - time_map[i][0]
        new_ending = int(round(time_map[i][1] + orig_end_diff * (original_bpm / target_bpm)))
        new_member = (original_length, new_ending)
        time_map.append(new_member)

        return time_map

    def stretch_audio(self, audio_data, sample_rate, time_map):
        """
        Stretch the audio to the desired BPM using the time map.

        Parameters:
            audio_data (np.ndarray): Audio data as a numpy array.
            sample_rate (int): Sample rate of the audio.
            time_map (list): Time map as a list of tuples.

        Returns:
            np.ndarray: Stretched audio data as a numpy array.
        """

        return pyrb.timemap_stretch(audio_data, sample_rate, time_map)

    def process_stems(self, input_audio, time_map, target_bpm):
    
        # Load stem tracks
        stem_paths = get_stem_paths(input_audio)
        stems = []
        for path in stem_paths:
            stem, _ = librosa.load(path)
            stems.append(stem)

        # Stretch each stem
        stretched_stems = []
        for stem in stems:
            stretched = self.stretch_audio(stem, time_map)
            stretched_stems.append(stretched)

        # Save stretched stems
        output_paths = []
        for i, stem in enumerate(stretched_stems):
            path = self._save_quantized_audio(stem, stem_paths[i], 
                                            target_bpm, output_dir,
                                            f'stem{i}')  
            output_paths.append(path)

        return output_paths
        
    def generate_metronome(self, audio_data, sample_rate, fixed_beat_times, target_bpm):
        """
        Generate a metronome click track for the quantized audio.
        
        clicks_audio = librosa.clicks(times=fixed_beat_times, sr=sample_rate)
        print(len(clicks_audio), len(strechedaudio))
        clicks_audio = clicks_audio[:len(strechedaudio)]         
        path = os.path.join(os.getcwd(), 'processed', vid.id + '- click.wav')
        sf.write(path, clicks_audio, sr)    
        """

        return None    

    def save_quantized_audio(self, audio_data, sample_rate, input_audio_path, target_bpm, output_dir, stem_name=None):
        # ... (audio saving logic)
        return None

        """
        

        # time strech audio
        print('- Quantize Audio: source')
        
        path_suffix = (
            f"Key {vid.audio_features['key']} - "
            f"Freq {round(vid.audio_features['frequency'], 2)} - "
            f"Timbre {round(vid.audio_features['timbre'], 2)} - "
            f"BPM Original {int(vid.audio_features['tempo'])} - "
            f"BPM {bpm}"
        )
        path_prefix = (
            f"{vid.id} - {vid.name}"
        )

        audiofilepaths = []
        # save audio to disk
        path = os.path.join(os.getcwd(), 'processed', path_prefix + " - " + path_suffix +'.wav')
        sf.write(path, strechedaudio, sr)
        audiofilepaths.append(path)

        # process stems
        stems = ['bass', 'drums', 'guitar', 'other', 'piano', 'vocals']
        for stem in stems:
            path = os.path.join(os.getcwd(), 'separated', 'htdemucs_6s', vid.id, stem +'.wav')
            print(f"- Quantize Audio: {stem}")
            y, sr = librosa.load(path, sr=None)
            strechedaudio = pyrb.timemap_stretch(y, sr, time_map)
            # save stems to disk
            path = os.path.join(os.getcwd(), 'processed', path_prefix + " - Stem " + stem + " - " + path_suffix +'.wav')
            sf.write(path, strechedaudio, sr)
            audiofilepaths.append(path)

        """
