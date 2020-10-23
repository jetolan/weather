import picamera
import time
from fractions import Fraction
import datetime
import os

'''
#view video stream
with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(60)
    camera.stop_preview()
'''



#check for output directory
dir='/home/pi/Pictures'
if not os.path.exists(dir):
    os.mkdir(dir)
    
#get time
now=datetime.datetime.now().isoformat()[-0:-7] 

with picamera.PiCamera() as camera:
    #must increase GPU Memory setting to 256 on pi zero
    camera.resolution=(4056,3040)

    camera.framerate=Fraction(1,6)
    camera.sensor_mode=3
    camera.iso=800

    #manual shutter speed max 3 seconds
    camera.shutter_speed=int(3*1e6)

    #for an auto shutter
    #time.sleep(2)
    #camera.shutter_speed=camera.exposure_speed

    #write
    time.sleep(5) # Camera warm-up time
    filename = f'{dir}/image_{now}.png'
    camera.capture(filename)
