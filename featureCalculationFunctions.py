__author__ = 'Jonathan'
import numpy as np
import scipy.stats as stats
import csv
import pywt
import re

from entropy import entropy_ci
from constants import *
from pyeeg import dfa
from itertools import *
from collections import deque

def getFieldNames(origNames, operations):
    newFields = [str(x) + '_' + str(y) for x,y in product(origNames, operations)]
    return  origNames + newFields

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

def _per_window_mean_TKEO(a):
    values = [y**2 - x*z for x, y, z in zip(a[:-2],a[1:-1],a[2:])]
    return reduce(lambda x, y: x+y, values)/(len(a)-2)



def windowHasFirstRow(timeWindow):
    match_exp = re.compile('([^\d]+)')
    firstFieldContents = timeWindow[0][0]
    return match_exp.search(firstFieldContents) == None

def waveletCompressForAllColoumns(timeWindow, shortTimeWindows, windowType):
    '''
    :param timeWindow:
    :param shortTimeWindows:
    :param windowType:
    :return:
    '''
    rows = []
    if windowHasFirstRow(timeWindow):
        origNames = timeWindow[1]
        newFirstRow = getFieldNames(origNames, [touple[1] for touple in stat_func_pointers])
        rows.append(newFirstRow)

    rows.append([])
    for column in timeWindow[1:].T:
        rows[len(rows)-1] += [func(column) for func in stat_func_pointers] # put the calculated fields in the correct row of result

    return np.array(rows)

stat_func_pointers = [(stats.tmax, 'max'),
                     (stats.tmin,'min' ),
                     (stats.trim_mean,'mean'),
                     (_mode, 'mode'),
                     (stats.tstd, 'std'),
                     (np.nanmedian, 'median'),
                     (stats.skew, 'skew'),
                     (stats.kurtosis, 'kurtosis'),
                     (_entropy, 'entropy'),
                     (stats.kurtosis, 'kurtosis'),
                     (_per_window_mean_TKEO, 'mean_TKEO')
                     ] #TODO add more functionsdc

freq_domain_func_pointers = [()

]
def statisticsForAllColoumns(timeWindow, shortTimeWindows, windowType):
    '''

    :param timeWindow:
    :param shortTimeWindows:
    :param windowType:
    :return:
    '''
    rows = []
    if windowHasFirstRow(timeWindow):
        origNames = timeWindow[1]
        newFirstRow = getFieldNames(origNames, [touple[1] for touple in stat_func_pointers])
        rows.append(newFirstRow)

    rows.append([])
    for column in timeWindow[1:].T:
        rows[len(rows)-1] += [func(column) for func in stat_func_pointers] # put the calculated fields in the correct row of result

    return np.array(rows)



def statsForLongTimeWindow():
    return

def statsForLongTimeWindow():
    return


# Functions for reducing windows into lines
def lowFreqsCounter(window, ):
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
