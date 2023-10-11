import pyaudio
import wave
import time
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Parameters for audio recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1             # Number of audio channels (mono)
RATE = 48000             # Sample rate (samples per second)
RECORD_DURATION = 10     # Duration of each recording in seconds
BUFFER_SIZE = 4096

# Your Google Drive credentials JSON file
SERVICE_ACCOUNT_FILE = 'service_account.json'

# Path to the folder where you want to upload the audio files in Google Drive (optional)
# Set to None if you want to upload to the root directory
FOLDER_ID = None

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Choose the desired input device by index
desired_device_index = 0  # Replace with the index of your chosen microphone

# Authenticate with the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])
drive_service = build('drive', 'v3', credentials=credentials)

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
    media = MediaFileUpload(filename, resumable=True)
    file_metadata = {
        'name': os.path.basename(filename),
        'parents': [FOLDER_ID] if FOLDER_ID else [],
    }
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f"Recording complete. Saved to Google Drive as '{filename}' with ID: {file['id']}")
