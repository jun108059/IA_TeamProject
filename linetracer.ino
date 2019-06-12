#include <SoftwareSerial.h>
#include <AFMotor.h>
AF_DCMotor motor_L(3);
AF_DCMotor motor_R(4); 
int incoming_state =0;
void setup() {
  Serial.begin(9600);           
  motor_L.setSpeed(1000);            
  motor_L.run(RELEASE);
  motor_R.setSpeed(1000);         
  motor_R.run(RELEASE);
}

void loop() {
    int val1 = digitalRead(A0);    
    int val2 = digitalRead(A5);     
    if(Serial.available() >0){
    incoming_state = Serial.read() - '0';
      if (incoming_state ==1){
        motor_L.run(RELEASE); 
        motor_R.run(RELEASE);
      }
      else{
        if (val1 == 0 && val2 == 0) {               
          motor_L.run(FORWARD); 
          motor_R.run(FORWARD);
      }
      else if (val1 == 0 && val2 == 1) {             
       motor_L.run(FORWARD); 
       motor_R.run(RELEASE);
      }
      else if (val1 == 1 && val2 == 0) {            
        motor_L.run(RELEASE); 
        motor_R.run(FORWARD);
      } 
      else if (val1 == 1 && val2 == 1) {            
        motor_L.run(RELEASE); 
        motor_R.run(RELEASE);
      }           
}
}
}


