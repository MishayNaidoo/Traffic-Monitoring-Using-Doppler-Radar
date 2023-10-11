# This python script records the radar readings to a wav file for a selected duration and then uploads this wav file to google drive

import pyaudio
import wave
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Parameters for audio recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1             # Number of audio channels (mono)
RATE = 48000             # Sample rate (samples per second)
RECORD_DURATION = 10     # Duration of each recording in seconds
BUFFER_SIZE = 4096

# Your Google Drive credentials JSON file
CREDENTIALS_FILE = 'trafficmonitoring-401516-dc644ef2c53d.json'

# Create a service object for the Google Drive API
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=['https://www.googleapis.com/auth/drive'])
drive_service = build('drive', 'v3', credentials=credentials)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# List available input devices and their indices
for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    device_name = device_info['name']
    print(f"Device {i}: {device_name}")

# Choose the desired input device by index
desired_device_index = 2  # Replace with the index of your chosen microphone

while True:
    frames = []

    # Get the current time and date for the filename
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    # Open the audio stream before entering the recording loop
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, input_device_index=desired_device_index, frames_per_buffer=BUFFER_SIZE)

    # Record audio data for the specified duration
    start_time = time.time()
    while time.time() - start_time < RECORD_DURATION:
        data = stream.read(BUFFER_SIZE)
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

    # Upload the file to Google Drive
    media_body = drive_service.files().create(
        media_body=filename,
        body={
            'name': filename,
            'parents': ['1effV0Icsmf3zc9hmt_s8qpQgEm6gttsh'],  # ID of the folder where you want to save the file
        }
    ).execute()

    print(f"Recording complete. Saved to Google Drive as '{filename}' with ID: {media_body['id']}")
