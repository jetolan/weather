import pandas as pd
import datetime
import os

import board
import busio
import adafruit_bme280
import adafruit_ina219

#get timestamp
#will need clock for non network connected device
now=datetime.datetime.now().isoformat()

# get data from BME280
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
degrees = bme280.temperature
humidity = bme280.humidity
hectopascals = bme280.pressure


#get data from ina219
i2c = busio.I2C(board.SCL, board.SDA)
ina219 = adafruit_ina219.INA219(i2c)
BV=ina219.bus_voltage
SV=ina219.shunt_voltage / 1000
I=ina219.current
power=BV*I

#write to dataframe
df = pd.DataFrame({'isotime' : pd.Series(now), 'temp' : pd.Series(degrees),'temp_mcp9808' : pd.Series(temp), 'pressure' : pd.Series(pascals), 'humidity' : pd.Series(humidity)}, columns=['isotime', 'temp', 'temp_mcp9808','pressure', 'humidity'])


#write to file
file='/home/pi/weather/weather_data.csv'
if not os.path.exists(file):
     df.to_csv(file, header=True)
else:
     with open(file, 'a') as f:
          df.to_csv(f, header=False)
