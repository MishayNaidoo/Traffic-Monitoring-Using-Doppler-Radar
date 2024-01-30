import pyaudio

audio = pyaudio.PyAudio()

for i in range(audio.get_device_count()):
	device_info = audio.get_device_info_by_index(i)
	device_name = device_info['name']
	print(f"Device {i}: {device_name}")
	print(device_info)

	
audio.terminate()
