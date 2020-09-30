/*
 * outputLog
 *
 * portIndex must be set to the port connected to the Arduino
 * read signal from Arduino and save to windspeed log
 * Press any key to stop logging
 */

import processing.serial.*;


PrintWriter output;
String fileName = "testlog.txt";

Serial myPort;        // Create object from Serial class
short portIndex = 0;  // select the com port, 0 is the first port
char HEADER = 'H';

void setup()
{
  size(200, 200);
  // Open whatever serial port is connected to Arduino.
  String portName = Serial.list()[portIndex];
  println(Serial.list());
  println(" Connecting to -> " + Serial.list()[portIndex]);
  myPort = new Serial(this, portName, 9600);
  output = createWriter(fileName); // save the file in the sketch folder
}

void draw()
{
  int val;

  if ( myPort.available() >= 15)  // wait for the entire message to arrive
  {
    if( myPort.read() == HEADER) // is this the header
    {
      
      val = readArduinoInt();
      // print the value of each bit
      for(int pin=2, bit=1; pin <= 13; pin++){
        print("digital pin " + pin + " = " );
        output.print("digital pin " + pin + " = " );
        int isSet = (val & bit);
        if( isSet == 0){
           println("0");
           output.println("0");
        }
        else  {
          println("1");
          output.println("0");
        }
        bit = bit * 2; // shift the bit
      }
    }
  }
}

void keyPressed() {
  output.flush(); // Writes the remaining data to the file
  output.close(); // Finishes the file
  exit(); // Stops the program
}

// return the integer value from bytes received on the serial port (in low,high order)
int readArduinoInt()
{
  int val;      // Data received from the serial port

  val = myPort.read();          // read the least significant byte
  val =  myPort.read() * 256 + val; // add the most significant byte
  return val;
}
