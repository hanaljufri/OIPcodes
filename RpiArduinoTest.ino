/* communication between Arduino (slave) and Raspberry Pi (master) testing script
 *  For I2C communication master (Rpi) has to initiate the conversation with slave (Arduino)
 *  Script will light up 3 different LEDs when Arduino receive command from Rpi 
 *  When Rpi request status of button, Arduino can send ON/OFF status

 *  written by Wei Jun
 *  version 1 23 August 2021*/
 
#include <Wire.h>

#define BUTTON 13 //set pin 13 for button 

const int redLed = 8; //set pin 8 as LED Pin
const int yellowLed = 9; //set pin 9 as LED Pin
const int greenLed = 10; //set pin 10 as LED Pin

 
void setup() {
  // Join I2C bus as slave with address 8
  Wire.begin(0x8);
  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  // Call requestEvent when data is requested from master     
  Wire.onRequest(requestEvent);

  //Set Button pin to Pull-Up configuration
  pinMode(BUTTON, INPUT_PULLUP);
  
  // Setup ledPin1 as output and turn LED off
  pinMode(redLed, OUTPUT);
  pinMode(yellowLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  
  digitalWrite(redLed, LOW);
  digitalWrite(yellowLed, LOW);
  digitalWrite(greenLed, LOW);
}
 
// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
    int inData = Wire.read(); // receive byte as an integer
    
    if (inData == 1) {
    digitalWrite(redLed, HIGH);
    delay(1000);
    digitalWrite(redLed, LOW);
    }
    else if (inData == 2) {
    digitalWrite(yellowLed, HIGH);
    delay(1000);
    digitalWrite(yellowLed, LOW);
    }
    else if (inData == 3) {
    digitalWrite(greenLed, HIGH);
    delay(1000);
    digitalWrite(greenLed, LOW);
    }
}

// Function that executes whenever data is requested from master
void requestEvent()
{
  //check button status
  //if LOW write 4 to I2C
    if (digitalRead(BUTTON) == LOW){
        Wire.write(4);
        }
  //if HIGH  write 5 to I2C
    else if (digitalRead(BUTTON) == HIGH){ 
        Wire.write(5);
       }  
}
