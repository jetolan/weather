import picamera
import datetime
import time
import os


#check for output directory
dir='/home/pi/weather/img'
if not os.path.exists(dir):
    os.mkdir(dir)

#get time
now=datetime.datetime.now().isoformat()[-0:-7]    

#take picture
with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    time.sleep(1) # Camera warm-up time
    filename = dir+'/image_'+now+'.jpg'
    camera.capture(filename)
