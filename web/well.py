import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

TIP_CONV = 0.5


def well_bin(data, now, interval=10):
    """
    interval: int
       length of binning interval
       In minutes
    """

    dt_np = pd.to_datetime(pd.to_datetime(data.isotime).values)
    now_dt = pd.to_datetime(now)

    # first date:
    d0 = datetime.datetime(int(dt_np[0].year), int(
        dt_np[0].month), int(dt_np[0].day), int(dt_np[0].hour))

    # conversion from tips to gallons
    tip_conversion = TIP_CONV

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
        yarray.append(val[d]/interval)
        yarray.append(val[d]/interval)  # repeat value twice, shifting indices

    return xarray, yarray


def df_plot(df, interval=1):
    plt.figure()
    xx, yy = well_bin(df, df.time.values[-1], interval=interval)
    plt.subplot(2, 1, 1)
    plt.plot(xx, yy)
    plt.xticks(rotation=90)
    plt.ylabel('Gallons per min')
    plt.xlabel('Time')
    plt.subplot(2, 1, 2)
    df['rain_tip'].groupby([df["time"].dt.year, df["time"].dt.month,
                            df["time"].dt.day]).count().multiply(TIP_CONV).plot(kind="bar")
    plt.xticks(rotation=90)
    plt.ylabel('Gallons per day')
    plt.xlabel('Time')
    plt.tight_layout()
    #plt.show()
    return df


def read_csv(filename):
    df = pd.read_csv(filename)
    df = df.dropna()
    time = pd.to_datetime(df.isotime).values
    df['time'] = time
    return df


def well_plot(filename):
    df = read_csv(filename)
    df_plot(df)
    print(filename)
    plt.savefig(filename.replace('.csv', '.png'))
    plt.show()
    return df


if __name__ == "__main__":
    filename = 'well_data_20201101.csv'
    filename = 'well_data_20201213.csv'
    filename = 'well_data_20201224.csv'
    filename = 'well_data_20210126.csv'
    filename = 'well_data_20210411.csv'
    filename = 'well_data_20210530.csv'
    filename = 'well_data_20210718.csv'
    filename = 'well_data_20221125.csv'
    df = well_plot(filename)
    ff = df[(df['time'] > '2021-03-29') & (df['time'] < '2021-03-30')]

    '''
    df = read_csv(filename)
    #ff=df[df['time']>'2020-12-24']
    ff = df[(df['time'] > '2021-01-20') & (df['time'] < '2021-01-24')]
    df_plot(ff)
    '''
