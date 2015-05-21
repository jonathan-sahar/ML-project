__author__ = 'Jonathan'
import numpy as np
import scipy.stats as stats
import csv
from entropy import entropy_ci
from constants import *
from pyeeg import dfa


def _mode(values): return stats.mode(values)[0][0]
def _range(a): return stats.tmax(a) - stats.tmin(a)
def _entropy(a): return entropy_ci(a, ENTROPY_RADIUS)

psd_D = {
    "low": 1,
    "mid": 3,
    "high":6
}
def _cross_correlation_accl(window, energy_type):
    '''
    :param window:
    :param energy_type: one of "low", "mid", "high"
    :return: cross correlation between movement in X and Y
    '''
    psd = str(psd_D[energy_type])
    a = window[:, accl_fields["x.PSD."+ psd]]
    b = window[:, accl_fields["y.PSD."+ psd]]
    return stats.pearsonr(a,b)[0]
#TODO: add cross_entropy from theano

def _DFA(a): return dfa(a, DFA_WINDOW_LEN)
def _per_window_TAKEO(a):
    values = [y**2 - x*z for x, y, z in zip(a[:-2],a[1:-1],a[2:])]
    return reduce(lambda x, y: x+y, values)/(len(a)-2)



def statisticsForAllColoumns(timeWindow, timeWindowLength, filePath, windowHasFirstRow):
    '''

    :param timeWindow:
    :param timeWindowLength:
    :param filePath:
    :param windowHasFirstRow:
    :return: a np.array, either one line of data OR two lines - one titles and one data
    '''
    func_pointers = [(stats.tmax, 'max'),
                     (stats.tmin,'min' ),
                     (stats.trim_mean,'mean'),
                     (_mode, 'mode'),
                     (stats.tstd, 'std'),
                     (np.nanmedian, 'median'),
                     (stats.skew, 'skew'),
                     (stats.kurtosis, 'kurtosis'),
                     (_entropy, 'entropy'),
                     (stats.kurtosis, 'kurtosis'),

                                ] #TODO add more functions

    data = []
    newLine = [] #values will hold a matrix
    reader = csv.reader(filePath)
    if windowHasFirstRow:
        newLine += reader.next()
        newLine.append([])
    for row in reader:
        data.append(row)
    data = np.array(data)
    for column in data.T:
        newLine[len(newLine)-1] += [func(column) for func in func_pointers]
    return np.array(newLine)



def statsForLongTimeWindow():
    return

def statsForLongTimeWindow():
    return

def lowFreqsCounter(window, shortTimeWindowPath):
    #if isLongTimeWindow == 0:
     #   return [] #TODO assert this
    numberOfrows = LONG_TIME_WINDOW/SHORT_TIME_WINDOW
    data = []
    shortTimeWindowFile = open(shortTimeWindowPath)
    reader = csv.reader(shortTimeWindowFile)
    row = reader.next()
    columbs = row.split(',')
    index = columbs.index('lowFreq') #TODO this is the name?
    lineCounter = 0
    thresholdCounter = 0
    for row in reader:
        columbs = row.split(',')
        if columbs[index] == 1:
            thresholdCounter+=1
        if lineCounter == numberOfrows - 1:
            data.append(thresholdCounter)
            thresholdCounter = 0
        lineCounter = ((lineCounter+1) % numberOfrows)
    return data


def lowFreqShortWindow(filePath, isLongTimeWindow, shotTimeWindowPath):
    #if isLongTimeWindow == 1:#TODO find their threshold
     #   return [] #TODO assert this


    return
