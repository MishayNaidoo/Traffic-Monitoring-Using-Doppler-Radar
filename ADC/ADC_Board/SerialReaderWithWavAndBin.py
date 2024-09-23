import serial
import wave
import struct

# Serial port configuration
ser = serial.Serial('COM7', baudrate=12000000)  # Adjust 'COMx' and baudrate

# File configuration
output_bin_path = 'E:/UCT/Masters/Traffic-Monitoring-Using-Doppler-Radar/ADC/ADC_Board/output12.bin'
output_wav_path = 'E:/UCT/Masters/Traffic-Monitoring-Using-Doppler-Radar/ADC/ADC_Board/output12.wav'
sample_rate = 48000  # Adjust to the correct sample rate for your data
num_channels = 1  # Mono audio
sample_width = 2  # 2 bytes (16-bit audio)

# ADC and voltage conversion constants
v_ref = 3.0  # Reference voltage for the ADC
max_adc_value = 65535  # Maximum ADC value for a 16-bit ADC
wav_min_value = -32768
wav_max_value = 32767

buffer = bytearray()  # Buffer to accumulate data

# Phase 1: Data Acquisition - Capture Raw ADC Values and Save to Binary File
try:
    print("Starting data acquisition...")

    with open(output_bin_path, 'wb') as binfile:
        while True:
            # Read the raw binary data from the serial port
            raw_data = ser.read(2048)
            
            # Accumulate the data in the buffer
            buffer.extend(raw_data)

            # Write data in chunks to the binary file to avoid frequent I/O operations
            if len(buffer) >= 65536:  # Adjust buffer size as needed
                binfile.write(buffer)
                buffer.clear()  # Clear the buffer after writing

except KeyboardInterrupt:
    print("Data acquisition terminated by user.")
    ser.close()

    # Write any remaining data in the buffer to the file
    if buffer:
        with open(output_bin_path, 'ab') as binfile:
            binfile.write(buffer)

    # Phase 2: Post-Processing - Convert Raw Values to 16-bit, Remove DC Shift, and Save as WAV
    print("Starting WAV file creation...")

    with wave.open(output_wav_path, 'w') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)

        all_samples = []

        with open(output_bin_path, 'rb') as binfile:
            while True:
                raw_data = binfile.read(5096)
                if not raw_data:
                    break

                # Convert the raw data into a list of 16-bit values
                sixteen_bit_list = [(raw_data[i]) | (raw_data[i + 1] << 8) for i in range(0, len(raw_data), 2)]

                # Convert the raw 16-bit values to voltages
                voltage_list = [(value / max_adc_value) * v_ref for value in sixteen_bit_list]

                # Collect all samples for DC shift calculation
                all_samples.extend(voltage_list)

        # Calculate the DC shift (mean of all samples)
        dc_shift = sum(all_samples) / len(all_samples)

        # Remove DC shift and save to WAV
        for voltage in all_samples:
            # Remove the DC shift
            voltage -= dc_shift

            # Convert the voltage values to fit within the WAV file's 16-bit signed integer range
            wav_value = int((voltage / v_ref) * wav_max_value)

            # Convert the integer to bytes and write to the WAV file
            wav_file.writeframes(struct.pack('<h', wav_value))

    print("WAV file creation completed.")
