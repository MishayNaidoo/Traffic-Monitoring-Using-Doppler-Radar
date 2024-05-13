import serial

ser = serial.Serial('COM7', baudrate=12000000)  # Adjust 'COMx' and baudrate

try:
    with open('E:/UCT/Masters/Traffic-Monitoring-Using-Doppler-Radar/ADC/output.txt', 'wb') as file:  # Use binary mode for writing raw data
        while True:
            # Read the raw binary data from the serial port
            raw_data = ser.read(1024)  

            # Write the raw data to the file
            file.write(raw_data)
            file.flush()  # Flush the buffer to ensure data is written immediately
            #print("Data written to file")

except KeyboardInterrupt:
    print("Serial reading terminated by user.")
    ser.close()

