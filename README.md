# Real-Time Satellite Telemetry Tracking Link

A distributed embedded system that pulls live orbital Two-Line Element (TLE) datasets, calculates multi-body vector tracking frames, and streams real-time satellite positions to a physical Raspberry Pi Pico flight controller dashboard.

## System Architecture
[Internet API] ➔ [Host Computer (Python / Skyfield)] ➔ (USB Serial) ➔ [Raspberry Pi Pico (MicroPython)] ➔ (I2C) ➔ [1602 LCD Display]

## Key Technical Implementations
- **Distributed System Pipeline:** Offloaded heavy mathematical aerospace coordinate processing to a Python host client, establishing a serial USB link layer to interact smoothly with resource-constrained microcontroller hardware.
- **Telemetry Data Caching:** Implemented local file-system caching for satellite parameter data, optimizing system tracking logic to process 0.5-second snappier runtime display loops while cutting external network traffic down to absolute zero.
- **Embedded Driver Integration:** Wrote a low-overhead stream parser on the Pico to decode packet data strings on-the-fly and map metrics over an I2C communication bus to a 16x2 character grid interface.
