import os
import serial
import subprocess
import time
import zipfile

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
            if len(parts) == 2 and parts[1].startswith('/media/raspberry/') and not parts[1].startswith('/media/raspberry/DIS_F407VG'):
                return parts[1]
    return None  # Return None if USB drive not found

def record_data():
    usb_path = find_usb_path()

    if usb_path:
        output_file_path = os.path.join(usb_path, 'output.txt')
        print("Writing output to:", output_file_path)

        ser = serial.Serial('/dev/ttyACM1', baudrate=12000000)  # Adjust 'COMx' and baudrate

        start_time = time.time()
        duration = 60

        try:
            with open(output_file_path, 'w') as file:
                while time.time() - start_time < duration:
                    # Read the raw binary data from the serial port
                    raw_data = ser.read(2048)

                    # Process or reformat the received raw data
                    formatted_data = list(raw_data)

                    sixteen_bit_list = [(raw_data[i]) | (raw_data[i + 1]<<8) for i in range(0, len(raw_data), 2)]
                    # Write the formatted data to the file
                    file.write(str(sixteen_bit_list) + '\n')
                    # print(sixteen_bit_list)

        except KeyboardInterrupt:
            print("Serial reading terminated by user.")
            ser.close()

        # Zip the output file
        zip_file_path = os.path.join(usb_path, 'output.zip')
        with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            zipf.write(output_file_path, os.path.basename(output_file_path))

        # Delete the original output file
        os.remove(output_file_path)


        print("Output file zipped and original deleted.")

    else:
        print("USB drive not found.")

# Run the record_data function
record_data()
