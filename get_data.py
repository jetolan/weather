import csv
import datetime
import os

import board
import busio
import adafruit_bme280
import adafruit_ina219

# get timestamp
# will need clock for non network connected device
now = datetime.datetime.now().isoformat()


# get data from BME280
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
    degrees = bme280.temperature
    humidity = bme280.humidity
    hectopascals = bme280.pressure
except:
    degrees = ''
    humidity = ''
    hectopascals = ''

# get data from ina219
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    ina219 = adafruit_ina219.INA219(i2c)
    BV = ina219.bus_voltage
    SV = ina219.shunt_voltage / 1000
    I = ina219.current
    power = BV*I
except:
    power = ''


# write to csv
file = '/home/pi/weather/weather_data.csv'
columns = ['isotime', 'temp', 'pressure', 'humidity', 'power']
if not os.path.exists(file):
    with open(file, 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=columns, delimiter=',')
        writer.writeheader()

with open(file, mode='a+') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=columns, delimiter=',')
    writer.writerow({'isotime': now,
                     'temp': degrees,
                     'pressure': (hectopascals*100),
                     'humidity': humidity,
                     'power': power,
                     })
