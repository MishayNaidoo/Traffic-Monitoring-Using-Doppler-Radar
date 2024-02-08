#include <wiringPiSPI.h>
#include <stdio.h>
#include <unistd.h>

// Define SPI channel and speed
#define spiChannel  0
#define spiSpeed  18000000  // 18 MHz

// Define MCP3914 command bytes
#define MCP3914_READ 0x05  // Read command byte
#define MCP3914_CONFIG 0x10  // Configuration command byte
#define SECURITY_BYTE 0b01111111 // Command to retreive the security byte

// Define configuration settings for MCP3914
const unsigned char MCP3914_CONFIG_SETTINGS[] = {0x20, 0x20, 0x00};  // Example configuration settings

int main() {
    // Initialize SPI
    wiringPiSPISetup(spiChannel, spiSpeed);

    // Send configuration settings to MCP3914
    unsigned char configTxData[4] = {MCP3914_CONFIG, MCP3914_CONFIG_SETTINGS[0], MCP3914_CONFIG_SETTINGS[1], MCP3914_CONFIG_SETTINGS[2]};
    wiringPiSPIDataRW(spiChannel, configTxData, sizeof(configTxData));

    while (1) {
        // Send read command to MCP3914
        unsigned char readTxData[1] = {SECURITY_BYTE};
        unsigned char readRxData[3] = {0};

        // Send and receive data
        wiringPiSPIDataRW(spiChannel, readTxData, sizeof(readTxData));
        
        // Receive ADC data
        wiringPiSPIDataRW(spiChannel, nullptr, 0);  // Dummy write to trigger SPI transfer
        wiringPiSPIDataRW(spiChannel, nullptr, 0);  // Dummy write to trigger SPI transfer
        wiringPiSPIDataRW(spiChannel, readRxData, sizeof(readRxData));

        // Combine received bytes into a 24-bit ADC value
        unsigned int adcValue = ((readRxData[0] << 16) | (readRxData[1] << 8) | readRxData[2]) & 0xFFFFFF;

        // Print the ADC value
        printf("ADC Value: %u\n", adcValue);

        // Wait for a moment
        usleep(1000000);
    }

    return 0;
}
