# Algorithm 1
Algorithm1 is the data processing algorithm and is designed to be run on the device receiving the radar data. 
The algorithm is design to read in a WAV file containing the traffic data using the radar setup detailed in the report pdf.
You just need to input the path to the WAV file and run the algorithm. The spectrogram of each target should be plotted as well as the 
time into the recording each target appeared.


# Algorithm 2
Algorithm2 is the data collection algorithm and is designed to be run on the device capturing the radar data, specifically a Raspberry Pi Zero W.
The soundcard must be connected to the Raspberry Pi. Make sure to set the Device index correctly. The code should print a list of devices and their indices when run.
Also make sure that the power off button has been connect to the correct GPIO pin.