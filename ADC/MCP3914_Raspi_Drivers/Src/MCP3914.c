#include "MCP3914.h"


/*
    INITIALISE STRUCT
*/

void MCP3914_Initialise(MCP3914 *dev, SPI_HandleTypeDef *spiHandle, GPIO_TypeDef *Port, uint16_t Pin){

    dev->spiHandle  =   spiHandle;
    dev->Port       =   Port;
    dev->Pin        =   Pin;
    dev->adcData[0] =   0x00;
    dev->adcData[1] =   0x00;
    dev->adcData[2] =   0x00;

    uint8_t MCP3914_CONFIG1_CLKINTEN[3] =   {0x00, 0x00, 0x00}; //WRITE THIS TO CONFIG1 TO ENABLE INTERNAL CLOCK

    MCP3914_WriteRegister(dev, MCP3914_REG_CONFIG1, MCP3914_CONFIG1_CLKINTEN); //ENABLES INTERNAL CLOCK

}


/*
    LOW LEVEL FUNCTIONS
*/

void MCP3914_ReadRegister(MCP3914 *dev, uint8_t reg){
    uint8_t REG = 0x41 | (reg << 1);
    uint8_t sendData[4] = {REG, 0x00, 0x00, 0x00};
    uint8_t receiveData[4];

    HAL_GPIO_WritePin(dev->Port, dev->Pin, GPIO_PIN_RESET); //enable SPI by setting CS low
    HAL_SPI_TransmitReceive(dev->spiHandle, sendData, receiveData, 4, HAL_MAX_DELAY);
    HAL_GPIO_WritePin(dev->Port, dev->Pin, GPIO_PIN_SET); //disable SPI by setting CS high

    dev->adcData[0] =   receiveData[1];
    dev->adcData[1] =   receiveData[2];
    dev->adcData[2] =   receiveData[3];
}

void MCP3914_WriteRegister(MCP3914 *dev, uint8_t reg, uint8_t *data){
    uint8_t REG = 0x40 | (reg << 1);
    uint8_t sendData[4] = {REG, data[0], data[1], data[2]};

    HAL_GPIO_WritePin(dev->Port, dev->Pin, GPIO_PIN_RESET); //enable SPI by setting CS low
    HAL_SPI_Transmit(dev->spiHandle, sendData, 4, HAL_MAX_DELAY);
    HAL_GPIO_WritePin(dev->Port, dev->Pin, GPIO_PIN_SET); //disable SPI by setting CS high    

}