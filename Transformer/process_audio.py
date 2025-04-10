
import wave
import numpy as np
import matplotlib.pyplot as plt

def plot_waveform(audio_file):
    # Open the audio file
    with wave.open(audio_file, 'r') as wav_file:
        # Extract Raw Audio from Wav File
        signal = wav_file.readframes(-1)
        signal = np.frombuffer(signal, dtype=np.int16)
        
        # Get the frame rate
        framerate = wav_file.getframerate()
        
        # Time axis in seconds
        time = np.linspace(0, len(signal) / framerate, num=len(signal))
        
        # Plot the waveform
        plt.figure(1)
        plt.title('Waveform of ' + audio_file)
        plt.plot(time, signal)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.show()

# Example usage
audio_file = "path_to_audio_file.wav"
plot_waveform(audio_file)