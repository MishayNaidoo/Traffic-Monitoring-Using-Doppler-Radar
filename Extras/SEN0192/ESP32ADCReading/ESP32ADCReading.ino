void setup() {
  // Start serial communication
  Serial.begin(250000);

  // Initialize the ADC
  analogReadResolution(12); // Set the ADC resolution to 12 bits (0-4095)
}

void loop() {
  // Read the analog value from ADC pin (e.g., GPIO 36 in this example)
  int sensorValue = analogRead(36); // Change the pin number as needed

  Serial.println(sensorValue);

}
