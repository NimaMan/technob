#  %%
import pandas as pd
from pydub import AudioSegment
from pydub.silence import detect_silence
from technob.audio.search.shazam.find import Shazam
import logging

logging.basicConfig(level=logging.INFO)

def find_songs_from_set_with_shazam(audio_file_path, initial_interval_duration=150*1000, overlap_duration=30*1000, confidence_threshold=0.7, consecutive_matches=2, silence_threshold=-50):
    '''
    Key Features:
    Audio Preparation: The function loads an audio file into an AudioSegment object.
    Variable Configuration: Several parameters like initial_interval_duration, overlap_duration, and confidence_threshold allow customization of the song recognition process.
    Continuous Recognition: The function segments the audio file and tries to recognize songs from each segment. If a song is recognized in a segment that wasn't recognized in the previous segment, it's added to the results list.
    Variable Intervals: The duration of the audio segments can increase or decrease based on the recognition results, ensuring adaptability.
    Dynamic Overlap: Overlap between segments is adjusted dynamically, especially if a song is recognized towards the end of a segment.
    Silence Detection: Silence intervals within segments help identify potential song transitions, thus adjusting the starting point for the next segment.
    Caching: Results from Shazam are cached based on the start time of the segments. This prevents redundant API calls and speeds up the process.
    Error Handling & Logging: Errors during the song recognition process are gracefully handled and logged. The function also logs information about the recognized songs for better traceability.
    
    Suggestions for Further Improvement:

    Enhanced Caching: Instead of just caching based on the start_time, consider a more sophisticated caching mechanism, perhaps based on the audio segment's hash. This would ensure that even if the same audio segment appears at different times, it won't be processed again.
    Advanced Transition Detection: While the function uses silence to detect song transitions, more advanced methods like spectral flux could be explored to detect transitions even when there isn't complete silence.
    Adaptive Confidence Threshold: Dynamically adjust the confidence_threshold based on the quality or clarity of the audio segment. For instance, in a noisy segment, you might be willing to accept a lower confidence score.
    Batch Processing: If the Shazam API supports it, consider sending multiple audio segments in a single batch request. This would reduce the number of API calls and potentially speed up the process.
    Feedback Loop: If the same song is recognized with varying confidence scores in consecutive segments, use this feedback to refine the segmentation process.
    Alternative Recognition Engines: Integrate other song recognition engines alongside Shazam. If one fails to recognize a song, the others might succeed, increasing overall accuracy.
    '''
    audio = AudioSegment.from_wav(audio_file_path)
    total_duration = len(audio) # in milliseconds
    
    df = pd.DataFrame(columns=["Start Time", "Song", "Artist", "Genre"])

    start_time = 0
    last_recognized_song = None
    fallback_increment = initial_interval_duration // 2  # Set to half of the interval duration

    while start_time < total_duration:
        end_time = start_time + initial_interval_duration
        segment = audio[start_time:end_time]
        songs = {}

        try:
            songs = Shazam(segment).get_songs(n_iterations=5, confidence_threshold=confidence_threshold, consecutive_matches=consecutive_matches)
        except Exception as e:
            logging.error(f"Error recognizing songs for segment starting at {start_time}: {e}")
        logging.info(f"Songs recognized for segment starting at {start_time}: {songs}")
     
        if songs:
            for song, details in songs.items():
                # Append song details to the dataframe using pd.concat
                new_row = pd.DataFrame({
                    "Start Time": [start_time / (1000 * 60)],  # Convert to minutes
                    "Song": [details["name"]],
                    "Artist": [details["artist"]],
                    "Genre": [details["genres"]["primary"]]
                })
                df = pd.concat([df, new_row], ignore_index=True)

            recognized_song = list(songs.keys())[0]
            # Continuous Recognition
            if recognized_song != last_recognized_song:
                last_recognized_song = recognized_song

            # Variable Intervals
            if len(songs) == 1:
                initial_interval_duration += 30 * 1000  # Increase by 30 seconds

        else:
            # Decrease interval if no song recognized
            initial_interval_duration = max(60 * 1000, initial_interval_duration - 10 * 1000)  # Minimum 1 minute

        # Song Transition Detection
        silence_intervals = detect_silence(segment, silence_thresh=silence_threshold)
        increment = max(silence_intervals[-1][1] if silence_intervals else 0, initial_interval_duration - overlap_duration)
        # Apply fallback increment if no progression is detected
        if increment <= 0:
            increment = fallback_increment

        start_time += increment

        # Dynamic Overlap
        if last_recognized_song and not silence_intervals:
            overlap_duration += 10 * 1000  # Increase overlap by 10 seconds

    return df


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


if __name__ == "__main__":
    # Usage
    audio_file = '/Users/nimamanaf/Desktop/Music/misc/Inquisitor (live) @ Monasterio 10 years.wav'
    songs_in_audio = find_songs_from_set_with_shazam(audio_file)
    #print(songs_in_audio)
    # save the results to a csv file in the same directory as the audio file 
    songs_in_audio.to_csv(audio_file.replace(".wav", ".csv"), index=False)
