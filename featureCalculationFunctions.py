__author__ = 'Jonathan'
import numpy as np
import scipy.stats as stats
import scipy.fftpack as fft
import csv
import pywt
import re

from entropy import entropy_ci
from constants import *
from structuredDataConstants import accl_fields, audio_fields, psd_D
from pyeeg import dfa
from itertools import *
from collections import deque

def getFieldNames(origNames, modifiers):
    '''
    :param origNames:
    :param modifiers:
    :return: names of new fields: each field appended with all modifiers.
    '''
    newFields = [str(x) + '_' + str(y) for x,y in product(origNames, modifiers)]
    return  np.array(newFields)

def windowHasFirstRow(timeWindow):
    match_exp = re.compile('([^\d]+)')
    firstFieldContents = timeWindow[0][0]
    return match_exp.search(firstFieldContents) == None


def _mode(values): return stats.mode(values)[0][0]
def _range(a): return stats.tmax(a) - stats.tmin(a)
def _entropy(a): return entropy_ci(a, ENTROPY_RADIUS)
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


def _cross_correlation_accl(window, energy_type): #TODO: add cross_entropy from theano
    return

def _DFA(a): return dfa(a, DFA_WINDOW_LEN)

def _per_window_mean_TKEO(a):
    values = [y**2 - x*z for x, y, z in zip(a[:-2],a[1:-1],a[2:])]
    return reduce(lambda x, y: x+y, values)/(len(a)-2)

def _zero_crossing_rate(a):
    positive = a > 0
    negative = ~positive
    return ((positive[:-1] & negative[1:]) | (negative[:-1] & positive[1:])).nonzero()


#operates on sub windows
def samplesInFreqRange(window):
    fields = [accl_fields["x.PSD."+ str(psd_D[energy_type])] for energy_type in ['high', 'med', 'low']]
    freqData = np.array(window[:, fields])
    means = freqData.mean()
    if windowHasFirstRow(window):
        origNames = ["x.PSD."+ str(psd_D[energy_type]) for energy_type in ['high', 'med', 'low']]
        firstRow = getFieldNames(origNames, ['is_freq_in_range '])
        rows = firstRow
    else:
        rows = []
    rows.append((FREQ_H < means) & (means < FREQ_H))

    return np.array(rows)


# operates on windows
def subWindowsInFreqRange(window, energy_type):
    fields = [accl_fields["x.PSD."+ str(psd_D[energy_type]) + '_is_freq_in_range'] for energy_type in ['high', 'med', 'low']]
    freqData = np.array(window[:, fields])
    counts  = [len(np.where(column == 'True')) for column in freqData.T]

    if windowHasFirstRow(window):
        origNames = ["x.PSD."+ str(psd_D[energy_type]) for energy_type in ['high', 'med', 'low']]
        firstRow = getFieldNames(origNames, ['num_subWindows_in_freq_range'])
        rows = firstRow
    else:
        rows = []

    rows.append(counts)
    return np.array(rows)

    psd = str(psd_D[energy_type])
    freqData = np.array(window[:, accl_fields["x.PSD."+ psd + ""]])
    numSamplesInRange =  len(np.where((FREQ_H < freqData) & (freqData < FREQ_H)))  #TODO: decide on range of frequencies
    return



#operates on entire data
def waveletCompressForAllColoumns(timeWindow, shortTimeWindows, windowType):
    '''
    :param timeWindow:
    :param shortTimeWindows:
    :param windowType:
    :return: matrix as a list of lists
    '''
    rows = []
    origNames = timeWindow[1]
    newFirstRow = getFieldNames(origNames, ['DCT_coeff_'+ str(i) for i in range(1,NUM_COEFFS + 1)])
    rows.append(newFirstRow)

    coefients = np.array([fft.dct(column) for column in timeWindow[1:].T])
    coefients_means = np.mean(np.array(coefients), 0)
    sorted_indices = sorted(range(len(coefients_means)), key= lambda x: coefients_means[x], reverse= True)
    top_indices = sorted_indices[:NUM_COEFFS]
    del sorted_indices
    mask = np.zeros(len(coefients))
    mask[top_indices] = True
    # The following is the freq-domain representation after compression: compressed by taking the on-average-best coefficients
    top_coeffients = coefients[mask, :]
    return np.vstack((rows,np.ravel(top_coeffients)))

    # TODO: restore when we understand wavelet transform
    # # lists of lists of coeffients
    # app_coefients = []
    # detail_coefients = []
    # for column in timeWindow[1:].T:
    #     col_app_coefients, col_detail_coefients= pywt.dwt2(column, 'db2')
    #     app_coefients.append(col_app_coefients)
    #     detail_coefients.append(col_detail_coefients)
    # app_coefients_means = np.mean(np.array(app_coefients), 0)
    # sorted_indices = sorted(range(len(app_coefients_means)), key= lambda x: app_coefients_means[x])
    # top_indices = sorted_indices[:-NUM_COEFFS]
    # del sorted_indices
    # mask = np.zeros(len(app_coefients))
    # mask[sorted_indices] = True

stat_func_pointers = [
                     (stats.tmax, 'max'),
                     (stats.tmin,'min' ),
                     (stats.trim_mean,'mean'),
                     (stats.tstd, 'std'),
                     (stats.skew, 'skew'),
                     (stats.kurtosis, 'kurtosis'),
                     (stats.kurtosis, 'kurtosis'),
                     (np.nanmedian, 'median'),
                     (_mode, 'mode'),
                     (_entropy, 'entropy'),
                     (_per_window_mean_TKEO, 'mean_TKEO'),
                     (_zero_crossing_rate, 'zero_crossings')
                     ] #TODO add more functionsdc

freq_domain_func_pointers = [()]

#operates in a window
def statisticsForAllColoumns(timeWindow, shortTimeWindows, windowType):
    '''
    :param timeWindow:
    :param shortTimeWindows:
    :param windowType:
    :return:
    '''
    if windowHasFirstRow(timeWindow):
        origNames = timeWindow[1]
        newFirstRow = getFieldNames(origNames, [touple[1] for touple in stat_func_pointers])
        rows = [newFirstRow]
    else: rows = []

    row = []
    for column in timeWindow[1:].T:
        row += [func(column) for func in stat_func_pointers] # put the calculated fields in the correct row of result

    rows.append(row)
    return np.array(rows)



def statsForLongTimeWindow():
    return

def statsForLongTimeWindow():
    return