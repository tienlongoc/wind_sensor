int numOfSwitches = 0;
bool switchRegister = false;
unsigned long time = millis();

void setup() {
  //start serial connection
  Serial.begin(9600);
  //configure pin 2 as an input and enable the internal pull-up resistor
  pinMode(2, INPUT_PULLUP);
}
  

void loop() {
  
  //read the pushbutton value into a variable
  int sensorVal = digitalRead(2);

  if (switchRegister != sensorVal)
  {
    switchRegister = sensorVal;
    numOfSwitches++;
  }

  if (millis() - time >= 60000)
  {
    Serial.write(numOfSwitches);
    time = millis();
    numOfSwitches = 0;
  }


}
