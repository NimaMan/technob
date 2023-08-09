
import subprocess



def extract_stems(destination: str, model_name: str):
        """Separate audio stems using Demucs DNN model.
        The stemsplit function is using a tool called Demucs to separate the stems (instrument tracks) from a given audio file. Here is a breakdown:

        It uses the subprocess module to call the external 'demucs' command line tool.
        'demucs' is a neural network based audio source separation tool. It can split an audio track into the isolated stems for drums, bass, vocals etc.
        The 'destination' parameter is the path to the input audio file to split stems from.
        The '-n' flag tells Demucs which pretrained model to use for source separation.
        'demucsmodel' is the name of the pretrained model to use. Demucs has models like 'mdx_extra' trained on different datasets.
        When called, Demucs will split the given 'destination' track into multiple audio files, one for each isolated stem.
        The output stem files will be saved to the same folder as the input 'destination' audio.
        The output stem files will be named 'destination' + '_stem' + stem name + '.wav'.        
        Args:
            destination (str): Path to audio file to split
            model_name (str): Name of Demucs model to use
        
        Returns:
            None
        """
        
        # Call Demucs executable with model name
        # Demucs will split audio into stem tracks
        subprocess.run([
            "demucs", 
            destination, 
            "-n", 
            model_name
        ])