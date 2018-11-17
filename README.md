Collects data from sensors and writes to csv file

### set static ip:

add:
```
interface eth0
static ip_address=192.168.0.52/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1

interface wlan0
static ip_address=192.168.0.52/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
```
to /etc/dhcpcd.conf

### crontab:
