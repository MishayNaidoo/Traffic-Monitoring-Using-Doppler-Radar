import pyaudio
import wave
import time
import RPi.GPIO as GPIO
import subprocess

# Parameters for audio recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1             # Number of audio channels (mono)
RATE = 48000            # Sample rate (samples per second)
RECORD_DURATION = 120     # Duration of each recording in seconds
BUFFER_SIZE = 4096

# Define GPIO pin for the shutdown button
SHUTDOWN_BUTTON_PIN = 18

# This function will be called when the button is pressed
def shutdown_button_callback(channel):
    print("Button pressed. Shutting down...")
    subprocess.call(['sudo', 'poweroff'])

# Initialize PyAudio
audio = pyaudio.PyAudio()

# List available input devices and their indices
for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    device_name = device_info['name']
    print(f"Device {i}: {device_name}")

# Choose the desired input device by index
desired_device_index = 3  # Replace with the index of your chosen microphone

# Set up the GPIO for the button
GPIO.setmode(GPIO.BCM)
GPIO.setup(SHUTDOWN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(SHUTDOWN_BUTTON_PIN, GPIO.FALLING, callback=shutdown_button_callback, bouncetime=2000)

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

    # Transmit the recorded file to your laptop using SCP
    subprocess.call(['scp','-i','home/raspberry/.ssh/id_rsa', filename, 'your_username@your_laptop_ip:/path/on/laptop'])

    # Optionally, remove the file from the Raspberry Pi to save space
    subprocess.call(['rm', filename])
