#include <SPI.h>

// MCP3914 SPI Configuration
const int chipSelectPin = 10; // Choose a digital pin for the CS (Chip Select) pin

// Define Command Byte for Retrieving Security Code
//#define SECURITY_BYTE 0b01111111
#define SECURITY_BYTE 127

void setup() {
  Serial.begin(9600);
  
  // Initialize MCP3914 SPI communication
  pinMode(chipSelectPin, OUTPUT);
  digitalWrite(chipSelectPin, HIGH); // Deselect MCP3914
  SPI.begin();
  
}

void loop() {
  // Read ADC data from channel 0 (you can modify this based on your requirements)
  uint32_t adcValue = readMCP3914Channel(0);
  
  // Print the ADC value to the serial monitor
  Serial.println("ADC Value: " + String(adcValue));
  
  delay(1000); // Adjust delay as needed
}


uint32_t readMCP3914Channel(uint8_t channel) {
  // Read the 24-bit ADC value from the specified channel
  uint32_t result = 0;
  
  // Construct the command byte
  uint8_t cmdByte = SECURITY_BYTE;
  // Select MCP3914 by pulling CS low
  digitalWrite(chipSelectPin, LOW);
  
  // Send the command byte and read the 3 bytes of data
  SPI.transfer(cmdByte);
  result = SPI.transfer(0);
  

  // Deselect MCP3914 by pulling CS high
  digitalWrite(chipSelectPin, HIGH);
  
  return result;
}


