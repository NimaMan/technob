# Tutorial 02: Segmentation - Breaking the Magical Music Puzzle

In the previous tutorial, we learned how music and computation work together like magical friends to create beautiful sounds. Now, let's take a closer look at one of the essential tools in our music magician's toolkit - Segmentation!

## What is Segmentation in Music?

Imagine you have a big jigsaw puzzle with many colorful pieces. Each piece represents a small part of a beautiful picture. But putting the whole puzzle together at once can be overwhelming, right?

In music, we have different parts that make up a song, just like different scenes in a magical adventure. Segmentation is like dividing the music into these smaller scenes, which we call "segments." Each segment has its own magical character and tells a part of the musical story.

## Why is Segmentation Important?

Let's say you have a magical song you love to dance to. It has exciting parts where everyone claps and jumps (we call this the "chorus"), and it has calm parts where the singer tells the beginning of the story (we call this the "intro").

Without segmentation, it would be like trying to read a whole book in one go without any chapters or breaks! With segmentation, we can focus on the exciting chorus part and make it even more magical by adding special effects. Or we can look at the calm intro part and make it even more magical by adding a beautiful melody.

## How Does Segmentation Work?

There are different ways to do segmentation, and we'll show you three exciting methods to get started:
### Classical Methods
#### 1. Fixed-Length Segments

Imagine you have a magic ruler that can measure exactly 10 seconds of music. With this ruler, you can cut the music into equal-sized segments, like slicing a delicious cake into even pieces. Each segment becomes a small part of the musical adventure, and we can explore them one by one.

#### 2. Silence Detection

In this method, the music machine listens carefully to the song. Whenever it hears silence, it marks the beginning of a new segment. It's like finding the spaces between the words in a magical storybook. Silence detection helps us find natural breaks in the music, like where the singer takes a breath or where there's a pause between beats.

#### 3. Beat Detection

Remember the dance party where everyone moves in sync? In this method, the music machine listens to the beats and dances along with them. It marks the moments when the beats change or when the music does a cool trick. Beat detection helps us find the most exciting parts of the song, like the chorus where everyone sings along!

## Segmentation using Machine Learning and Algorithms
There are many different ways to do segmentation using machine learning and algorithms. Here are some of the most popular methods:
### Classical Methods
#### 1. Hidden Markov Models (HMMs)
Hidden Markov Models (HMMs) are a type of probabilistic model that can be used for segmentation. They are powerful tools that can learn from data and solve complex problems. In music, HMMs can be used for segmentation by learning from examples of segmented music.

#### 2. Dynamic Programming (DP)
Dynamic Programming (DP) is a method for solving optimization problems. It is a powerful tool that can be used for segmentation. In music, DP can be used for segmentation by learning from examples of segmented music.

#### 3. Neural Networks
Neural networks have become increasingly popular in recent years. They are powerful tools that can learn from data and solve complex problems. In music, neural networks can be used for segmentation by learning from examples of segmented music. Some of the most popular segmentation neural network  models are: 

- SegNet
- U-Net

## Let's Try Some Magic!

Now, let's put on our magician hats and try out some code examples to see segmentation in action.

```python
# Imagine we have a magical music file called "techno_song.mp3"
# Let's use the "librosa" library to perform segmentation

import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load the music file
audio_file = "techno_song.mp3"
y, sr = librosa.load(audio_file)

# Method 1: Fixed-Length Segments
# Let's cut the music into segments of 10 seconds each
segment_duration = 10  # 10 seconds
segments = librosa.util.frame(y, int(segment_duration * sr), int(segment_duration * sr))

# Display the segments
plt.figure(figsize=(12, 4))
librosa.display.waveshow(y, sr=sr, alpha=0.5)
librosa.display.waveshow(segments[:, 0], sr=sr, color='r')
plt.title("Fixed-Length Segments")
plt.legend(['Music', 'Segment 1'])
plt.show()
```

In this code example, we loaded a magical music file called "techno_song.mp3" and divided it into fixed-length segments of 10 seconds each. The red segment you see in the plot represents the first 10 seconds of the song.

Now, let's try another method:

```python
# Method 2: Silence Detection
# Let's find the silent parts and mark them as segments

import numpy as np

# Find the silent parts using the "librosa" library
silence_threshold = 0.02  # Adjust this threshold as needed
silence_mask = np.abs(y) < silence_threshold

# Find the indexes where silence ends and music starts
segment_starts = librosa.util.frame(silence_mask, frame_length=2, hop_length=1).max(axis=0)
segment_starts = np.where(segment_starts)[0]

# Create segments using the indexes
segments = librosa.util.frame(y, frame_length=sr, hop_length=1, index=segment_starts)

# Display the segments
plt.figure(figsize=(12, 4))
librosa.display.waveshow(y, sr=sr, alpha=0.5)
librosa.display.waveshow(segments[:, 0], sr=sr, color='g')
plt.title("Silence Detection Segments")
plt.legend(['Music', 'Segment 1'])
plt.show()
```

In this example, we used silence detection to find the silent parts in the music and marked them as segments. The green segment you see in the plot represents one of the segments where there's no music playing.

Finally, let's try the last method:

```python
# Method 3: Beat Detection
# Let's find the exciting parts of the music where the beats change

# Use the "librosa" library to detect beats
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

# Find the times where the beats occur
beat_times = librosa.frames_to_time(beats, sr=sr)

# Create segments around the beat times
segments = librosa.util.frame(y, frame_length=sr, hop_length=1, index=beats)

# Display the segments
plt.figure(figsize=(12, 4))
librosa.display.waveshow(y, sr=sr, alpha=0.5)
librosa.display.waveshow(segments[:, 0], sr=sr, color='b')
plt.title("Beat Detection Segments")
plt.legend(['Music', 'Segment 1'])
plt.show()
```

In this example, we used beat detection to find the exciting parts of the music where the beats change. The blue segment you see in the plot represents one of the segments around a beat.

And there you have it - segmentation magic! Now you can experiment with different songs and methods to create your own musical puzzles and explore each piece of the music one by one.

In the next tutorial, we'll uncover the secret of pitch tracking - how to find the magical numbers that represent the notes in the music. So get ready for more musical adventures, and keep your magic hats on! 🧙‍♂️🎵🔮