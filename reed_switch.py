#!/usr/bin/python

# based on:
# https://www.raspberrypi.org/learning/weather-station-guide/rain-gauge.md

import RPi.GPIO as GPIO
import datetime
import pandas as pd
import os
import time
import sys

pin = 4


def bucket_tipped(channel):
    """
    Each time GPIO is detected, write new line to csv
    """
    now = datetime.datetime.now().isoformat()
    print("rain gauge tip at : " + str(now))

    df = pd.DataFrame({'isotime': pd.Series(now), 'rain_tip': pd.Series('1')})

    # write to file
    file = '/home/pi/weather/rain_data.csv'
    if not os.path.exists(file):
        df.to_csv(file, header=True)
    else:
        with open(file, 'a') as f:
            df.to_csv(f, header=False)


def main_loop():
    """
    Continuous loop for constant monitoring
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(
        pin, GPIO.FALLING, callback=bucket_tipped, bouncetime=300)

    while 1:
        # do your stuff...
        time.sleep(0.1)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print(f'{sys.stderr}, \nExiting by user request.\n')
        sys.exit(0)
