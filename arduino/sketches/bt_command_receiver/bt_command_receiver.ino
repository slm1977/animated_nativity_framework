#include <SoftwareSerial.h>

SoftwareSerial mySerial (4,2); // Rx, Tx 

String command = "";

void doCommand(String cmd) {
    Serial.println("Command to Send:" + cmd);
    
    char cmdType = cmd.charAt(0);
    int pin = cmd.substring(1,cmd.indexOf(",")).toInt();
    int pinValue = cmd.substring(cmd.indexOf(",")+1).toInt();
    Serial.println("Cmd Type:" + String(cmdType));
    Serial.println("Cmd Pin:" + String(pin));
    Serial.println("Cmd Value:" + String (pinValue));
    
    Serial.println("");
    
    if (cmdType=='D')
       { 
         if (pinValue>0)
         digitalWrite(pin,HIGH);
         else
         digitalWrite(pin,LOW);
       }
       else if (cmdType=='A')
       {
         analogWrite(pin, pinValue);
       }
   }

void setup() {

   // Open serial communications and wait for port to open:
  Serial.begin(9600);
  
  // default hc06 baud rate
  mySerial.begin(9600);
  
  pinMode(8, OUTPUT);
  pinMode(10, OUTPUT);
  Serial.println("BT Command Receiver started.");
  
}

void loop()
{
	
	
	if (mySerial.available()) 
		{
		  Serial.println("serial data available!");
			  while (mySerial.available()) 
				  { 
				  char charReaded =  (char) mySerial.read();
				     if (charReaded=='|')
				     {
				    	 doCommand(command);
				    	 command = "";
				     }
				     else
				     {
					  command += charReaded;
				     }
				     Serial.println("Partial Command:" + command);
				  }
 
			  
     Serial.println();
     //String cmd = String(command).substring(0,numBytes);
     //doCommand(command);
   }
   
  
}
