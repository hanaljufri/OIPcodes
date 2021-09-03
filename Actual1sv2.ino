/* Complete code to do automation 
 *  Rpi(master) has to initiate communication with Arduino(slave)
 *  Rpi will send Arduino information
 *  Arduino will call washdrysterilize(), washdry() or sterilize()*/

#include <Wire.h>
#include <Stepper.h>

/*pic_status changing from 5 to 6 will signal Rpi to take picture and do ML; 
 * i is a counter to ensure spinning of the cylinder holder one complete round to take picture*/
int pic_status = 5;
int i = 0;
int read_status = 0;
int done_status = 0;

//interval delay between sv1 on and off; 10s
int delay1 = 1000;

//interval delay between sv1 on and off; 20s
int delay2 = 1000;

//interval delay between inlet off and outlet off; 15s
int delay3 = 1000;

//interval delay between fan on and off; 10s
int delay4 = 1000;

//interval delay betweem LED on and off; 10s
int delay5 = 1000;

//digital pins controlling each electronic component
int sv1 =2;
int sv2 =3;
int fan = 4;
int LED = 5;
int stepper = 6;

//motor
int stepsPerRevolution =2048;
Stepper myStepper(stepsPerRevolution,8,10,9,11);
int motSpeed = 10;



void setup() {
  //print to Serial monitor for checking
  Serial.begin(9600);
  Serial.println("Start");

  // Join I2C bus as slave with address 8
  Wire.begin(0x7);
  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  // Call requestEvent when data is requested from master     
  Wire.onRequest(requestEvent);

  //set motor speed
  myStepper.setSpeed(motSpeed);

  //define pinMode
  pinMode(sv1, OUTPUT);
  pinMode(sv2, OUTPUT);
  pinMode(fan, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(stepper, OUTPUT);

  digitalWrite(sv1, LOW);
  digitalWrite(sv2, LOW);
  digitalWrite(fan, LOW);
  digitalWrite(LED, LOW);
  digitalWrite(stepper, LOW);
}

void loop() {
  if(read_status == 1){
    read_status = 0;
    //washdrysterilize and check for cleanliness
    wash();
    dry();
    sterilize();
    pic_status = 6;
    }

  else if(read_status == 2){
     read_status = 0;
    //washdry
    wash();
    dry();
    pic_status = 6;
   
    }
    
  else if(read_status == 3){
     read_status = 0;
    //sterilize
    sterilize();
    pic_status = 6;
    }
    
  else if(read_status == 4){
    read_status = 0;
    pic_status = 5;
    rotate();
    
  }
    
   
   
}

/*interrupt function when receive info from Rpi*/

void receiveEvent(int howMany) {
    int x = Wire.read(); // receive byte as an integer
    Serial.println(x);         // print the integer
    read_status = x;
}

/*interrupt function to send info to Rpi*/
void requestEvent()
{
  //check button status
  //if pic_status == 5 write 5 to I2C
    if (pic_status == 5){
        Wire.write(5);
        }
  //if pic_status == 6 write 6 to I2C
    else if (pic_status == 6){ 
        Wire.write(6);
       }
}
//Functions
void wash(){
//filling with water
    digitalWrite(sv1, HIGH);
    delay(delay1);
    digitalWrite(sv1, LOW);

  //<need to inform Rpi to show on LCD to ask user to on ultrasonic>
  //<Rpi to inform Arduino that ultrasonic is done>

  //rinsing everything
    digitalWrite(sv2, HIGH);
    digitalWrite(sv1, HIGH);
    delay(delay2);
    digitalWrite(sv1, LOW);
    delay(delay3);
    digitalWrite(sv2, LOW);
}

void dry(){
  //dry
    digitalWrite(fan, HIGH);
    delay(delay4);
    digitalWrite(fan, LOW);
}

void sterilize(){
  //sterilize
    digitalWrite(LED, HIGH);
    delay(delay5);
    digitalWrite(LED, LOW);
}

void rotate(){
   //rotate stepper motor 
  if(i<9){
      digitalWrite(stepper,HIGH);
      myStepper.step(stepsPerRevolution/10);
      i= i+1;
      pic_status =6;
    }
   else if(i==9){
       myStepper.step(stepsPerRevolution/10);
       digitalWrite(stepper,LOW);
       i = 0;
    }
}
