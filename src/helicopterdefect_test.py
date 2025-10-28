import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import random
healthy_dir = "synthetic_helicopter_audio"

def spectrogram_dir():
    os.makedirs("defected_spectrogram_dir", exist_ok=True)

target_sr = 22050
n_fft = 1024
hop_length = 512
n_mels = 128

def inject_anomaly(y):
    choice = random.choice(["noise", "dropout", "pitch", "freq_mask"])

    if choice == "noise":
        noise = np.random.normal(0, 0.05, y.shape)
        y += noise

    elif choice == "dropout":
        start = random.randint(0, len(y) // 2)
        end = start + random.randint(2000, 8000)
        y[start:end] = 0

    elif choice == "pitch":
        y = librosa.effects.pitch_shift(y, sr=target_sr, n_steps=np.random.uniform(2, 4))

    elif choice == "freq_mask":
        y = librosa.effects.preemphasis(y)
    return y

def save_defect_spectrogram(audio_path, output_path):
    y, _ = librosa.load(audio_path, sr=target_sr)
    y = inject_anomaly(y,target_sr)
    S = librosa.feature.melspectrogram(y, sr=target_sr, n_fft=n_fft,hop_length=hop_length, n_mels=n_mels)
    S_dB = librosa.power_to_db(S, ref=np.max)
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    librosa.display.specshow(S_dB, sr=target_sr, hop_length=hop_length,cmap="viridis")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()

file_count = 0
for filename in os.listdir(healthy_dir):
    if filename.endswith(".wav") and file_count <= 10:
        audio_path = os.path.join(healthy_dir, filename)
        output_name = filename.replace(".wav", "_defect.png")
        output_path = os.path.join("defected_spectrogram_dir", output_name)
        
        save_defect_spectrogram(audio_path, output_path)
        file_count += 1
print("Synthetic defective samples generated.")


