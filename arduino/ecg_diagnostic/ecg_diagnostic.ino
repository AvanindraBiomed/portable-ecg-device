/*
  ============================================================
  PORTABLE ECG DEVICE — Diagnostic Sketch
  ============================================================
  Use this sketch to troubleshoot signal issues.
  Prints: RAW value, LO+ state, LO- state, running MIN, MAX
  Open Serial Monitor (not Plotter) at 115200 baud.

  MIN/MAX resets every 5 seconds to show recent signal range.
  If MIN and MAX are close together → signal is stuck/railed.
  If MIN and MAX are far apart → signal is moving (good).
  ============================================================
*/

const int ECG_PIN  = A0;
const int LO_PLUS  = 10;
const int LO_MINUS = 11;

int minVal = 1023;
int maxVal = 0;
unsigned long lastReset = 0;

void setup() {
  Serial.begin(115200);
  pinMode(LO_PLUS,  INPUT);
  pinMode(LO_MINUS, INPUT);
  Serial.println("RAW | LO+ | LO- | MIN | MAX");
  Serial.println("----+-----+-----+-----+----");
}

void loop() {
  int val = analogRead(ECG_PIN);
  int lop = digitalRead(LO_PLUS);
  int lom = digitalRead(LO_MINUS);

  if (val < minVal) minVal = val;
  if (val > maxVal) maxVal = val;

  // Reset min/max every 5 seconds
  if (millis() - lastReset > 5000) {
    minVal    = 1023;
    maxVal    = 0;
    lastReset = millis();
    Serial.println("--- MIN/MAX RESET ---");
  }

  Serial.print(val);   Serial.print(",");
  Serial.print(lop);   Serial.print(",");
  Serial.print(lom);   Serial.print(",");
  Serial.print(minVal);Serial.print(",");
  Serial.println(maxVal);

  delay(10);
}
