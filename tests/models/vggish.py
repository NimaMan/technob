import torch


if __name__ == "__main__":

    model = torch.hub.load('harritaylor/torchvggish', 'vggish')
    model.eval()
    
    # load an audio file 
    import librosa
    audio_path = "technob/docs/examples/cse.WAV"
    y, sr = librosa.load(audio_path)

    # extract audio features
    import numpy as np
    features = model.forward(y, sr)
    print(features.shape)