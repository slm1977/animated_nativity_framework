#include <SoftwareSerial.h>
SoftwareSerial mySerial (4,2); // Rx, Tx
String command = ""; // response from HC-06

void setup() {
pinMode(13,OUTPUT);
digitalWrite(13,HIGH);
Serial.begin(9600);
Serial.println("Type AT command");
// default hc06 baud rate
mySerial.begin(9600);
}

void loop(){
// Read device output if available
//Serial.println("check serial availability...");
if (mySerial.available()) {
  Serial.println("serial data available!");
  while (mySerial.available()) 
  { command += (char) mySerial.read();
  
  }
  Serial.println(command);
  if (command=="led_on")
  { digitalWrite(13,HIGH);
     mySerial.println("led_on ok");
  }
  else if (command=="led_off")
  { digitalWrite(13,LOW);
    mySerial.println("led_on ok");
  }
  command = "";
}

// Read the input if available
if(Serial.available()){
  delay(10);
  mySerial.write(Serial.read());
}

}
