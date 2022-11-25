Collects data from sensors and writes to csv file

#SETUP
##################
enable ssh, i2c, camera
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y python3-pip python3-smbus i2c-tools matchbox-keyboard emacs
sudo pip3 install --upgrade setuptools
```

```
sudo git clone -b wellmeter https://github.com/jetolan/weather
cd weather
sudo python3 setup.py install
```

enable i2c
```
sudo raspi-config nonint do_i2c 0
sudo i2cdetect -y 1
```

################

### crontab:

must be root:

sudo crontab -e

```
@reboot python3 /home/pi/weather/reed_switch.py
*/1  * * * * python3 /home/pi/weather/heartbeat.py
@reboot python3 /home/pi/weather/relay.py
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


### clock

sudo i2cdetect -y 1
sudo emacs /boot/config.txt
add : dtoverlay=i2c-rtc,pcf8523
reboot
sudo i2cdetect -y 1
 
 
sudo apt-get -y remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove 
sudo systemctl disable fake-hwclock

sudo emacs /lib/udev/hwclock-set
comment out:
#if [ -e /run/systemd/system ] ; then 
#exit 0
#fi

#/sbin/hwclock --rtc=$dev --systz --badyear
#/sbin/hwclock --rtc=$dev --systz

sudo hwclock -w
sudo hwclock -r
