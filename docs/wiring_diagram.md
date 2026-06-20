# Wiring Diagram — Portable ECG Device

## AD8232 → Arduino Nano

| AD8232 Pin | Arduino Nano Pin | Wire Color (suggested) |
|---|---|---|
| 3.3V | 3.3V | Red |
| GND | GND | Black |
| OUTPUT | A0 | Green |
| LO+ | D10 | Yellow |
| LO− | D11 | Yellow |

> ⚠️ **CRITICAL:** AD8232 operates on 3.3V only. Connecting to 5V will permanently damage the module.

---

## LEDs → Arduino Nano

| Component | Connection |
|---|---|
| Green LED (long leg / anode) | 220Ω resistor → D7 |
| Green LED (short leg / cathode) | GND |
| Red LED (long leg / anode) | 220Ω resistor → D8 |
| Red LED (short leg / cathode) | GND |

---

## Electrode Leads → AD8232

| Electrode | Lead Color | AD8232 Port | Body Placement |
|---|---|---|---|
| RA (Right Arm) | White | RA jack | Right collarbone |
| LA (Left Arm) | Black | LA jack | Left collarbone |
| RL (Reference) | Red | RL jack | Lower left ribcage |

---

## Power

- Arduino Nano powered via **USB cable to laptop** (no separate battery needed for prototype)
- Laptop should ideally run on **battery power** during recording to minimize 50Hz mains noise

---

## Breadboard Layout

```
LEFT POWER RAIL          TERMINAL STRIP (left half)     CENTER GAP     TERMINAL STRIP (right half)     RIGHT POWER RAIL
──────────────           ──────────────────────────     ──────────     ──────────────────────────       ────────────────
  +  |  −               [ Arduino Nano sits here  ]                   [ AD8232 sits here        ]
                         [ spanning center gap     ]                   [ Electrode jack faces up ]
                                                                       [ LEDs below AD8232       ]
```

- Nano's 3V3 pin → Left rail outer column (+ bus)
- Nano's GND pin → Left rail inner column (− bus)
- AD8232 3.3V → + bus
- AD8232 GND → − bus
- All LED cathodes → − bus

---

## Signal Flow

```
Skin → Electrode Pads → Lead Wires → AD8232 (amplify + filter) → Arduino A0 (digitize) → USB → Laptop (display)
```
