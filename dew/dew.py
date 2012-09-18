"""
Dew point calculation routines
"""
from __future__ import division
import numpy as np
import pylab as pl

# Constants from Wikipedia for the calculation
class Constants:
    # a = 6.112  # Not needed for Magnus, but for the higher accuracy modificiations
    b = 17.67
    c = 243.5  # degC

def Tdp(T, RH):
    """ Calculate dew point with the Magnus formula based on
    http://en.wikipedia.org/wiki/Dew_point

    """
    b, c = Constants.b, Constants.c
    g = np.log(RH/100) + b * T / (c + T)
    return c * g / (b - g)

def findhumidity(d, T):
    """ Calculate the relative humidity for a given dew point and
    temperature by reversing the Magnus formula

    """
    b, c = Constants.b, Constants.c
    return np.exp((d * b - (d + c) * b * T / (c + T)) / (c + d)) * 100


if __name__ == "__main__":
    T = 21
    RH = 60
    dp = Tdp(T, RH)
    print "Dew point: %.1f C" %(dp)

    Tlist = np.linspace(19, 30, 101)
    RHlist = np.array([findhumidity(dp, t) for t in Tlist])

    pl.plot(Tlist, RHlist, 'k-', linewidth=3)
    pl.plot([T, T], [min(RHlist), max(RHlist)], 'k--')
    pl.xlim([Tlist[0], Tlist[-1]])
    pl.grid()
    pl.ylim([min(RHlist), max(RHlist)])
    pl.xlabel('Temperature (C)')
    pl.ylabel('Relative Humidity (RH%)')

    pl.savefig("dewpoint.png")

    pl.show()
