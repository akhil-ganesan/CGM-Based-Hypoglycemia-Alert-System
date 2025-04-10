
const int pinBuzzer = 12; //Buzzer Pin
       
void setup() {
  Serial.begin(9600); 
  pinMode(pinBuzzer,OUTPUT); 

}

void loop () {
  int button; 
  int cgm = random(40,100);
  Serial.println(cgm);

  if (cgm <= 54) {
   tone(pinBuzzer, 100);
  } else {
    noTone(pinBuzzer);
  }
  delay(1000);
}