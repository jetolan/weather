from Adafruit_Python_BME280 import Adafruit_BME280
from Adafruit_MCP9808 import MCP9808
import pandas as pd
import datetime
import os

#get timestamp
#will need clock for non network connected device
now=datetime.datetime.now().isoformat()


#get data from BME280
sensor = Adafruit_BME280.BME280(mode=Adafruit_BME280.BME280_OSAMPLE_8)
degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
humidity = sensor.read_humidity()
#timestamp = sensor.t_fine #not sure what this is...doesn't seem to be time

#get data from MCP9808
#sensor = MCP9808.MCP9808()
# Initialize communication with the sensor.
#sensor.begin()
#temp = sensor.readTempC()


#write to dataframe
#df = pd.DataFrame({'isotime' : pd.Series(now), 'temp' : pd.Series(degrees),'temp_mcp9808' : pd.Series(temp), 'pressure' : pd.Series(pascals), 'humidity' : pd.Series(humidity)}, columns=['isotime', 'temp', 'temp_mcp9808','pressure', 'humidity'])

df = pd.DataFrame({'isotime' : pd.Series(now), 'temp' : pd.Series(degrees), 'pressure' : pd.Series(pascals), 'humidity' : pd.Series(humidity)}, columns=['isotime', 'temp','pressure', 'humidity'])

#write to file
file='/home/pi/weather/weather_data.csv'
if not os.path.exists(file):
     df.to_csv(file, header=True)
else:
     with open(file, 'a') as f:
          df.to_csv(f, header=False)
