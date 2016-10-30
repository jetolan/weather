import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import datetime
from pytz import utc, timezone

#read csv file with data
data=pd.read_csv('weather_data.csv', sep=',', header=0, engine='python')

#time data
time=np.array(data['isotime']) # in UTC isotime
dt=[datetime.datetime.strptime(X, "%Y-%m-%dT%H:%M:%S.%f" ) for X in time]

def to_pacific(dt):
 utc_dt = utc.localize(dt)
 pacific = timezone('US/Pacific')
 loc_dt = utc_dt.astimezone(pacific)  
 return loc_dt

loc_dt=[to_pacific(X) for X in dt]

#weather data
temp=np.array(data['temp']) # in degrees C
pressure=data['pressure'] / 1000. #convert to kPa 
humidity=data['humidity'] # percentage

#plotting setup
plt.figure(0, figsize=(12, 8))
gs1 = GridSpec(3, 3)
gs1.update(left=0.15, right=0.95, wspace=0.3, hspace=0.15)

ax1 = plt.subplot(gs1[0,:])
plt.plot(loc_dt, temp, color='red', linewidth=2, alpha=.7)
plt.plot(loc_dt, temp, '.', color='red', alpha=.7)
plt.ylabel('Temperature / degrees C')

ax2 = plt.subplot(gs1[1,:])
plt.plot(loc_dt, pressure, color='blue',linewidth=2, alpha=.7)
plt.plot(loc_dt, pressure, '.', color='blue', alpha=.7)
ax = plt.gca()
ax.get_yaxis().get_major_formatter().set_useOffset(False) #turn off sci notation
plt.ylabel('Pressure / kPa')

ax3 = plt.subplot(gs1[2,:])
plt.plot(loc_dt, humidity, color='green',linewidth=2, alpha=.7)
plt.plot(loc_dt, humidity, '.', color='green', alpha=.7)
plt.xlabel('Date & Time')
plt.ylabel('Humidity / %')

plt.show()
plt.savefig('weather_data.pdf', format='pdf')
