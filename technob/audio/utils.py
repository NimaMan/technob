
from pydub import AudioSegment


def convert_type(audio_file_path, format_, output_path=None, artist=" ", album=None): 
    """
    Converts the audio file to the given format.

    Parameters:
        audio_file_path (str): Path to the audio file.
        format_ (str): Format to convert to.
        output_path (str, optional): Path to save the converted audio file. Default is None (overwrite the original file).
        artist (str, optional): Artist name to add to the converted audio file. Default is " ".
        album (str, optional): Album name to add to the converted audio file. Default is " ".

    Returns:
        str: Path to the converted audio file.
    """
    if not output_path:
        output_path = audio_file_path
    if album is None:
        album = artist

    song = AudioSegment.from_file(audio_file_path)
    song.export(output_path, format=format_, tags={'artist': artist, 'album': album})
    return output_path


def convert_bitrate(audio_file_path, bitrate, output_path=None, artist=" ", album=" "):
    """
    Converts the audio file to the given bitrate.

    Parameters:
        audio_file_path (str): Path to the audio file.
        bitrate (str): Bitrate to convert to.
        output_path (str, optional): Path to save the converted audio file. Default is None (overwrite the original file).
        artist (str, optional): Artist name to add to the converted audio file. Default is " ".
        album (str, optional): Album name to add to the converted audio file. Default is " ".

    Returns:
        str: Path to the converted audio file.
    """
    if not output_path:
        output_path = audio_file_path
    song = AudioSegment.from_file(audio_file_path)
    song.export(output_path, bitrate=bitrate, tags={'artist': artist, 'album': album})
    return output_path



if __name__ == "__main__":
    file_dir = "/Users/nimamanaf/Desktop/Music/"
    audio_file_name = "Reinier Zonneveld - CSE (Original Mix).WAV"
    audio_file_path = file_dir + audio_file_name
    output_path = file_dir + "CSE.wav"
    convert_type(audio_file_path, format_="Wav", output_path=output_path, artist="Reinier Zonneveld", album=None)