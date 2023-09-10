
from pydub import AudioSegment
from pydub.silence import detect_silence
from technob.audio.search.shazam.find import Shazam
import logging

logging.basicConfig(level=logging.INFO)

def find_songs_from_set_with_shazam_v2(audio_file_path, initial_interval_duration=60*1000, overlap_duration=30*1000, confidence_threshold=0.9, consecutive_matches=2, silence_threshold=-50):
    audio = AudioSegment.from_wav(audio_file_path)
    total_duration = len(audio)
    
    recognized_songs = []
    segments_cache = {}

    start_time = 0
    last_recognized_song = None

    while start_time < total_duration:
        end_time = start_time + initial_interval_duration
        segment = audio[start_time:end_time]

        # Use cached results if segment was processed before
        if start_time in segments_cache:
            songs = segments_cache[start_time]
        else:
            try:
                songs = Shazam(segment).get_songs(n_iterations=5, confidence_threshold=confidence_threshold, consecutive_matches=consecutive_matches)
                segments_cache[start_time] = songs
            except Exception as e:
                logging.error(f"Error recognizing songs for segment starting at {start_time}: {e}")
                songs = {}

        logging.info(f"Songs recognized for segment starting at {start_time}: {songs}")

        if songs:
            recognized_song = list(songs.keys())[0]
            # Continuous Recognition
            if recognized_song != last_recognized_song:
                recognized_songs.append(recognized_song)
                last_recognized_song = recognized_song
            # Variable Intervals
            if len(songs) == 1:
                initial_interval_duration += 30 * 1000  # Increase by 30 seconds

        else:
            # Decrease interval if no song recognized
            initial_interval_duration = max(60 * 1000, initial_interval_duration - 10 * 1000)  # Minimum 1 minute

        # Song Transition Detection
        silence_intervals = detect_silence(segment, silence_thresh=silence_threshold)
        if silence_intervals:
            start_time += silence_intervals[-1][1]
        else:
            # Dynamic Overlap
            if last_recognized_song:
                overlap_duration += 10 * 1000  # Increase overlap by 10 seconds
            start_time += (initial_interval_duration - overlap_duration)

    return recognized_songs

def find_songs_from_set_with_shazam_v1(audio_file_path):
    '''
    The function accepts an audio file path (audio_file_path) as its input.
    The audio is loaded into an AudioSegment object.
    The function initializes a few variables:
    start_time to keep track of the starting point of the audio segment to be analyzed.
    interval_duration to define the duration of the audio segment. It starts with 1 minute.
    overlap_duration to define how much overlap there is between consecutive audio segments. It's set to 30 seconds.
    last_recognized_song to remember the song that was recognized in the previous iteration.
    In a loop, the function segments the audio and uses the Shazam class to recognize songs from each segment.
    It employs continuous recognition to keep track of song changes.
    If only one song is recognized in an interval, the interval duration is increased by 30 seconds. If no song is recognized, the interval is reduced by 10 seconds (but it doesn't go below 1 minute).
    The function uses silence detection to identify potential song transitions and adjust the start time for the next segment accordingly.
    The recognized songs are added to a list (recognized_songs), which is returned at the end.
    '''
    audio = AudioSegment.from_wav(audio_file_path)
    total_duration = len(audio)
    
    recognized_songs = []

    start_time = 0
    interval_duration = 60 * 1000  # Start with 1 minute in milliseconds
    overlap_duration = 30 * 1000  # 30 seconds in milliseconds

    last_recognized_song = None

    while start_time < total_duration:
        end_time = start_time + interval_duration
        segment = audio[start_time:end_time]

        songs = Shazam(segment).get_songs(n_iterations=5, confidence_threshold=0.9, consecutive_matches=2)
        print(songs)
        if songs:
            recognized_song = list(songs.keys())[0]

            # Continuous Recognition
            if recognized_song != last_recognized_song:
                recognized_songs.append(recognized_song)
                last_recognized_song = recognized_song

            # Variable Intervals
            if len(songs) == 1:
                interval_duration += 30 * 1000  # Increase by 30 seconds

        else:
            # Decrease interval if no song recognized
            interval_duration = max(60 * 1000, interval_duration - 10 * 1000)  # Minimum 1 minute

        # Song Transition Detection
        silence_intervals = detect_silence(segment, silence_thresh=-50)
        if silence_intervals:
            start_time += silence_intervals[-1][1]
        else:
            start_time += (interval_duration - overlap_duration)

    return recognized_songs

# Usage
audio_file = '/Users/nimamanaf/Desktop/Music/Amelia Lens/Amelie Lens   Tomorrowland Winter 2023.wav'
songs_in_audio = find_songs_from_set_with_shazam_v2(audio_file)
print(songs_in_audio)
