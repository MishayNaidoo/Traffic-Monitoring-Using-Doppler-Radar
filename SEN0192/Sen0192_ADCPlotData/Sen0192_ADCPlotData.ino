const int analogPin = A0; // Define the analog input pin
const int numSamples = 100; // Define the number of samples to collect
int analogData[numSamples]; // Array to store the collected data
int sampleIndex = 0; // Index to keep track of the current sample
int count = 0;

void setup() {
  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  // Read analog data from the ADC pin
  int sensorValue = analogRead(analogPin);

  // Store the data in the array
  analogData[sampleIndex] = sensorValue;
  sampleIndex++;

  // Check if we have collected enough samples
  if (sampleIndex == numSamples && count < 30) {
    // Export the data through the serial port
    for (int i = 0; i < numSamples; i++) {
      Serial.print(analogData[i]);
      Serial.print(","); // Add a comma as a separator
    }
    Serial.println(); // Print a newline character to indicate the end of the data
    //delay(2000);
    // Reset the sampleIndex to start collecting data again
    sampleIndex = 0;
    count++;
  }

  // You can add a delay here to control the sampling rate if needed
  // delay(100); // Uncomment this line to add a delay between samples
}