# Technob - Audio Processing for Techno Music Production

Technob is an open-source Python audio processing module designed to assist music enthusiasts, producers, and DJs in mixing and producing techno songs. This module will eventually provides a comprehensive set of tools to analyze, manipulate, and enhance audio signals, giving you the power to create your unique techno music with ease.

# Current Features

## Segmentation: 
Break down long audio recordings into smaller segments to analyze and process specific sections independently. This allows you to focus on individual elements of the music for better control and manipulation.

## Pitch Tracking: 
Pitch tracking is the process of determining the pitch of an audio signal at different points in time. The putch is defined as the frequency of the sound wave, which is perceived as the musical note. For example, a pitch of 440 Hz corresponds to the note A4. Pitch tracking is useful for identifying the notes played in the audio and understanding the melody and harmonies. Melody is the sequence of notes played in a song, while harmony is the combination of multiple notes played simultaneously. This information helps you make informed decisions when creating new layers of sound.

## Sample Separation: 
Separate the harmonic (musical) and percussive (rhythmic) components of the audio. This enables you to apply different effects and processing to each part separately, leading to more dynamic and polished techno tracks.

## Beat Tracking: 
Beat tracking is the process of identifying the rhythmic beats in an audio signal. Beats are the regular pulses that form the foundation of music. They are typically produced by percussive instruments such as drums and cymbals. Beat tracking is useful for synchronizing your music with the desired tempo and maintaining a consistent beat throughout your mix. It also helps you identify the downbeats, which are the first beats of each bar. Downbeats are often emphasized to create a sense of rhythm and structure in the music. 

Beat tracking is a challenging task because the beats are not always clearly defined. The tempo may vary throughout the song, and the percussive sounds may be masked by other instruments. Technob will integrate state-of-the-art beat tracking algorithm to provide accurate and reliable results. Beat tracking enables synchronization with the desired tempo and maintaining a consistent beat throughout your mix. 

## Feature Extraction: 
Extract essential audio features such as intensity, pitch, timbre, and volume. These features provide valuable insights into the characteristics of your audio and assist you in crafting the desired sound. For example, you can use the intensity to identify the loud and soft parts of the music and adjust the volume accordingly. You can also use the pitch to identify the notes played in the audio and ensure they are in harmony with each other. We will show you how to extract and visualize these features in the examples.

## Quantization: 
Align the audio to a specific tempo or beat grid. Quantization ensures that all elements of your music are precisely timed and synchronized, creating a tight and professional sound. Quantization is especially important in techno music, where the beat is the driving force of the track. We will show you how to quantize your audio to the desired tempo or beat grid in the examples. 

## Source Separation: 
Isolate and separate different sound sources within a mixed audio recording. This allows you to modify or enhance individual elements, such as vocals or instruments, independently.

Source separation is a challenging task because the mixed audio signal is a combination of multiple sources. The sources may overlap in time and frequency, making it difficult to separate them. Source separation is an active area of research, and many algorithms have been developed to tackle this problem. 

# Why all these features are important for techno music production?
1. Segmentation:
Imagine you have a big box of colorful LEGO bricks. Each brick represents a different sound in a techno song, like a drum hit, a synth melody, or a vocal sample. Now, to build an awesome LEGO creation, you need to sort and group the bricks by their colors and shapes, right? Segmentation is like sorting these LEGO bricks. It breaks down a long techno song into smaller parts, just like dividing your LEGO bricks into groups. This way, you can focus on one group at a time, making it easier to understand and improve each part of the music. With segmentation, you can work on the exciting build-up part, the catchy melody, or the powerful drop separately and make them all sound perfect!

2. Pitch Tracking:
Pitch is like the highness or lowness of a musical note. It's like the different keys on a piano. In techno music, you have those cool synthesizer sounds, and each sound has its special key. Pitch tracking helps you figure out which keys are played in the song at different moments. It's like having a magical piano that can tell you the exact notes being played! Once you know the notes, you can add more sounds that match those notes to create a harmonious and beautiful techno melody that makes people dance happily.

3. Sample Separation:
In a techno song, you have two main groups of sounds: the "beat" that makes you tap your foot and the "music" that makes you feel the groove and dance freely. Sample separation is like using special glasses that let you see the beat and the music separately. Imagine wearing these magical glasses to watch a soccer match. With one eye, you see only the players running around and kicking the ball (the beat). With the other eye, you see the exciting crowd cheering and waving flags (the music). Separating the beat and the music helps you treat them differently. You can make the beat sound punchy and powerful, while the music can be smooth and dreamy.

4. Beat Tracking:
A techno song is like a train journey. You want the train to keep chugging along at a steady pace so that everyone can enjoy the ride and dance together happily. Beat tracking is like having a fantastic train conductor who keeps the train on track and on time. It helps you find the strong, rhythmic beats in the music. These beats are like the wheels of the train turning, and they give techno its signature energy and drive. When the beats are steady and consistent, the whole journey becomes super fun and exciting!

5. Feature Extraction:
Think of your favorite techno song as a special cake. Now, if you want to make that cake even more delicious, you need to know its ingredients. Feature extraction is like being a cake expert who can taste the cake and tell you all about its yummy flavors. In the same way, feature extraction helps you "taste" the music and understand its different ingredients, like how loud or soft it is, how the different sounds blend together, and more. Once you know these ingredients, you can make adjustments to create the perfect techno cake that makes everyone go, "Wow!"

6. Quantization:
Have you ever played with toy cars or trains? To make them race smoothly, you need a racetrack with lanes and markings to keep everything organized. Quantization is like creating those lanes and markings for your techno song. It helps you line up all the different sounds in the music so they play at the right time, like the cars on a racetrack following the lanes. When everything is in sync and perfectly timed, it's like magic! Your techno song becomes super tight and powerful, and people can't help but move to the beat!

7. Source Separation:
Imagine you're in a noisy room with many people talking at once. It's hard to focus on a single conversation because all the sounds mix together. Source separation is like having special ears that can pick out and separate the voices of your friends from all the noise in the room. In techno music, you have lots of different sounds playing together, and source separation helps you hear each sound separately. You can then give special attention to the cool synth, the awesome vocals, and the exciting drums, just like chatting with each friend separately in that noisy room!

With all these awesome features in the Technob audio processing module, you'll have the power to create fantastic techno songs that make people dance, smile, and have an amazing time on the dance floor! So, let's dive in and start making some incredible techno music together! 🎶

# Getting Started
To use Technob in your techno music production, follow the installation instructions and examples provided in the Documentation. The documentation takes you through the entire audio processing pipeline with clear explanations and code samples.


## Installation 
Technob is currently in the early stages of development. To install the latest version of Technob, move to the root directory of the project and run the following command:
```bash
pip install -e .
```


# Current State of the Project
Technob is currently in the early stages of development. Our objective is to use state of the art machine learning and signal processing techniques to develop a robust and reliable audio processing module for techno music production. Currently, we are in the process of finishing the following steps of the audio processing pipeline:
- [x] Quantization
The current version of Technob supports quantization to a specific tempo. We are working on adding support for quantization to a beat grid. In particular, we are exploring:
    - Pitch Shifting: Pitch shifting is the process of changing the pitch of an audio signal without changing its tempo. This is useful for aligning the audio to a specific beat grid. Currently, we are working on implementing a pitch shifting algorithm based on the phase vocoder. We are also exploring other pitch shifting algorithms, such as the pitch synchronous overlap and add (PSOLA) algorithm.
    - Time Stretching: Time stretching is the process of changing the tempo of an audio signal without changing its pitch. This is useful for aligning the audio to a specific tempo. Currently, we are working on implementing a time stretching algorithm based on the phase vocoder. We are also exploring other time stretching algorithms, such as the phase vocoder with a time domain pitch shifter (TD-PSOLA).

- [x] Source Separation
The current version of Technob supports source separation using classical algorithms and machine learning. In particular, we are exploring:
    - Non-negative Matrix Factorization (NMF): NMF is a classical algorithm for source separation. It works by decomposing a spectrogram into a set of basis vectors and a set of activation vectors. The basis vectors represent the different sources in the audio signal, while the activation vectors represent the contribution of each source to the audio signal. Currently, we are working on implementing a NMF algorithm based on the multiplicative update rule. We are also exploring other NMF algorithms, such as the alternating non-negative least squares (ANLS) algorithm.
    - Deep Clustering: Deep clustering is a machine learning algorithm for source separation. It works by training a deep neural network to cluster the time-frequency bins of a spectrogram into different sources. Currently, we are working on implementing a deep clustering algorithm based on the deep clustering network (DCN). We are also exploring other deep clustering algorithms, such as the permutation invariant training (PIT) algorithm.

    - Meta is offering some source-separation models. Currently, we suppport using Demucs. We are working on adding support for other source-separation models, such as Open-Unmix.

- [x] Beat Tracking
    Beat Tracking is being performed using the librosa library at the moment. The support for ``madmom`` will be added soon. In addition, we are working on adding state of the art beat tracking algorithms, such as the beat tracking algorithm based on the dynamic bayesian network (DBN).

- [x] Pitch Tracking
    Pitch Tracking is being performed using the librosa library at the moment. Check this link for some discussion on [pitch detection](https://brentspell.com/2022/pytorch-yin/). 

- [x] Segmentation
    Segmentation is a work in progress. We are looking into adding Deep audio segmenter similar to:
        - [Deep Audio Segmenter](https://github.com/janclemenslab/das)

- [x] Feature Extraction
    Feature Extraction is a work in progress. The current objective of the feature selection is to extract features that are relevant to finding similar songs. This part will be supported in version 0.2.0.

    Some of the work that will be inevstigated are: 
    - MERT model: the pre-print, pre-trained models, and training code can be found here:
        - [Pre-print](https://arxiv.org/abs/2306.00107)
        - [Pre-trained models](https://huggingface.co/m-a-p/MERT-v1-330M)
        - [Github repo](https://github.com/yizhilll/MERT)
    
-[x] Music Gen and Audio Craft 
    We will add the latest models open sourced by Meta, in July 2023. 

- [x] Search Engine
    The search engine is a work in progress. The current objective of the search engine is to find similar songs. This part will be supported in version 0.2.0. The main objective of the search engine is to find similar songs. 

- [x] Tests 
    The tests are a work in progress. The current objective of the tests is to make sure that the code is working as expected. This part will be supported in version 0.2.0.

-[x] Improve Tutorial
    The tutorial is a work in progress. Our Initial objective in the tutorial is to make it beginner freindly with no prior informaation aboout Audio Processing to very advanced information on how to use state of the art algorithms, data structures, and models to create a techno song. 

-[x] Docker Support
    Docker support is a work in progress. The current objective of the docker support is to make it easy to deploy the search engine. This part will be supported in version 0.2.0.

# Contribute
We welcome contributions from the techno community! Whether it's adding new features, fixing bugs, or improving documentation, every contribution makes Technob even better. The  Contribution Guidelines will be added in version 0.2.0.

# License
Technob is released under the MIT License.

