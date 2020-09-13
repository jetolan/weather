import numpy as np
import os
import datetime
import glob
from datetime import timedelta
from pytz import utc, timezone
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.models import Range1d
from bokeh.embed import components


def local_time(dt):
    # input is list of datetime, output is list of np.datetime

    def to_pacific(dt):
        utc_dt = utc.localize(dt)
        loc_dt = utc_dt.astimezone(timezone('US/Pacific'))
        return loc_dt

    loc_dt = [to_pacific(X) for X in dt]

    # hack to make datetime64 in Pacific for bokeh plotting
    loc_np = []
    for i in range(len(loc_dt)):
        shift = int(str(loc_dt[i])[-4:-3])  # datetime contains tzinfo
        utc_np = np.datetime64(loc_dt[i])
        loc_np.append(utc_np-np.timedelta64(shift, 'h'))  # subtract timezone

    return loc_np


def dew_point(T, RH):
        # from https://en.wikipedia.org/wiki/Dew_point
        #T in Celsius
        # RH in %  (ie 65)
    b = 17.67
    c = 257.14
    d = 234.5
    gamma = np.log(RH/100. * np.exp((b - T / d) * (T / (c + T))))
    T_dp = (c * gamma) / (b - gamma)
    return T_dp


def line_plot(xdata, ydata, labels, now):
        # xdata and ydata as list
    pl = figure(width=800, height=350, x_axis_type="datetime")

    # add renderers
    for i in range(len(ydata)):
        pl.circle(xdata, ydata[i], size=4, color='darkgrey', alpha=0.2)
        pl.line(xdata, ydata[i], color=labels['color'][i])

    # set attributes
    pl.title.text = labels['title']
    pl.grid.grid_line_alpha = 0
    pl.xaxis.axis_label = labels['xaxis']
    pl.yaxis.axis_label = labels['yaxis']
    pl.ygrid.band_fill_color = "grey"
    pl.ygrid.band_fill_alpha = 0.1

    # set default xaxis range to most recent day
    pl.x_range = Range1d(now-np.timedelta64(24, 'h'), now)

    return pl


def rain_bin(data, now):
    dt = [datetime.datetime.strptime(X, "%Y-%m-%dT%H:%M:%S.%f")
          for X in data['isotime']]
    dt_np = np.array(dt)

    # first date:
    d0 = datetime.datetime(int(dt[0].year), int(
        dt[0].month), int(dt[0].day), int(dt[0].hour))

    # bin rain data into intervals
    # length of binning interval:
    interval = 30  # min

    # conversion from tips to inches of rain:
    # 2tips = 1/2 tsp = 2.46 mL = 2.46cm^3
    # diameter of funnel = 3 7/8 inch = 9.8425 cm
    # Area = (9.8425/2)**2*pi=76.085cm^2
    # 2 tip = 2.46 / 76.085 cm = 0.03233cm = 0.0127inches
    # 1 tip = 0.00635
    tip_conversion = 0.00635

    dates = []
    val = []
    # find rainfall in interval
    while d0 < now:
        dates.append(d0)
        d1 = d0+datetime.timedelta(minutes=interval)
        mask = (dt_np >= d0) & (dt_np < d1)
        val.append(np.sum(mask)*tip_conversion)
        d0 = d1

    # double points to make bar plot
    xarray = []
    yarray = []
    for d in range(len(dates)-1):
        xarray.append(dates[d])
        xarray.append(dates[d+1])
        yarray.append(val[d])
        yarray.append(val[d])  # repeat value twice, shifting indices

    return xarray, yarray


def wplot():

    # read csv file with temperture, pressure and humidity dataa
    #--------------------#
    data = pd.read_csv('weather_data.csv', sep=',', header=0)
    # localize time
    time = np.array(data['isotime'])  # in UTC isotime
    dt = [datetime.datetime.strptime(X, "%Y-%m-%dT%H:%M:%S.%f") for X in time]
    loc_np = local_time(dt)

    # read csv file with rainfall data
    #--------#
    rain_data = pd.read_csv('rain_data.csv', sep=',', header=0)
    # bin rain data
    xarray_utc, yarray = rain_bin(rain_data, dt[-1])
    xarray = local_time(xarray_utc)
    # make 24hr rain total:
    int24 = np.array(xarray) > (xarray[-1]-np.timedelta64(24, 'h'))
    int24[::2] = False  # don't double count bar plotted xarray
    yarray_np = np.array(yarray)
    rain24hr = np.sum(yarray_np[int24])

    # conversions for weather data
    #--------------------#
    temp = np.array(data['temp']) * 9/5 + 32  # convert to F
    # temp_mcp9808=np.array(data['temp_mcp9808']) * 9/5 + 32 # convert to F
    pressure = np.array(data['pressure']) * \
        0.000295299830714  # convert to inHg
    humidity = np.array(data['humidity'])  # percentage
    dew_p = []
    for i in range(len(humidity)):
        dew_p.append((dew_point(data['temp'][i], data['humidity'][i])))
    dew_p = np.array(dew_p) * 9/5 + 32  # convert to F
    power = np.array(data['power'])

    # plotting
    #--------------------#
    # labels={"title":"Air Temperature", "xaxis":"Date (Pacific Time)", \
    #        "yaxis":"Temperature / degrees F", "color":["red", "orange"]}
    #p1=line_plot(loc_np, [temp, temp_mcp9808], labels, loc_np[-1])
    labels = {"title": "Air Temperature", "xaxis": "Date (Pacific Time)",
              "yaxis": "Temperature / degrees F", "color": ["red"]}
    p1 = line_plot(loc_np, [temp], labels, loc_np[-1])

    labels = {"title": "Barometric Pressure", "xaxis": "Date (Pacific Time)",
              "yaxis": "Pressure / inHg", "color": ["green"]}
    p2 = line_plot(loc_np, [pressure], labels, loc_np[-1])

    labels = {"title": "Relative Humidity", "xaxis": "Date (Pacific Time)",
              "yaxis": "Humidity / Percent", "color": ["navy"]}
    p3 = line_plot(loc_np, [humidity], labels, loc_np[-1])

    labels = {"title": "Rainfall", "xaxis": "Date (Pacific Time)",
              "yaxis": "inches", "color": ["blue"]}

    p4 = line_plot(xarray, [yarray], labels, loc_np[-1])

    labels = {"title": "Solar Power", "xaxis": "Date (Pacific Time)",
              "yaxis": "power / mW", "color": ["navy"]}
    p5 = line_plot(loc_np, [power], labels, loc_np[-1])

    p = gridplot([[p1], [p2], [p3], [p4], [p5]])

    # output
    #--------------------#

    # output to static HTML file
    #output_file("weather.html", title="weather_station")
    # show(p)

    # OR, output to string variables which can be written into another html file
    script, div = components(p)

    # get latest photo
    dirname = 'pictures/'
    files = glob.glob(dirname+'.jpg')
    if any(files):
        photos = np.sort(photos)
    else:
        photos = "none.jpg"

    # also output latest values
    latest = {'time': str(loc_np[-1]), 'temp': temp[-1], 'pressure': pressure[-1],
              'humidity': humidity[-1], 'dew_point': dew_p[-1],
              'photo': dirname+photos[-1], 'rainfall': rain24hr}

    return script, div, latest


###################################


if __name__ == "__main__":

    script, div, latest = wplot()
