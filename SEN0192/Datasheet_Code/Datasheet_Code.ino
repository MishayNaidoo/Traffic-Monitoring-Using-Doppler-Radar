/*!
 * @file  microwaveSensor.ino
 * @brief  This example reads temperature and humidity from SHT1x Humidity and Temperature Sensor.
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license  The MIT License (MIT)
 * @author  Loan <Loan.he@dfrobot.com>
 * @version  V1.0
 * @date  2015-7-30
 */

/***********Notice and Trouble shooting***************
  1.Connection and Diagram can be found here
<https://wiki.dfrobot.com.cn/_SKU_SEN0192__Microwave_sensor%E5%BE%AE%E6%B3%A2%E4%BC%A0%E6%84%9F%E5%99%A8%E6%A8%A1%E5%9D%97>
  2.This code is tested on Arduino Uno, Leonardo, Mega boards.
  3.arduino Timer library is created by jonoxer.
  See <https://www.dfrobot.com.cn/images/upload/File/SEN0192/20160112134309yy5nus.zip arduino Timer library> for details.
 ****************************************************/
#include <MsTimer2.h>           //Timer interrupt function
int pbIn = 0;                   // Define the interrupt PIN is 0, that is, digital pins 2
int ledOut = 13;
int count = 0;
volatile int state = LOW;       //Define ledOut, default is off

void setup()
{
  Serial.begin(9600);
  pinMode(ledOut, OUTPUT);
  attachInterrupt(pbIn, stateChange, FALLING); // Sets the interrupt function, falling edge triggered interrupts.
  MsTimer2::set(1000, process); // Set the timer interrupt time 1000ms
  MsTimer2::start();//Timer interrupt start

}

void loop()
{
  Serial.println(count); // Printing times of 1000ms suspension
  delay(1);
  if (state == HIGH) //When moving objects are detected later, 2s shut down automatically after the ledout light is convenient.
  {
    delay(2000);
    state = LOW;
    digitalWrite(ledOut, state);    //Turn off led
  }

}


void stateChange()  //Interrupt function
{
  count++;

}

void process()   //Timer handler
{
  if (count > 100000000) //1000ms interrupt number greater than 1 is considered detected a moving object (this value can be adjusted according to the actual situation, equivalent to adjust the detection threshold of the speed of a moving object)
  {
    state = HIGH;
    digitalWrite(ledOut, state);    //Lighting led
    count = 0; //Count zero

  }
  else
    count = 0; //In 1000ms, interrupts does not reach set threshold value is considered not detect moving objects, interrupt the count number is cleared to zero.
}
