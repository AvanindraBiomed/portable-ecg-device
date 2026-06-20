/*
  ============================================================
  PORTABLE ECG DEVICE — Main Sketch
  ============================================================
  Hardware:  Arduino Nano + AD8232 ECG Module
  Author:    Avanindra Singh Rathore
  Platform:  Arduino Nano (ATmega328P)
  Baud Rate: 115200

  WIRING:
    AD8232 3.3V   → Nano 3.3V
    AD8232 GND    → Nano GND
    AD8232 OUTPUT → Nano A0
    AD8232 LO+    → Nano D10
    AD8232 LO-    → Nano D11
    Green LED     → 220Ω → Nano D7
    Red LED       → 220Ω → Nano D8

  HOW TO VIEW:
    Arduino IDE → Tools → Serial Plotter → 115200 baud
  ============================================================
*/

// ── Pin Definitions ─────────────────────────────────────────
const int ECG_PIN   = A0;   // AD8232 analog output
const int LO_PLUS   = 10;   // Leads-off detection +
const int LO_MINUS  = 11;   // Leads-off detection -
const int LED_GREEN = 7;    // Electrodes connected indicator
const int LED_RED   = 8;    // Leads-off warning indicator

// ── Sampling ─────────────────────────────────────────────────
const int SAMPLE_RATE = 250;                          // Hz
const unsigned long SAMPLE_INTERVAL = 1000000 / SAMPLE_RATE; // microseconds
unsigned long lastSampleTime = 0;

// ── Moving Average Filter ────────────────────────────────────
const int FILTER_SIZE = 5;
int filterBuffer[FILTER_SIZE];
int filterIndex = 0;
long filterSum   = 0;

// ─────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);

  pinMode(LO_PLUS,   INPUT);
  pinMode(LO_MINUS,  INPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED,   OUTPUT);

  // Initialize filter buffer
  for (int i = 0; i < FILTER_SIZE; i++) filterBuffer[i] = 0;

  Serial.println("ECG_READY");
  digitalWrite(LED_GREEN, HIGH);
}

// ─────────────────────────────────────────────────────────────
void loop() {
  unsigned long now = micros();

  if (now - lastSampleTime >= SAMPLE_INTERVAL) {
    lastSampleTime = now;

    // Check leads-off detection
    if ((digitalRead(LO_PLUS) == 1) || (digitalRead(LO_MINUS) == 1)) {
      // Leads off — send 0 so plotter shows flat line instead of garbage
      Serial.println(0);
      digitalWrite(LED_GREEN, LOW);
      digitalWrite(LED_RED,   HIGH);

    } else {
      // Read and filter ECG signal
      int raw = analogRead(ECG_PIN);

      // 5-point moving average filter
      filterSum -= filterBuffer[filterIndex];
      filterBuffer[filterIndex] = raw;
      filterSum += raw;
      filterIndex = (filterIndex + 1) % FILTER_SIZE;
      int filtered = filterSum / FILTER_SIZE;

      Serial.println(filtered);
      digitalWrite(LED_GREEN, HIGH);
      digitalWrite(LED_RED,   LOW);
    }
  }
}
