# pip install soundfile scipy

import os
import numpy as np
import soundfile as sf
from scipy.signal import butter,lfilter

num_samples = 10000
duration = 10
sr = 22050

output_dir = "synthetic_helicopter_audio"
os.makedirs(output_dir, exist_ok=True)

def amplitude_modulation(signal, rate, depth, sr):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    modulator = (1 + depth * np.sin(2 * np.pi * rate * t))
    return signal * modulator

def bandpass_filter(data, cutoff, sr, order=5):
    nyq = 0.5 * sr
    normal_cutoff=cutoff/nyq
    b, a = butter(order, normal_cutoff, btype="low")
    return lfilter(b, a, data)

def generate_random_sample(sr, duration):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    base_freq = np.random.uniform(180, 220)
    harmonics = np.random.randint(2, 5)
    weights = np.random.uniform(0.3, 1.0, harmonics)
    signal = sum(weights[i] * np.sin(2 * np.pi * base_freq * (i + 1) * t) for i in range(harmonics))

    am_rate = np.random.uniform(0.5, 3.0)
    am_depth = np.random.uniform(0.2, 0.5)
    signal = amplitude_modulation(signal, am_rate, am_depth, sr)

    noise = np.random.normal(0, 0.01, signal.shape)
    signal += noise

    gain = np.random.uniform(0.3, 0.8)
    signal *= gain

    cutoff = np.random.uniform(2000, 8000)
    signal = bandpass_filter(signal, cutoff, sr)
    signal /= np.max(np.abs(signal))
    return signal

for i in range(num_samples):
    audio = generate_random_sample(sr, duration)
    file_name = os.path.join(output_dir, f"helicopter_healthy_{i:05d}.wav")
    sf.write(file_name, audio, sr)

    if (i+1)%100==0:
        print(f"{i+1}/{num_samples} saved: {file_name}")
print("Done generating synthetic audio.")
