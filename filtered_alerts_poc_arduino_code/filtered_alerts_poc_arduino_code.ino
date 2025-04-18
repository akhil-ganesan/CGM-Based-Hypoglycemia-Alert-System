const float filter_alpha = 0.5;
volatile float prior_in = -1;
const int pinBuzzer = 12; // Buzzer Pin
volatile float startTime = 0; 
  
void setup() {
  Serial.begin(9600); 
  pinMode(pinBuzzer,OUTPUT);
  startTime = millis();  
}

void loop () {
  int time = millis() - startTime;
  int real_cgm = (30) * (sin(time * 2 * PI / 3000)) + 54; // 3 second repeat period; on for 1 sec & off for 2 sec
  int noise = random(0,30);
  int in = real_cgm + noise;

  // Filter if prior > 0; it's negative if first input data point is read
  if (prior_in > 0) {
    int temp = in;
    in = filter(in, prior_in, filter_alpha);
    prior_in = temp;
  } else {
    prior_in = in;
  }
  Serial.println("Readings");
  Serial.println(real_cgm);
  Serial.println(prior_in);
  Serial.println(in);

  if (in <= 54) {
    tone(pinBuzzer, 10);
  } else {
    noTone(pinBuzzer);
  }

  delay(1000);
}

int filter(float input, float prior, float a) {
  return input * a + (1 - a) * prior;
}


