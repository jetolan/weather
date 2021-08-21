import RPi.GPIO as GPIO
import datetime
import time

'''
Use the 3.3.V pin, gnd pin and GPIO 24 to connect to the relay
Connect COM and N0 in parallel with the well swtich
Jumper in the L position

Grundfos Low-Level Float Switch is Normally Open in the down position
So we have the relay normally open and in parallel

Used this relay:
https://www.amazon.com/gp/product/B00LW15A4W/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1
'''


def switch_relay(state):
    # get time (not used yet)
    now = datetime.datetime.now().isoformat()[-0:-7]

    GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers

    RELAIS_1_GPIO = 23
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)  # GPIO Assign mode

    # whether we pull up or down depends on the jumpers on the relay
    if state == 'down':
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW)  # pull down
    if state == 'up':
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)  # pull up


if __name__ == '__main__':
    while 1:
        # get time (not used yet)
        now = datetime.datetime.now().isoformat()[-0:-7]
        # just go based on timer rather than date
        time.sleep(1)
        # 15min open -> pumping
        switch_relay('down')
        time.sleep(60*15)
        # then 45min closed -> not pumping
        switch_relay('up')
        time.sleep(60*45)
