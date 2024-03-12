import struct
import wave

# Step 1: Read ADC Samples from a Text File
with open('E:/UCT/Masters/Traffic-Monitoring-Using-Doppler-Radar/ADC/output.txt', 'r') as file:
    lines = file.readlines()

# Convert the text data to a list of integers
adc_samples = [eval(sample.strip()) for sample in lines]
adc_samples = [item for sublist in adc_samples for item in sublist]

# Step 2: Format the Data for Audacity
# Normalize ADC samples to the range [-1, 1] (float PCM)
normalized_samples = [sample / 2048.0 - 1.0 for sample in adc_samples]

# Pack the normalized samples into a byte stream (16-bit PCM, little-endian format)
audio_data = struct.pack('<' + 'h' * len(normalized_samples), *map(int, normalized_samples))

# Step 3: Save the Data to a WAV File
with wave.open('E:/UCT/Masters/Traffic-Monitoring-Using-Doppler-Radar/ADC/output.wav', 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16-bit PCM
    wav_file.setframerate(40000)  # Adjust the sample rate if needed
    wav_file.writeframes(audio_data)


