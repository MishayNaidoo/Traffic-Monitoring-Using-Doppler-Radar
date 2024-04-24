import os
import serial
import subprocess
import time
from datetime import datetime

# Function to find the path to the USB drive
def find_usb_path():
    # Run lsblk command to list block devices
    result = subprocess.run(['lsblk', '-o', 'NAME,MOUNTPOINT'], capture_output=True, text=True)
    output = result.stdout

    # Split the output by lines
    lines = output.split('\n')

    # Iterate through lines to find the USB drive
    for line in lines[1:]:
        if line:
            parts = line.split()
            print(parts)
            if len(parts) == 2 and parts[1].startswith('/media/raspberry/C'):
                return parts[1]
    return None  # Return None if USB drive not found


def record_and_save_data(usb_path, duration_seconds):
    while True:
        if usb_path:
            output_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt'
            output_file_path = os.path.join(usb_path, output_file_name)
            print("Writing output to:", output_file_path)

            ser = serial.Serial('/dev/ttyACM1', baudrate=12000000)  # Adjust 'COMx' and baudrate

            start_time = time.time()
            end_time = start_time + duration_seconds

            try:
                with open(output_file_path, 'w') as file:
                    while time.time() < end_time:
                        # Read the raw binary data from the serial port
                        raw_data = ser.read(2048)

                        # Process or reformat the received raw data
                        formatted_data = list(raw_data)

                        sixteen_bit_list = [(raw_data[i]) | (raw_data[i + 1]<<8) for i in range(0, len(raw_data), 2)]
                        # Write the formatted data to the file
                        file.write(str(sixteen_bit_list) + '\n')
                        # print(sixteen_bit_list)

                print("Data recorded successfully.")
                ser.close()

            except KeyboardInterrupt:
                print("Serial reading terminated by user.")
                ser.close()

            time.sleep(1)  # Wait for a second before starting the process again
        else:
            print("USB drive not found.")
            time.sleep(1)  # Wait for a second before checking USB path again

usb_path = find_usb_path()

duration_seconds = 60  # Replace with desired duration in seconds

record_and_save_data(usb_path, duration_seconds)