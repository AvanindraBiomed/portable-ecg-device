"""
============================================================
PORTABLE ECG DEVICE — Python Live Display
============================================================
Author:  Avanindra Singh Rathore
Requires: pyserial, matplotlib, numpy, scipy

Install dependencies:
    pip install pyserial matplotlib numpy scipy

Usage:
    python ecg_monitor.py

Make sure Arduino is running ecg_main.ino before starting.
The script auto-detects the Arduino's COM port.
============================================================
"""

import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks


# ── Configuration ──────────────────────────────────────────────
BAUD_RATE   = 115200
BUFFER_SIZE = 500      # samples shown on screen (~2s at 250Hz)
SAMPLE_RATE = 250      # Hz


# ── Auto-detect Arduino port ───────────────────────────────────
def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        desc = p.description.lower()
        if any(x in desc for x in ['arduino', 'ch340', 'usb serial', 'uart']):
            return p.device
    return None

PORT = find_arduino_port()
if PORT is None:
    PORT = input(
        "Arduino not detected automatically.\n"
        "Enter port manually (e.g. COM5 or /dev/ttyUSB0): "
    )

print(f"Connecting to Arduino on {PORT} ...")
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
print("Connected!\n")


# ── Buffers ────────────────────────────────────────────────────
ecg_buf   = deque([512] * BUFFER_SIZE, maxlen=BUFFER_SIZE)
leads_off = False
bpm_value = 0


# ── 50 Hz notch filter (removes Indian mains hum) ─────────────
def notch_filter(data, freq=50.0, fs=SAMPLE_RATE, Q=30.0):
    w0  = freq / (fs / 2.0)
    b, a = butter(2, [w0 * 0.9, w0 * 1.1], btype='bandstop')
    return filtfilt(b, a, np.array(data, dtype=float))


# ── BPM estimation from R-peaks ───────────────────────────────
def calc_bpm(data):
    arr = np.array(data, dtype=float)
    arr -= arr.mean()
    threshold = arr.std() * 0.7
    peaks, _ = find_peaks(arr, height=threshold, distance=int(SAMPLE_RATE * 0.4))
    if len(peaks) >= 2:
        rr_avg = np.mean(np.diff(peaks)) / SAMPLE_RATE
        bpm    = 60.0 / rr_avg
        return int(bpm) if 40 < bpm < 200 else 0
    return 0


# ── Plot setup ─────────────────────────────────────────────────
fig = plt.figure(figsize=(13, 6), facecolor='#0a0a0a')
fig.suptitle('🫀  Portable ECG Monitor  |  USB Wired  |  AD8232 + Arduino Nano',
             color='#00ff99', fontsize=13, fontweight='bold', y=0.97)

ax = fig.add_axes([0.07, 0.14, 0.88, 0.72])
ax.set_facecolor('#0d0d0d')
ax.set_xlim(0, BUFFER_SIZE)
ax.set_ylim(100, 900)
ax.set_xlabel('Samples  (250 per second  =  ~2 second window)', color='#666')
ax.set_ylabel('ADC Value  (0 – 1023)', color='#666')
ax.tick_params(colors='#555')
ax.grid(True, color='#181818', linewidth=0.6)
for spine in ax.spines.values():
    spine.set_edgecolor('#222')

ecg_line,   = ax.plot([], [], color='#00ff99', linewidth=1.2, antialiased=True)
status_txt   = ax.text(0.01, 0.96, '', transform=ax.transAxes,
                       color='#00ff99', fontsize=11, va='top', fontweight='bold')
bpm_txt      = ax.text(0.76, 0.96, '', transform=ax.transAxes,
                       color='#ff5555', fontsize=13, va='top', fontweight='bold')


# ── Animation update ───────────────────────────────────────────
frame_counter = 0

def update(_frame):
    global leads_off, bpm_value, frame_counter
    frame_counter += 1

    while ser.in_waiting > 0:
        try:
            raw = ser.readline().decode('utf-8', errors='ignore').strip()
            if raw == '!':
                leads_off = True
            elif raw.lstrip('-').isdigit():
                leads_off = False
                ecg_buf.append(int(raw))
        except Exception:
            pass

    y = list(ecg_buf)
    x = list(range(len(y)))

    if len(y) == BUFFER_SIZE:
        try:
            y_filt = notch_filter(y)
            ecg_line.set_data(x, y_filt)
            if frame_counter % 25 == 0:
                bpm_value = calc_bpm(y_filt)
        except Exception:
            ecg_line.set_data(x, y)
    else:
        ecg_line.set_data(x, y)

    if leads_off:
        status_txt.set_text('⚠  LEADS OFF  —  reattach electrodes')
        status_txt.set_color('#ff4444')
        bpm_txt.set_text('')
    else:
        status_txt.set_text('●  LIVE')
        status_txt.set_color('#00ff99')
        bpm_txt.set_text(f'❤  {bpm_value} BPM' if bpm_value else '❤  —')

    return ecg_line, status_txt, bpm_txt


ani = animation.FuncAnimation(
    fig, update, interval=20, blit=True, cache_frame_data=False
)

plt.show()
ser.close()
