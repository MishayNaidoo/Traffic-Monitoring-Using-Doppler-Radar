import pyaudio
import wave

# This script uses PyAudio to record the radar data and save it in a wav file


# Parameters for audio recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 2           # Number of audio channels (mono)
RATE = 48000            # Sample rate (samples per second)
RECORD_SECONDS = 20      # Duration of the recording in seconds
OUTPUT_FILENAME = "output.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# List available input devices and their indices
for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    device_name = device_info['name']
    print(f"Device {i}: {device_name}")

# Choose the desired input device by index
desired_device_index = 1 # Replace with the index of your chosen microphone

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open an audio input stream with the selected device
stream = audio.open(format=pyaudio.paInt16, channels=2, rate=48000,
                    input=True, input_device_index=desired_device_index,
                    frames_per_buffer=1024)

print(f"Recording for {RECORD_SECONDS} seconds...")

frames = []

# Record audio data
for _ in range(0, int(RATE / 1024 * RECORD_SECONDS)):
    data = stream.read(1024)
    frames.append(data)

print("Finished recording.")

# Stop and close the audio stream
stream.stop_stream()
stream.close()

# Terminate PyAudio
audio.terminate()

# Save the recorded audio as a WAV file
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio saved as {OUTPUT_FILENAME}")







