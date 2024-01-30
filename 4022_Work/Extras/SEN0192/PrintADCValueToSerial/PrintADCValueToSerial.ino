void setup() {
  // Initialize the Serial communication at 9600 baud
  Serial.begin(115200);
}

void loop() {
  // Read the analog value from pin A0
  int sensorValue = analogRead(A0);
  Serial.println(sensorValue);
  Serial.println(millis());
}
