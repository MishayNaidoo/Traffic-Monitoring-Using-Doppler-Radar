import serial

ser = serial.Serial('/dev/ttyACM2', baudrate=12000000)  # Adjust 'COMx' and baudrate

prev_val = 0
try:
    with open('/home/mishay/Traffic-Monitoring-Using-Doppler-Radar/ADC/output.txt', 'w') as file:
        while True:
            # Read the raw binary data from the serial port
            raw_data = ser.read(12)  

            # Process or reformat the received raw data
            formatted_data = []

            # Combine every 3 bytes into one 24-bit value
            for i in range(0, len(raw_data), 3):
                # Combine 3 bytes into one 24-bit integer (little-endian)
                value = (raw_data[i+2]) | (raw_data[i + 1] << 8) | (raw_data[i] << 16)
                formatted_data.append(value/16777216*1.2)

            # Write the formatted data to the file
            for value in formatted_data:
                #if (value != prev_val):
                file.write(str(value) + '\n')
                    #prev_val = value
            print(formatted_data)

except KeyboardInterrupt:
    print("Serial reading terminated by user.")
    ser.close()


