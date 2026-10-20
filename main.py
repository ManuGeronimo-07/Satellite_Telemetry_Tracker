#Manus Two-Line Element (TLE) Satellite Pass Predictor & Visualizer (MicroPython Script)
#Creating a Python script to fetch the TLE data from the internet and calculate the satellite passes
#Computer will sent a simple signal over the USB cable to the Raspberry Pi Pico

import sys
import time
import machine
import select
import pico_i2c_lcd
from pico_i2c_lcd import I2cLcd
from time import sleep
from machine import I2C, Pin

#The Pico will wait for data blink it's built-in LED when it receives data from the USB cable to show it's tracking the satellite
#Setting up the built-in LED; for a standard Pico, it is GP25
led = Pin(25, Pin.OUT)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) #Data pin (sda) is pin 0, clock pin (scl) is pin 1
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16) #2 rows, 16 columns on LCD

lcd.clear()
lcd.move_to(0,0)
lcd.putstr("MISSION CONTROL")
lcd.move_to(0,1)
lcd.putstr("AWAITING DATA...")
        
print("Flight software active with LCD.")

while True:
    lcd.show_cursor()
    lcd.blink_cursor_on()
    #Checking if data is coming from the laptop over the USB cable
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
    #"stdin" is the standard input stream. "select.select(rlist,wlist, xlist, timeout)" is the set that we want our stdin to be in
        #If true, read the line of data sent by the laptop
        line = sys.stdin.readline().strip()
        if not line:
            continue
        #Split the data into pieces (example incoming string: "PASS,45.2")
        data = line.split(",")
        
        if len(data) >= 2:
            status = str(data[0])
            val = str(data[1])
        
            if "NO_PASS" in status:
                led.value(0)
                lcd.clear()
                lcd.move_to(0,0)
                lcd.putstr("TARGET: ISS")
                lcd.move_to(0,1)
                lcd.putstr("BELOW HORIZON")
            
            elif "PASS" in status:
                led.value(1)
                lcd.clear()
                lcd.move_to(0,0)
                lcd.putstr("TRACKING ISS")
                lcd.move_to(0,1)
                lcd.putstr(f"ELEV: {val} deg")
            
    time.sleep(0.2) #Data is checked every 0.5 seconds      