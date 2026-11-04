#!/usr/bin/env python3
"""
Ran Yang 10/27/2024
Connection:
VDD -> 3.3V
VREF -> 3.3V
AGND -> GND
CLK -> GPIO11
Dout -> GPIO09
Din -> GPIO10
CS -> GPIO8
DGND -> GND

Analog input -> CH0 ~ CH7
"""
import spidev
import time
from time import sleep
import RPi.GPIO as GPIO

spi = spidev.SpiDev()  # Open spi bus
spi.open(0, 0)  # Open(bus, device)
spi.max_speed_hz = 1000000
spi.mode = 0b00  # SPI modes; 00, 01, 10, 11
pump_pin = 17


def read_adc(channel):
    if not 0 <= channel <= 7:
        raise IndexError('Invalid channel. Enter a value between 0 and 7.')
    """Data sheet page 19 explains setting the sgl/diff bit to high, hence we add 8 = 0b1000
    left shift 4 bits to make space for the second byte of data[1]."""
    request = [0x1, (8 + channel) << 4,
               0x0]  # [Start bit, configuration, listen space]
    # Data is recorded in 3 bytes: data[0] - discard, data[1] - keep last 2 bits, data[2] - keep all.
    data = spi.xfer2(request)
    # Shift bits to get the 10-bit data.
    data10bit = ((data[1] & 3) << 8) + data[2]
    return data10bit
while True:
    raw_count0 = read_adc(0)
    raw_count1 = read_adc(1)
    v_volt0 = raw_count0 * 3.3/1023
    v_volt1 = raw_count1 * 3.3/1023
    print(f"Voltage Channel 0: {v_volt0:.2f}V")
    print(f"Voltage Channel 1: {v_volt1:.2f}V")
    print(f"Raw Count Channel 0: {raw_count0: .3f}")
    print(f"Raw Count Channel 1: {raw_count1: .3f}")
    runtime = (raw_count0 / 1023) * 1023
    print(f"Pump Runtime: {runtime:.2f}s")
    if runtime > 0.05:
        print("Pump On")
        GPIO.output(pump_pin, GPIO.HIGH)
        sleep(runtime)
        GPIO.output(pump_pin,GPIO.LOW)
        print("Pump OFF")
    sleep(0.5)




