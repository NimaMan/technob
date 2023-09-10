

#%%

import numpy as np
from pydub import AudioSegment
from io import BytesIO
import requests
import uuid
import time
import json
import asyncio

from technob.audio.search.shazam.algorithm import SignatureGenerator
from technob.audio.search.shazam.signature_format import DecodedMessage


class Shazam:
    API_URL = 'https://amp.shazam.com/discovery/v5/en/RU/iphone/-/tag/%s/%s?sync=true&webv3=true&sampling=true&connected=&shazamapiversion=v3&sharehub=true&hubv5minorversion=v5.1&hidelb=true&video=v3'
    HEADERS = {
        "X-Shazam-Platform": "IPHONE",
        "Accept": "*/*",
        "Accept-Language": "en",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Shazam/3685 CFNetwork/1197 Darwin/20.0.0"
    }

    def __init__(self, audio):
        self.audio = self._prepare_audio(audio)
        self.MAX_TIME_SECONDS = 8

    def _prepare_audio(self, audio):
        if isinstance(audio, str):
            format_ = audio.split('.')[-1]
            audio = AudioSegment.from_file(audio, format=format_)   
        elif isinstance(audio, np.ndarray):
            audio = AudioSegment(audio.tobytes(), )
        elif isinstance(audio, bytes):
            audio = AudioSegment.from_file(BytesIO(audio))
        elif isinstance(audio, AudioSegment):
            pass
        else:
            raise TypeError('audio must be str, np.ndarray, bytes or AudioSegment')
        
        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        return audio

    async def async_attempt_recognition(self):
        """Asynchronous version of attempt_recognition."""
        # Assuming there's an asynchronous method that fetches song data
        return await self.fetch_song_data_async()

    def get_songs(self, n_iterations=20, confidence_threshold=0.9, consecutive_matches=3) -> dict:
        recognize_generator = self.attempt_recognition()

        songs = {}
        consecutive_song_counter = 0
        last_song_name = ""

        for _ in range(n_iterations):
            n = next(recognize_generator, None)
            
            # Check if "name" key exists in n
            if n and "name" in n:
                if not n["name"] in songs:
                    songs[n["name"]] = n
            else:
                # Handle cases where "name" is absent. Log or continue based on your preference.
                print(n.get("error", "Unexpected error during recognition."))
                continue

            # Early Exit
            if n.get("score", 0) > confidence_threshold:
                break
            # Limit Unnecessary Recognitions
            if n["name"] == last_song_name:
                consecutive_song_counter += 1
            else:
                consecutive_song_counter = 0
                last_song_name = n["name"]

            if consecutive_song_counter >= consecutive_matches:
                break

        return songs
    '''
    def get_songs(self, n_iterations=20) -> dict:
        recognize_generator = self.attempt_recognition()
        
        songs = {}
        for i in range(n_iterations):
            n = next(recognize_generator)
            if not n["name"] in songs:
                songs[n["name"]] = n
        return songs
    
    def attempt_recognition(self) -> dict:
        signatureGenerator = self.createSignatureGenerator(self.audio)
        while True:
        
            signature = signatureGenerator.get_next_signature()
            if not signature:
                break
            
            results = self.sendRecognizeRequest(signature)
            currentOffset = signatureGenerator.samples_processed / 16000
            audio_info = {"name": results["track"]["title"],
                        "artist": results["track"]["subtitle"],
                        #"genres": results["track"]["genres"], 
                        "shazam_url": results["track"]["url"],
                        #"other_ionfo": results["track"]["hub"],
                        #results["track"]["relatedtracksurl"] # check for the "subject" to find the related tracks in this link
            }
            
            yield audio_info
    '''
    def attempt_recognition(self) -> dict:
        signatureGenerator = self.createSignatureGenerator(self.audio)

        while True:
            signature = signatureGenerator.get_next_signature()
            if not signature:
                break
            
            results = self.sendRecognizeRequest(signature)

            # Check if "track" key exists in results
            if "track" in results:
                audio_info = {
                    "name": results["track"]["title"],
                    "artist": results["track"]["subtitle"],
                    "genres": results["track"]["genres"], 
                    #"shazam_url": results["track"]["url"],
                    #"other_ionfo": results["track"]["hub"],
                    #results["track"]["relatedtracksurl"] # check for the "subject" to find the related tracks in this link
                }
                yield audio_info
            else:
                # Handle cases where "track" is absent. Log or yield a message, based on your preference.
                yield {"error": "Track not recognized or Shazam API response issue."}
        
    def sendRecognizeRequest(self, sig: DecodedMessage) -> dict:
        data = {
            'signature': {
                'uri': sig.encode_to_uri(),
                'samplems':int(sig.number_samples / sig.sample_rate_hz * 1000)
                },
            'timestamp': int(time.time() * 1000),
            'context': {},
            'geolocation': {}
                }
        r = requests.post(
            self.API_URL % (str(uuid.uuid4()).upper(), str(uuid.uuid4()).upper()), 
            headers=self.HEADERS,
            json=data
        )
        return r.json()
    
    def createSignatureGenerator(self, audio: AudioSegment) -> SignatureGenerator:
        signature_generator = SignatureGenerator()
        signature_generator.feed_input(audio.get_array_of_samples())
        signature_generator.MAX_TIME_SECONDS = self.MAX_TIME_SECONDS
        if audio.duration_seconds > 12 * 3:
            signature_generator.samples_processed += 16000 * (int(audio.duration_seconds / 16) - 6)
        return signature_generator


if __name__ == '__main__':
    audio_file = 'technob/docs/examples/Age Of Love.wav'
    songs = Shazam(audio_file,).get_songs(n_iterations=20, confidence_threshold=0.9, consecutive_matches=3)
    print(songs.keys())

    audio_file = "technob/docs/examples/cse.WAV"
    songs = Shazam(audio_file,).get_songs(n_iterations=20, confidence_threshold=0.9, consecutive_matches=3)
    print(songs.keys())
