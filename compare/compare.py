# -*- coding: utf-8 -*-
import numpy as np
import pylab as pl
from datetime import datetime
import time
from time import mktime, strptime
from matplotlib.dates import epoch2num, num2date
import sys
import ConfigParser as cp
from pytz import timezone
from pymongo import Connection
from calendar import timegm

dt = np.dtype({'names':['date','temperature','humidity'],
               'formats':[np.float, np.float, np.float]})

def loadlog(logfile):
    """
    Read logs from the UB10, exported to CSV
    Date format needs to be "09/13/2012 11:12:13 AM"

    Returns anumpy array with three columns, and addressable as 'date', 'temperature', 'humidity'
    """
    logs  = np.loadtxt(logfile,
                       delimiter=',',
                       comments="\"",
                       usecols=(1, 2, 3),
                       converters = {1: lambda x: mktime(strptime(x, "%m/%d/%Y %I:%M:%S %p")),
                                     2: lambda x: np.nan if x == "" else float(x),
                                     3: lambda x: np.nan if x == "" else float(x)},
                       dtype=dt,
                       unpack=False,
                       skiprows=2
                       )
    return logs

def getremote(server, port, limits):
    """
    Download data from mongo server according to settings
    between the given time limits

    server
    port
    limits = (start, finish) in unixtime
    """
    connection = Connection(server, port)
    db = connection.weather
    coll = db.readings

    datenow = datetime.fromtimestamp(limits[1], tz)
    datelimit = datetime.fromtimestamp(limits[0], tz)

    results = coll.find({'date': {"$gte": datelimit, "$lte": datenow}})
    num = results.count()
    logs = np.zeros((num, ), dtype=dt)

    for i, point in enumerate(results):
        date = timegm(point['date'].timetuple())
        try:
            logs['date'][i] = date
            logs['humidity'][i] = point['humidity']
            logs['temperature'][i] = point['temperature']
        except (IndexError):
            pass
    return logs, datenow, datelimit

def doplot(series):
    """
    Do the actual plotting of the series
    Needs data with the given dtypes to be able to address the
    'date', 'humidity', 'temperature' columns
    """
    fig = pl.figure(figsize=(11.27, 8.69))
    dates = [num2date(epoch2num(s[0]['date']), tz) for s in series]

    ax1 = fig.add_subplot(211)
    for i, s in enumerate(series):
        ax1.plot_date(dates[i], s[0]['humidity'], '-', label=s[1])
    ax1.set_ylabel("Humidity (%)")
    ax1.legend(loc='best')
    fig.autofmt_xdate()

    ax2 = fig.add_subplot(212)
    signs = ['s', 'x', 'o']
    for i, s in enumerate(series):
        ax2.plot_date(dates[i], s[0]['temperature'], signs[i % len(signs)], label=s[1])
    ax2.set_ylabel("Temperature (C)")
    ax2.legend(loc='best')
    fig.autofmt_xdate()

    ax1.set_title("%s -> %s" %(dates[0][0], dates[0][-1]))

if __name__ == "__main__":
    if len(sys.argv) > 2:
        configfile = sys.argv[1]
        infile = sys.argv[2]
    else:
        print "No configuration/input given!\nusage: compare.py configfile logfile"
        sys.exit(1)

    config = cp.ConfigParser()
    config.read(configfile)

    tz = timezone(config.get('Setup', 'timezone'))
    dbhost, dbport = config.get('Database', 'dbhost'), config.getint('Database', 'dbport')

    ub = loadlog(infile)
    start, finish = ub['date'][0], ub['date'][-1]
    limits = (start, finish)
    ws, d1, d2 = getremote(dbhost, dbport, limits)

    np.save('%s.ub.npy' %infile, ub)
    np.save('%s.ws.npy' %infile, ws)
    # ub = np.load('ub.npy')
    # ws = np.load('ws.npy')

    doplot([(ws, 'WeatherStation'), (ub, 'U10'),])
    pl.savefig("%s.png" %infile)

    pl.show()
