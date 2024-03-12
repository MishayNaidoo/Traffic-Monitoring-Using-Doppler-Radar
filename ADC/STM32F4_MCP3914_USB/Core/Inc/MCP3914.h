#ifndef MCP3914_SPI_DRIVER_H
#define MCP3914_SPI_DRIVER_H

#include "stm32f4xx_hal.h"

/*
    DEFINES
*/

#define MCP3914_DEVICE_ID   0x1


/*
    REGISTERS
*/

#define MCP3914_REG_CHANNEL_0       0x00
#define MCP3914_REG_CHANNEL_1       0x01
#define MCP3914_REG_CHANNEL_2       0x02
#define MCP3914_REG_CHANNEL_3       0x03
#define MCP3914_REG_CHANNEL_4       0x04
#define MCP3914_REG_CHANNEL_5       0x05
#define MCP3914_REG_CHANNEL_6       0x06
#define MCP3914_REG_CHANNEL_7       0x07
#define MCP3914_REG_MOD             0x08
#define MCP3914_REG_PHASE0          0x09
#define MCP3914_REG_PHASE1          0x0A
#define MCP3914_REG_GAIN            0x0B
#define MCP3914_REG_STATUSCOM       0x0C
#define MCP3914_REG_CONFIG0         0x0D
#define MCP3914_REG_CONFIG1         0x0E
#define MCP3914_REG_OFFCAL_CH0      0x0F
#define MCP3914_REG_GAINCAL_CH0     0x10
#define MCP3914_REG_OFFCAL_CH1      0x11
#define MCP3914_REG_GAINCAL_CH1     0x12
#define MCP3914_REG_OFFCAL_CH2      0x13
#define MCP3914_REG_GAINCAL_CH2     0x14
#define MCP3914_REG_OFFCAL_CH3      0x15
#define MCP3914_REG_GAINCAL_CH3     0x16
#define MCP3914_REG_OFFCAL_CH4      0x17
#define MCP3914_REG_GAINCAL_CH4     0x18
#define MCP3914_REG_OFFCAL_CH5      0x19
#define MCP3914_REG_GAINCAL_CH5     0x1A
#define MCP3914_REG_OFFCAL_CH6      0x1B
#define MCP3914_REG_GAINCAL_CH6     0x1C
#define MCP3914_REG_OFFCAL_CH7      0x1D
#define MCP3914_REG_GAINCAL_CH7     0x1E
#define MCP3914_REG_LOCKCRC         0x1F





/*
    ADC STRUCT
*/
typedef struct{

    SPI_HandleTypeDef *spiHandle;
    GPIO_TypeDef *Port;
    uint16_t Pin;

    uint8_t adcData[3];

} MCP3914;

/*
    INITIALISATION
*/
void MCP3914_Initialise(MCP3914 *dev, SPI_HandleTypeDef *spiHandle, GPIO_TypeDef *Port, uint16_t Pin);


/*
    DATA ACQUISITION
*/
void MCP3914_ReadRegister(MCP3914 *dev, uint8_t reg);
void MCP3914_WriteRegister(MCP3914 *dev, uint8_t reg, uint8_t *data);


#endif