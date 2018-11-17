Collects data from sensors and writes to csv file

### set static ip:

add:
```
interface eth0
static ip_address=192.168.8.52/24
static routers=192.168.8.1
static domain_name_servers=192.168.8.1

interface wlan0
static ip_address=192.168.8.52/24
static routers=192.168.8.1
static domain_name_servers=192.168.8.1
```
to /etc/dhcpcd.conf

### crontab:

```
@reboot python /home/pi/weather/reed_switch.py
*/10  * * * * python /home/pi/weather/get_data.py
*/11 * * * * /bin/sh /home/pi/weather/transfer.sh
0   19 * * * python /home/pi/weather/takepicture.py
```
