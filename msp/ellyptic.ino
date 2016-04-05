
#define PIN P2_3
#define PIN_IN P2_5

volatile byte state = HIGH;
volatile boolean got_data = false;
volatile unsigned long prev = 0;
volatile unsigned int dt = 0;

byte lvl = 1;
boolean in_read = false;

void setup() {
  Serial.begin(9600);
  pinMode(RED_LED, OUTPUT);
  pinMode(PIN, INPUT_PULLUP);
  pinMode(PIN_IN, INPUT_PULLUP);
  attachInterrupt(PIN, int_, FALLING);
  delay(500);
}

void loop() {
    if (got_data) {
      got_data = false;
      Serial.print(lvl);
      Serial.print(";");
      Serial.print(dt);
      Serial.println();
    }
    if (digitalRead(PIN_IN) == LOW) {
        byte new_l = read_data();
        if (new_l != lvl) {
            lvl = new_l;
        }
        delay(10);
    }
}

byte read_data() {
    byte res = 0;
    delay(4);
    for(byte i=0; i<5; i++) {
        long l = millis();
        byte a = digitalRead(PIN_IN);
        res = (res << 1) + a;
        delay(10 - (millis()-l));
    }
    return res + 1;
}

void int_() {
  unsigned long p = prev;
  if (millis() - p > 200) {
    state = ! state;
    digitalWrite(RED_LED, state);
    prev = millis();
    if (p != 0) {
      got_data = true;
      dt = prev - p;
    }
  }
}
