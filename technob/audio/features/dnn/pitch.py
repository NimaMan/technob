
import crepe
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import predict_and_save



def get_pitch_crepe(audio_data, sample_rate):
        """Extract pitch using a DNN model.
        
        Uses the CREPE model to analyze an audio file
        and extract pitch over time.

        Args:
            audio_file
        
        Returns:
            pitch (List[List[float]]): Pitch values with time, 
                frequency and confidence for each frame.
        """

        # Extract pitch using CREPE model
        time, frequency, confidence, activation = crepe.predict(
            audio_data, sample_rate, 
            model_capacity="tiny",
            viterbi=True, 
            center=True,
            step_size=10,
            verbose=1
        )

        # Construct pitch array
        pitch = []
        for i in range(len(time)):
            pitch.append([time[i], frequency[i], confidence[i]])

        return pitch


def extractMIDI(audio_paths, output_dir):
    print('- Extract Midi')
    save_midi = True
    sonify_midi = False
    save_model_outputs = False
    save_notes = False

    predict_and_save(audio_path_list=audio_paths, 
                  output_directory=output_dir, 
                  save_midi=save_midi, 
                  sonify_midi=sonify_midi, 
                  save_model_outputs=save_model_outputs, 
                  save_notes=save_notes)
