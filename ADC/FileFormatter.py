# Function to format unformatted data
def format_data(unformatted_data):
    # Split the data into a list of hexadecimal values
    hex_values = unformatted_data.split()

    # Convert hexadecimal values to decimal integers
    decimal_values = [int(hex_value, 8) for hex_value in hex_values]

    # Format the data as needed
    formatted_data = " ".join(map(str, decimal_values))

    return formatted_data

# Specify the path to the unformatted data file
input_file_path = 'E:/UCT/Masters/Traffic-Monitoring-Using-Doppler-Radar/ADC/unformattedData.txt'

# Specify the path for the formatted data output file
output_file_path = 'E:/UCT/Masters/Traffic-Monitoring-Using-Doppler-Radar/ADC/formattedData.txt'

try:
    # Open the unformatted data file and read its content
    with open(input_file_path, 'r') as input_file:
        unformatted_data = input_file.read()

    # Format the data
    formatted_data = format_data(unformatted_data)

    # Write the formatted data to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(formatted_data)

    print("Data formatted successfully. Formatted data saved to", output_file_path)

except FileNotFoundError:
    print(f"Error: File '{input_file_path}' not found.")

except Exception as e:
    print(f"An error occurred: {e}")
