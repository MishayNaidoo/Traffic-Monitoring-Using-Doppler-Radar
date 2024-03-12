import numpy as np
import matplotlib.pyplot as plt

# Reference voltage for the ADC (replace with your actual Vref)
Vref = 3

# Sampling rate
sampling_rate = 120000  # samples per second

# Step 1: Read ADC Samples from a Text File
with open('E:/UCT/Masters/Traffic-Monitoring-Using-Doppler-Radar/ADC/output.txt', 'r') as file:
    lines = file.readlines()

# Convert the text data to a list of integers
adc_samples = [eval(sample.strip()) for sample in lines]
adc_samples = [item for sublist in adc_samples for item in sublist]

#print(adc_samples)
# Step 2: Convert ADC Values to Voltages
voltages = [(sample / 4095) * Vref for sample in adc_samples]

# Step 3: Create a time axis
time_axis = np.arange(0, len(voltages)) / sampling_rate

# Step 4: Plot the Data
plt.plot(time_axis[:], voltages[:])
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage (V)')
plt.title('ADC Data Plot (Voltage) over Time')
plt.show()

