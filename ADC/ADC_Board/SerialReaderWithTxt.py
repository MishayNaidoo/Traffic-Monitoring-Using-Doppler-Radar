import serial

ser = serial.Serial('COM7', baudrate=12000000)  # Adjust 'COMx' and baudrate

try:
    with open('E:/UCT/Masters/Traffic-Monitoring-Using-Doppler-Radar/ADC/ADC_Board/output.txt', 'w') as file:
        while True:
            # Read the raw binary data from the serial port
            raw_data = ser.read(2048)

            # Convert the raw data into a list of 16-bit values
            sixteen_bit_list = [(raw_data[i]) | (raw_data[i + 1] << 8) for i in range(0, len(raw_data), 2)]

            # Write each 16-bit value on a new line in the file
            for value in sixteen_bit_list:
                file.write(f'{value}\n')

            # Optionally, print the values to the console
            print(sixteen_bit_list)

except KeyboardInterrupt:
    print("Serial reading terminated by user.")
    ser.close()
