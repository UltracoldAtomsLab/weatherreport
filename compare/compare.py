# -*- coding: utf-8 -*-
import numpy as np
import pylab as pl
import datetime
import pytz
import time
from time import mktime
from matplotlib.dates import strpdate2num, epoch2num, num2date

tz = pytz.timezone('Asia/Taipei')


logfile = "2012_0828_15_26pm.csv"
# logfile = "test3.csv"
def dateconv(s):
    date, time = s.split(' ')
    month, day, year = [int(x) for x in date.split('/')]
    time = time.decode('utf-8')
    hour = int(time[2:4])    
    if time[0] != u'上':
        if hour < 12:
            hour += 12
    elif hour == 12:
        hour = 0
    minute = int(time[5:7])
    second = int(time[8:9])
    thisdate = datetime.datetime(2000+year, month, day, hour, minute, second, 0)
    return float(mktime(thisdate.timetuple()))

dt=np.dtype({'names':['date','temperature','humidity'],'formats':[np.float, np.float, np.float]})
logdate, temperature, humidity = np.loadtxt(logfile,
                                         delimiter=',',
                                         comments="\"",
                                         usecols=(1, 2, 3),
                                         converters = {1: lambda x: dateconv(x), 2: lambda x: np.nan if x == "" else float(x), 3: lambda x: np.nan if x == "" else float(x)},
                                         dtype=dt,
                                         unpack=True)

newdate = epoch2num(logdate)
# print date
# newdate = date[:]
print newdate
fig = pl.figure(figsize=(11.27, 8.69))

ax1 = fig.add_subplot(211)
ax1.plot_date(newdate, humidity, 'k-')
ax1.set_ylabel("Humidity (%)")

ax2 = fig.add_subplot(212)
ax2.plot_date(newdate, temperature, 'k.')
ax2.set_ylabel("Temperature (C)")
fig.autofmt_xdate()


pl.show()
