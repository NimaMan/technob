
'''
We need to get an "Apllication" API key from AcoustID fto detect the song from the audio file. check the link below to get the key:
https://acoustid.org/faq
'''

# %%
import numpy as np
import acoustid


def get_response(api_key, audio, meta = ['recordings',]):
    if meta is None:
        meta = ['recordings',
                'recordingids',
                'releases',
                'releaseids',
                'releasegroups',
                'releasegroupids',
                'tracks',
                'compress',
                'usermeta',
                'sources']
        
    if isinstance(audio, str):
        duration, fingerprint = acoustid.fingerprint_file(audio)
    elif isinstance(audio, bytes):
        duration, fingerprint = acoustid.fingerprint(audio)
    elif isinstance(audio, np.ndarray):
        duration, fingerprint = acoustid.fingerprint(audio.tobytes())
    else:
        raise TypeError('audio must be str, np.ndarray or bytes')
    return acoustid.lookup(api_key, fingerprint, duration, meta=meta)


def extract_song_details(results, return_accoustid=False):
    similar_songs = []
    if len(results) == 0:
        print("No results are found.")
        return similar_songs
    for result in results:
        score = result.get('score', 0)
        
        # Check if the result meets the score threshold and has recording details
        if 'recordings' in result:
            recording = result['recordings'][0]
            title = recording.get('title')
            artist = recording['artists'][0]['name']
            duration = recording.get('duration')
            song_info = {"title": title, "artist": artist, "score": score, "duration": duration}
            similar_songs.append(song_info)
        else:
            if return_accoustid:
                similar_songs.append({"accoustid": result['id'], "score": score})
    return similar_songs

    
def identify_song(audio_file_path, api_key):
    response = get_response(api_key, audio_file_path)
    results = response['results']
    if len(results) == 0:
        return None
    return extract_song_details(results)



if __name__ == "__main__":
    api_key = None
    audio_file = 'technob/docs/examples/Age Of Love.wav'
    response = get_response(api_key, audio_file)
    song_info = identify_song(audio_file, api_key)
    print(song_info)
