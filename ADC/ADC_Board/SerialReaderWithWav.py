import serial
import wave
import struct

# Serial port configuration
ser = serial.Serial('COM7', baudrate=12000000)  # Adjust 'COMx' and baudrate

# WAV file configuration
output_wav_path = 'E:/UCT/Masters/Traffic-Monitoring-Using-Doppler-Radar/ADC/ADC_Board/output8.wav'
sample_rate = 48000  # Adjust to the correct sample rate for your data
num_channels = 1  # Mono audio
sample_width = 2  # 2 bytes (16-bit audio)

# ADC and voltage conversion constants
v_ref = 3.0  # Reference voltage for the ADC
max_adc_value = 65535  # Maximum ADC value for a 16-bit ADC
wav_min_value = -32768
wav_max_value = 32767

try:
    # Set up the WAV file for writing
    with wave.open(output_wav_path, 'w') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)

        while True:
            # Read the raw binary data from the serial port
            raw_data = ser.read(5096)

            # Convert the raw data into a list of 16-bit values and then to voltages
            sixteen_bit_list = [(raw_data[i]) | (raw_data[i + 1] << 8) for i in range(0, len(raw_data), 2)]
            voltage_list = [(value / max_adc_value) * v_ref for value in sixteen_bit_list]

            # Convert the voltage values to fit within the WAV file's 16-bit signed integer range
            wav_values = [int((voltage / v_ref) * wav_max_value) for voltage in voltage_list]

            # Convert the list of integers to bytes and write to the WAV file
            for value in wav_values:
                wav_file.writeframes(struct.pack('<h', value))

            # Optionally, print the voltage values to the console
            #print(voltage_list)

except KeyboardInterrupt:
    print("Serial reading terminated by user.")
    ser.close()
