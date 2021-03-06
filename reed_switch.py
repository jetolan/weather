#!/usr/bin/python

# based on:
# https://www.raspberrypi.org/learning/weather-station-guide/rain-gauge.md

import RPi.GPIO as GPIO
import datetime
import os
import csv
import time
import sys

pin = 24


def bucket_tipped(channel):
    """
    Each time GPIO is detected, write new line to csv
    """
    now = datetime.datetime.now().isoformat()
    print("rain gauge tip at : " + str(now))

    # write to file
    file = '/home/pi/weather/well_data.csv'
    columns = ['', 'isotime', 'rain_tip']
    if not os.path.exists(file):
        with open(file, 'w') as fp:
            writer = csv.DictWriter(fp, fieldnames=columns, delimiter=',')
            writer.writeheader()

    with open(file, mode='a+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns, delimiter=',')
        writer.writerow({'': 0,
                         'isotime': now,
                         'rain_tip': 1,
                         })


def main_loop():
    """
    Continuous loop for constant monitoring
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, GPIO.PUD_DOWN)
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
