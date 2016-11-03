import picamera
import datetime
import time
import os


#check for output directory
dir='/home/pi/weather/pictures'
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

#alternatively:
#raspistill -w 1280 -h 720 -n -t 100 -q 10 -e jpg -th none -o /home/pi/weather/pictures/image.jpg
    
