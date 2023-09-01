from pydub import AudioSegment
from pydub.playback import play

# Load the audio file
song = AudioSegment.from_wav("technob/technob/interface/cse.wav")

# Play the audio file
play(song)
