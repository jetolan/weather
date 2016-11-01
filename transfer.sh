#/bin/bash

#turn on wifi:
sudo ifconfig wlan0 up
sleep 30

#scp -i /home/pi/weather/Insight2016B.pem /home/pi/weather/weather_data.csv ubuntu@54.153.39.29:weather/web/.

#rsync uses less bandwidth than scp:
rsync -rave "ssh -i /home/pi/weather/Insight2016B.pem" /home/pi/weather/weather_data.csv ubuntu@54.153.39.29:weather/web/.

rsync -rave "ssh -i /home/pi/weather/Insight2016B.pem" /home/pi/weather/rain_data.csv ubuntu@54.153.39.29:weather/web/.

#turn wifi back off to save power
sudo ifconfig wlan0 down

