import pyaudio
import wave
import time

# Parameters for audio recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1             # Number of audio channels (mono)
RATE = 44100             # Sample rate (samples per second)
RECORD_DURATION = 10     # Duration of each recording in seconds

# Initialize PyAudio
audio = pyaudio.PyAudio()

while True:
    frames = []

    # Get the current time and date for the filename
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    # Open the audio stream before entering the recording loop
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, frames_per_buffer=1024)

    # Record audio data for the specified duration
    start_time = time.time()
    while time.time() - start_time < RECORD_DURATION:
        data = stream.read(1024)
        frames.append(data)

    # Close the audio stream after finishing recording
    stream.stop_stream()
    stream.close()

    # Generate a unique filename with a timestamp for when recording began
    filename = f"recording_{timestamp}.wav"

    print(f"Recording complete. Saving to WAV as '{filename}'...")

    # Save the recorded audio to the unique filename
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
