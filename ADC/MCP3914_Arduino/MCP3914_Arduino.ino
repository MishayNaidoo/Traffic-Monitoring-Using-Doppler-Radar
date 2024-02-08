#include <SPI.h>

// MCP3914 SPI Configuration
const int chipSelectPin = 10; // Choose a digital pin for the CS (Chip Select) pin


// MCP3914 Memory Addresses
#define MCP3914_REG_CONFIG0   13
#define MCP3914_REG_CHANNEL_BASE  0



void setup() {
  Serial.begin(9600);
  
  // Initialize MCP3914 SPI communication
  pinMode(chipSelectPin, OUTPUT);
  digitalWrite(chipSelectPin, HIGH); // Deselect MCP3914
  SPI.begin();
  
  // Initialize MCP3914 (you might need to configure other settings based on your requirements)
  initializeMCP3914();
}

void loop() {
  // Read ADC data from channel 0 (you can modify this based on your requirements)
  uint32_t adcValue = readMCP3914Channel(0);
  
  // Print the ADC value to the serial monitor
  Serial.println("ADC Value: " + String(adcValue));
  
  delay(1000); // Adjust delay as needed
}

void initializeMCP3914() {
  // Configure MCP3914 as needed (you might need to adjust these configurations)
  // For example, you can set the MCP3914_CONF_START bit in the CONFIG1 register to start conversions.
  
  // Example: Set OSR to 256 with temp comp
  writeMCP3914Register(MCP3914_REG_CONFIG0, MCP3914_CONF_OSR256);
}

uint32_t readMCP3914Channel(uint8_t channel) {
  // Read the 24-bit ADC value from the specified channel
  uint32_t result = 0;
  
  // Construct the command byte
  uint8_t cmdByte = MCP3914_CONST_ADDR | MCP3914_READ | MCP3914_REG_CHANNEL_BASE | channel;
  // Select MCP3914 by pulling CS low
  digitalWrite(chipSelectPin, LOW);
  
  // Send the command byte and read the 3 bytes of data
  SPI.transfer(cmdByte);
  result |= SPI.transfer(0) << 16;
  result |= SPI.transfer(0) << 8;
  result |= SPI.transfer(0);
  
  // Deselect MCP3914 by pulling CS high
  digitalWrite(chipSelectPin, HIGH);
  
  return result;
}

void writeMCP3914Register(uint8_t reg, uint32_t data) {
  // Write a 24-bit value to the specified register
  // Note: This assumes that the register is 3 bytes wide
  
  // Construct the command byte
  uint8_t cmdByte = MCP3914_CONST_ADDR | MCP3914_WRITE | reg;
  
  // Select MCP3914 by pulling CS low
  digitalWrite(chipSelectPin, LOW);
  
  // Send the command byte
  SPI.transfer(cmdByte);
  
  // Send the 3 bytes of data
  SPI.transfer((data >> 16) & 0xFF);
  SPI.transfer((data >> 8) & 0xFF);
  SPI.transfer(data & 0xFF);
  
  // Deselect MCP3914 by pulling CS high
  digitalWrite(chipSelectPin, HIGH);
}
