#TLE Satellite Pass Predicter & Visualizer (Standard Python)
#In this script, the computer will handle the heavy internet requests and tracking algorithms and then deliver a simple status update to the Pico via USB

from datetime import datetime, timedelta, timezone
import time
import requests
import serial
import os
from skyfield.api import Topos, load, wgs84
from skyfield.sgp4lib import EarthSatellite

#Configuring USB Port
pico_port = "COM3"
baud_rate = 115200
try:
    pico = serial.Serial(pico_port, baud_rate, timeout=1)
    print(f"Connected to Pico on {pico_port}")
except Exception as e:
    print(f"Could not connect to Pico. Please Check your port settings.\nError: {e}")
    exit()

#Target coordinates and satellite setup (Using my current location in Boston, MA)
myLatitude = 42.3398247
myLongitude = -71.0880961

ts = load.timescale()

#Fetching ISS TLE data
#Temporarily commented out to avoid hitting the firewall
#tleURL = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE"
#response = requests.get(tleURL)
#with open('iss_tle.txt', 'w') as f:
    #f.write(response.text)

#Loading the local file directly
satellites = load.tle_file('iss_tle.txt')
satellite = satellites[0]

#Loading the planet database
myLocation = wgs84.latlon(myLatitude, myLongitude)
print("Ground Station is working. Streaming live tracking to Pico...")

#Live streaming loop
try:
    while True:
        #Getting the exact current time
        now = datetime.now(timezone.utc)
        t = ts.utc(now.year, now.month, now.day, now.hour, now.minute, now.second)
        
        #Calculating current satellite position relative to my location
        difference = satellite - myLocation
        
        #"alt-az" is short for altitude (up-down) and azimuth (left-right)
        alt, az, distance = difference.at(t).altaz()
        
        #Checking if the satellite is above the horizon
        if alt.degrees > -90:
            command = f"PASS,{alt.degrees:.2f}\n"
            print(f"ISS is currently overhead. Elevation: {alt.degrees:.2f} degrees")
        else:
            command = "NO_PASS,0\n"
            print("ISS is below the horizon.")
        
        #Sending the string down the USB cable to the Pico
        pico.write(command.encode("utf-8"))
        pico.flush()
        
        time.sleep(2) #Update every 2 seconds
        
except KeyboardInterrupt:
    pico.close()
    print("\nGround Station stopped.")