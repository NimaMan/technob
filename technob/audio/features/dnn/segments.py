
import os 
import sys
import numpy as np
import Segmenter


def get_segments(audio_file_path):
        """Segment an audio file and return boundaries and labels.
        
        Uses an external Segmenter model to analyze the audio file
        and identify segment boundaries and predict labels for each
        identified segment.

        Args:
            audio_file_path (str): Path to audio file.
        
        Returns:
            boundaries (List[float]): List of segment boundary times.
            labels (List[str]): List of predicted label for each segment.
        """

        # Load Segmenter model 
        segmenter = Segmenter() 

        # Segment audio file
        boundaries, labs = segmenter.proc_audio(audio_file_path)
        
        # Return segment boundaries and predicted labels
        return boundaries, labs