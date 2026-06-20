# 🫀 Portable ECG Device
### Arduino Nano + AD8232 | Real-Time Heart Signal Acquisition

![GitHub repo size](https://img.shields.io/github/repo-size/AvanindraRathore/portable-ecg-device)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Arduino%20Nano-blue)
![Language](https://img.shields.io/badge/language-C%2B%2B%20%7C%20Python-orange)

A fully functional portable ECG (Electrocardiogram) device built from scratch using an Arduino Nano and AD8232 ECG front-end module. Captures real-time heart electrical signals via 3-lead electrode placement and displays a live waveform on a laptop screen over USB.

> Built as part of my Biomedical Engineering + Machine Intelligence studies at SRMIST.

---

## ⚙️ Hardware Used

| Component | Purpose |
|---|---|
| Arduino Nano (ATmega328P) | Microcontroller — ADC + USB serial |
| AD8232 ECG Module | Signal amplification + filtering (~1000x gain) |
| Disposable Ag/AgCl Electrode Pads | Skin-contact signal acquisition |
| ECG Lead Wires (3.5mm snap type) | RA / LA / RL connections |
| 220Ω Resistors × 2 | LED current limiting |
| Green + Red LEDs | Leads-on / leads-off indicators |
| Mini Breadboard | Prototype assembly |
| Jumper Wires (M-M) | Connections |
| USB-A to Mini-USB Cable | Power + data to laptop |

---

## 🔌 Wiring

| AD8232 Pin | Arduino Nano Pin |
|---|---|
| 3.3V | 3.3V |
| GND | GND |
| OUTPUT | A0 |
| LO+ | D10 |
| LO− | D11 |

| Component | Connection |
|---|---|
| Green LED anode | 220Ω → D7 |
| Green LED cathode | GND |
| Red LED anode | 220Ω → D8 |
| Red LED cathode | GND |

> ⚠️ **Critical:** AD8232 must connect to 3.3V only. Never connect to 5V — it will permanently damage the module.

---

## 📁 Repository Structure

```
portable-ecg-device/
│
├── arduino/
│   ├── ecg_main/
│   │   └── ecg_main.ino          # Main ECG sketch (250Hz sampling, leads-off detection)
│   └── ecg_diagnostic/
│       └── ecg_diagnostic.ino    # Diagnostic sketch for troubleshooting
│
├── python/
│   └── ecg_monitor.py            # Python live display app (matplotlib + notch filter)
│
├── docs/
│   └── wiring_diagram.md         # Full wiring reference
│
├── images/
│   └──Project Related Photos (PNG)
│
├── README.md
└── LICENSE
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/AvanindraRathore/portable-ecg-device.git
cd portable-ecg-device
```

### 2. Upload Arduino sketch
- Open `arduino/ecg_main/ecg_main.ino` in Arduino IDE 2.0
- Select board: **Arduino Nano**
- Select processor: **ATmega328P** (try Old Bootloader if upload fails)
- Select the correct COM port
- Click Upload

### 3. View live waveform (Serial Plotter)
- After uploading, open **Tools → Serial Plotter**
- Set baud rate to **115200**
- Attach electrodes to body
- Observe waveform



---

## 🧠 How It Works

The heart generates electrical impulses during each beat — typically **0.5–5 mV** across the skin surface. These signals are:

1. **Picked up** by 3 Ag/AgCl gel electrode pads placed on the body
2. **Amplified ~1000×** by the AD8232's instrumentation amplifier
3. **Filtered** — high-pass filter removes baseline wander, low-pass removes high-frequency noise
4. **Digitized** by Arduino Nano's 10-bit ADC at 250 samples/second
5. **Transmitted** over USB serial to laptop
6. **Displayed** as a live scrolling waveform

The characteristic **QRS complex** (the sharp spike in each heartbeat cycle) corresponds to ventricular depolarization — the electrical event that triggers the heart's main pumping action.

---

## 📍 Electrode Placement (Lead I Configuration)

| Electrode | Lead Color | Body Position |
|---|---|---|
| RA (Right Arm) | White | Right collarbone |
| LA (Left Arm) | Black | Left collarbone |
| RL (Right Leg / Reference) | Red | Lower left ribcage |

> RL is the driven-right-leg reference electrode. **Never skip it** — without RL, the AD8232 cannot reject common-mode noise and the output will be overwhelmed by 50Hz mains interference.

---

## ⚡ Signal Challenges & Solutions

| Challenge | Cause | Solution |
|---|---|---|
| 50Hz mains hum | Powerline interference | Software notch filter (scipy) |
| Baseline wander | Breathing / movement | AD8232's built-in high-pass filter |
| Motion artifact | Body movement | Sit still, rest arm flat on surface |
| Saturated output | Loose RL electrode | Check RL snap connection and pad adhesion |
| Leads-off noise | Floating LO+/LO− pins | Code outputs 0 when leads-off detected |

---

## 🔮 Roadmap

- [x] Breadboard prototype
- [x] Real-time USB serial waveform
- [x] Leads-off detection
- [x] Python live display with notch filter
- [ ] Move to permanent PCB (perfboard)
- [ ] Add enclosure (project box)
- [ ] BPM (heart rate) calculation
- [ ] Machine learning layer — real-time arrhythmia detection
- [ ] Wireless transmission (future version)

---

## 🛠️ Built With

- [Arduino IDE 2.0](https://www.arduino.cc/en/software)
- [Python 3](https://www.python.org/)
- [pyserial](https://pyserial.readthedocs.io/)
- [matplotlib](https://matplotlib.org/)
- [scipy](https://scipy.org/)
- [numpy](https://numpy.org/)

---

## 👤 Author

**Avanindra Singh Rathore**
B.Tech Biomedical Engineering (Machine Intelligence Specialization)
SRMIST, Chennai

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/avanindra-singh-rathore)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/AvanindraRathore)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

*"Building things that interact with the human body makes the biomedical side of engineering feel very real, very fast."*
