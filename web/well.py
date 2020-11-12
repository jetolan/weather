import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt


def well_bin(data, now):
    dt_np = pd.to_datetime(pd.to_datetime(data.isotime).values)
    now_dt = pd.to_datetime(now)

    # first date:
    d0 = datetime.datetime(int(dt_np[0].year), int(
        dt_np[0].month), int(dt_np[0].day), int(dt_np[0].hour))

    # bin rain data into intervals
    # length of binning interval:
    interval = 5  # min

    # conversion from tips to gallons
    tip_conversion = 1

    dates = []
    val = []
    # find rainfall in interval
    while d0 < now_dt:
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


def well_plot(filename):
    df = pd.read_csv(filename)
    time = pd.to_datetime(df.isotime).values
    df['time'] = time
    xx, yy = well_bin(df, time[-1])
    plt.subplot(2, 1, 1)
    plt.plot(xx, yy)
    plt.ylabel('Gallons')
    plt.xlabel('Time')
    plt.subplot(2, 1, 2)
    df['rain_tip'].groupby([df["time"].dt.year, df["time"].dt.month,
                            df["time"].dt.day, df["time"].dt.hour]).count().plot(kind="bar")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    return df


if __name__ == "__main__":
    filename = '/Users/jetolan/Desktop/rain_data.csv'
    df = well_plot(filename)
