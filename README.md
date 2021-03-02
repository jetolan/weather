Collects data from sensors and writes to csv file

#SETUP
##################
enable ssh, i2c, camera
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y python3-pip python-smbus i2c-tools
sudo pip3 install --upgrade setuptools
```

```
git clone https://github.com/jetolan/weather
cd weather
sudo python3 setup.py install
```

```
sudo i2cdetect -y 1
```

################

### crontab:

must be root:

sudo crontab -e

```
@reboot python3 /home/pi/weather/reed_switch.py
*/10  * * * * python3 /home/pi/weather/get_data.py
0   12 * * * python3 /home/pi/weather/takepicture.py
```

################

### Read directly off sd card:

https://www.jeffgeerling.com/blog/2017/mount-raspberry-pi-sd-card-on-mac-read-only-osxfuse-and-ext4fuse

###############

### ~~set static ip:~~
THIS is probably a bad idea!! Don't do it (2020-07-02) messes up time and apt-get

https://www.raspberrypi.org/learning/networking-lessons/rpi-static-ip-address/
add:


```
interface eth0
static ip_address=192.168.1.52/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1

interface wlan0
static ip_address=192.168.1.52/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1

```
to /etc/dhcpcd.conf


### ssh
on local network (yachthouse) TP-LINK Archer C7:
ssh -X pi@192.168.1.52

find ip address with 
arp -a

### wifi drivers
https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=62371



### piscope
https://www.raspberrypi.org/forums/viewtopic.php?t=155990
http://abyz.me.uk/rpi/pigpio/piscope.html
commands:
$ sudo pigpiod
$ piscope
