#if defined(ARDUINO) 
SYSTEM_MODE(MANUAL); 
#endif

const int sound = D3; // right thumb
int sound_state = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(sound, INPUT_PULLDOWN);
}

void loop() {
  // put your main code here, to run repeatedly:
  sound_state = digitalRead(sound);
  Serial.println(sound_state);
  if (sound_state) {
    Serial.println("button pressed");
  } else {
    Serial.println("button not pressed");
  }
  delay(200);
}
