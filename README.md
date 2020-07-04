Collects data from sensors and writes to csv file

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

### crontab:

```
@reboot python /home/pi/weather/reed_switch.py
*/10  * * * * python /home/pi/weather/get_data.py
*/11 * * * * /bin/sh /home/pi/weather/transfer.sh
0   19 * * * python /home/pi/weather/takepicture.py
```
### ssh
on local network (yachthouse) TP-LINK Archer C7:
ssh -X pi@192.168.1.52
