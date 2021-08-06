import RPi.GPIO as GPIO
import datetime
import time


def switch_relay():
    # get time (not used yet)
    now = datetime.datetime.now().isoformat()[-0:-7]

    GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers

    RELAIS_1_GPIO = 24
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)  # GPIO Assign mode
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW)  # out
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)  # on
    time.sleep(10)


if __name__ == '__main__':
    while 1:
        time.sleep(10)
        switch relay()
