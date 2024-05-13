import serial


ser = serial.Serial('COM7', baudrate=12000000)  # Adjust 'COMx' and baudrate

try:
    with open('E:/UCT/Masters/Traffic-Monitoring-Using-Doppler-Radar/ADC/output.txt', 'w') as file:
        while True:
            # Read the raw binary data from the serial port
            raw_data = ser.read(1024)  

            # Process or reformat the received raw data
            formatted_data = list(raw_data)

            sixteen_bit_list = [(raw_data[i]) | (raw_data[i + 1]<<8) for i in range(0, len(raw_data), 2)]
            # Write the formatted data to the file
            file.write(str(sixteen_bit_list) + '\n')
            print(sixteen_bit_list)

except KeyboardInterrupt:
    print("Serial reading terminated by user.")
    ser.close()






