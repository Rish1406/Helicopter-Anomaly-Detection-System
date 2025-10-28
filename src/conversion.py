import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

audio_dir="synthetic_helicopter_audio"
output_dir="healthy_spectograms"
os.makedirs(output_dir,exist_ok=True)

target_sr=22050
n_fft=1024
hop_length=512
n_mels=128

def save_viridis_spectrogram(audio_path,output_path):
    y,_=librosa.load(audio_path,sr=target_sr)
    S = librosa.feature.melspectrogram(y=y, sr=target_sr, n_fft=n_fft,hop_length=hop_length, n_mels=n_mels)
    S_dB = librosa.power_to_db(S, ref=np.max)
    fig,ax=plt.subplots(figsize=(4, 4), dpi=100)
    librosa.display.specshow(S_dB, sr=target_sr, hop_length=hop_length, x_axis=None, y_axis=None, cmap='viridis')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

for filename in os.listdir(audio_dir):
    if filename.endswith(".wav"):
        audio_path = os.path.join(audio_dir, filename)
        output_name = filename.replace(".wav", ".png")
        output_path = os.path.join(output_dir, output_name)
        save_viridis_spectrogram(audio_path, output_path)
print("All audio files accepted to viridis spectrograms.")