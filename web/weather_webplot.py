import numpy as np
import os
import datetime
from datetime import timedelta
from pytz import utc, timezone
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.models import Range1d
from bokeh.embed import components

def wplot():
 #--------------------#
 
 #read csv file with data
 data=pd.read_csv('weather_data.csv', sep=',', header=0, engine='python')

 #--------------------#
 
 #time data
 time=np.array(data['isotime']) # in UTC isotime
 dt=[datetime.datetime.strptime(X, "%Y-%m-%dT%H:%M:%S.%f" ) for X in time]

 def to_pacific(dt):
  utc_dt = utc.localize(dt)
  pacific = timezone('US/Pacific')
  loc_dt = utc_dt.astimezone(pacific)  
  return loc_dt
 
 loc_dt=[to_pacific(X) for X in dt]

 #hack to make datetime64 in Pacific for bokeh plotting
 loc_np=[]
 for i in range(len(loc_dt)):
    shift=int(str(loc_dt[i])[-4:-3]) #datetime contains tzinfo
    utc_np=np.datetime64(loc_dt[i])
    loc_np.append(utc_np-np.timedelta64(shift, 'h')) #subtract timezone
 

 def dew_point(T, RH):
  #from https://en.wikipedia.org/wiki/Dew_point
  #T in Celsius
  #RH in %  (ie 65)
   b=17.67
   c=257.14
   d=234.5
   gamma = np.log ( RH/100. * np.exp ( (b - T / d) * (T / ( c +T ))))
   T_dp = ( c * gamma ) / (b - gamma )
   return T_dp  
 
 #weather data
 temp=np.array(data['temp']) * 9/5 + 32 # convert to F
 temp_mcp9808=np.array(data['temp_mcp9808']) * 9/5 + 32 # convert to F
 pressure=np.array(data['pressure']) *  0.000295299830714 #convert to inHg 
 humidity=np.array(data['humidity']) # percentage
 dew_p=[]
 for i in range(len(humidity)):
  dew_p.append((dew_point(data['temp'][i],data['humidity'][i])))
 dew_p=np.array(dew_p) * 9/5 + 32 # convert to F
 #--------------------#
  
 window_size = 30
 window = np.ones(window_size)/float(window_size)
 
 #xdata and ydata as list
 def line_plot(xdata, ydata, labels):
  pl = figure(width=800, height=350, x_axis_type="datetime")

  # add renderers
  for i in range(len(ydata)):
    pl.circle(xdata, ydata[i], size=4, color='darkgrey', alpha=0.2)
    pl.line(xdata, ydata[i], color=labels['color'][i])
  
  #set attributes
  pl.title.text = labels['title']
  pl.grid.grid_line_alpha=0
  pl.xaxis.axis_label = labels['xaxis']
  pl.yaxis.axis_label = labels['yaxis']
  pl.ygrid.band_fill_color="grey"
  pl.ygrid.band_fill_alpha = 0.1
  
  # set default xaxis range to most recent day
  pl.x_range = Range1d(loc_np[-1]-np.timedelta64(24, 'h'), loc_np[-1])

  return pl

 labels={"title":"Air Temperature", "xaxis":"Date (Pacific Time)", \
         "yaxis":"Temperature / degrees F", "color":["red", "orange"]}
 p1=line_plot(loc_np, [temp, temp_mcp9808], labels)
 
 labels={"title":"Barometric Pressure", "xaxis":"Date (Pacific Time)", \
          "yaxis":"Pressure / inHg","color":["green"]}
 p2=line_plot(loc_np, [pressure], labels)

 labels={"title":"Relative Humidity", "xaxis":"Date (Pacific Time)", \
          "yaxis":"Humdity / Percent", "color":["navy"]}
 p3=line_plot(loc_np, [humidity], labels)


 p = gridplot([[p1],[p2],[p3]])

 #--------------------#
 
 # output to static HTML file
 #output_file("weather.html", title="weather_station")
 #show(p)

 #OR, output to string variables which can be written into another html file
 script, div = components(p)

 #get latest photo
 dirname='pictures/'
 photos = filter(lambda x: '.jpg' in x.lower(),os.listdir(dirname+'.'))
 
 #also output latest values
 latest={'time':str(loc_np[-1]), 'temp':temp[-1], 'pressure':pressure[-1], \
         'humidity':humidity[-1], 'dew_point':dew_p[-1], 'photo':dirname+photos[-1]}
 
 return script, div, latest


###################################


if __name__ == "__main__":    
    
    script, div, latest = wplot()
