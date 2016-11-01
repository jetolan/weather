
#based on:
#https://www.raspberrypi.org/learning/weather-station-guide/rain-gauge.md




#!/usr/bin/python

import RPi.GPIO as GPIO
import datetime
import pandas as pd
import os

pin = 6

def bucket_tipped(channel):

    now=datetime.datetime.now().isoformat()
    print "rain gauge tip at : "+str(now)

    df=pd.DataFrame({'isotime' : pd.Series(now), 'rain_tip':pd.Series('1')})

    #write to file
    
    file='/home/pi/weather/rain_data.csv'
    if not os.path.exists(file):
             df.to_csv(file, header=True)
    else:
        with open(file, 'a') as f:
                      df.to_csv(f, header=False)


GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(pin, GPIO.FALLING, callback=bucket_tipped, bouncetime=300)

#GPIO.remove_event_detect(channel)  
