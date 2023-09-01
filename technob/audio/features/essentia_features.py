'''
Pip install does not work on Mac OS. You need to install Essentia from source.
Install Dependencies: Use Homebrew to install required dependencies. Some dependencies might not be necessary for your specific use, so you can exclude them.
bash
Copy code
brew install gcc@9 cmake pkg-config python3 libyaml fftw libtool
Clone Essentia:
bash
Copy code
git clone https://github.com/MTG/essentia.git
cd essentia
Build Essentia without certain dependencies:
Modify the build process to exclude dependencies that are causing issues. For example, to exclude Gaia, FFMPEG, and other dependencies, you'd do:
bash
Copy code
./waf configure --mode=release --with-python --no-gaia --no-ffmpeg --no-examples --no-tests
./waf
sudo ./waf install
'''

import essentia
import essentia.standard as es


class EssentiaFeaturesExtractor:
    """
    Extracts audio features using the Essentia library.
    """
    
    def __init__(self, audio_file_path):
        self.audio_file_path = audio_file_path
        self.loader = es.MonoLoader(filename=self.audio_file_path)
        self.audio = self.loader()
    
    def get_segments(self):
        # Onset detection for segmentation
        od = es.OnsetDetection(method='hfc')
        w = es.Windowing(type = 'hann')
        fft = es.FFT() 
        c2p = es.CartesianToPolar() 
        pool = essentia.Pool()
        
        for frame in es.FrameGenerator(self.audio, frameSize=1024, hopSize=512):
            mag, phase = c2p(fft(w(frame)))
            pool.add('features.hfc', od(mag, phase))
            
        onsets = es.Onsets()
        onsets_hfc = onsets(essentia.array([pool['features.hfc']]), [1])
        
        return onsets_hfc

    def get_pitch(self):
        pitch_extractor = es.PredominantPitchMelodia()
        pitch_values, pitch_confidence = pitch_extractor(self.audio)
        return pitch_values

    def get_mfcc(self):
        mfcc = es.MFCC()
        w = es.Windowing(type = 'hann')
        spectrum = es.Spectrum()  
        pool = essentia.Pool()
        
        for frame in es.FrameGenerator(self.audio, frameSize=1024, hopSize=512):
            mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
            pool.add('lowlevel.mfcc', mfcc_coeffs)
        
        return pool['lowlevel.mfcc']

    def get_beats(self):
        rhythm_extractor = es.RhythmExtractor2013()
        bpm, beats, beats_confidence, _, _ = rhythm_extractor(self.audio)
        return bpm, beats

    def get_spectral_contrast(self):
        spectral_contrast = es.SpectralContrast()
        pool = essentia.Pool()
        
        for frame in es.FrameGenerator(self.audio, frameSize=1024, hopSize=512):
            f, s = spectral_contrast(frame)
            pool.add('lowlevel.spectral_contrast', s)
        
        return pool['lowlevel.spectral_contrast']

    def extract_features(self):
        features = {
            'segments': self.get_segments(),
            'pitch': self.get_pitch(),
            'mfcc': self.get_mfcc(),
            'beats': self.get_beats(),
            'spectral_contrast': self.get_spectral_contrast()
        }
        return features

if __name__ == "__main__":
    # This is a dummy demonstration for the newly added methods.
    import librosa
    demo_audio = librosa.tone(440, duration=5)
    sample_rate = 22050

    example_features = {
        "rhythm": EssentiaFeaturesExtractor.get_rhythm(demo_audio, sample_rate),
        "tonnetz": EssentiaFeaturesExtractor.get_tonnetz(demo_audio, sample_rate),
        "spectral_contrast": EssentiaFeaturesExtractor.get_spectral_contrast(demo_audio, sample_rate),
        "zero_crossing_rate": EssentiaFeaturesExtractor.get_zero_crossing_rate(demo_audio)
    }

    