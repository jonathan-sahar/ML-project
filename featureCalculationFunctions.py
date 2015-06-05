__author__ = 'Jonathan'
import re
import numpy as np
from itertools import product

import scipy.stats as stats
import scipy.fftpack as fft
from pyeeg import dfa
from entropy import entropy_ci

from constants import *
from structuredDataConstants import accl_fields, audio_fields, psd_D

def getFieldNames(origNames, modifiers):
    '''
    :param origNames:
    :param modifiers:
    :return: names of new fields: each field appended with all modifiers.
    '''
    newFields = [str(x) + '_' + str(y) for x,y in product(origNames, modifiers)]
    return  np.array(newFields)

def windowHasFirstRow(timeWindow):
    match_exp = re.compile('([A-Za-z]+)')
    firstFieldContents = str(timeWindow[0][0])
    return (match_exp.search(firstFieldContents) != None)


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
    a = window[:, accl_fields["x_PSD."+ psd]]
    b = window[:, accl_fields["y_PSD."+ psd]]
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
    v = ((positive[:-1] & negative[1:]) | (negative[:-1] & positive[1:]))
    w = np.where(v)
    return [len(w)]

#operates on sub windows
def numSamplesInFreqRange(window):
    fields = [accl_fields["x_PSD_"+ str(psd_D[energy_type])] for energy_type in ['high', 'med', 'low']]
    if windowHasFirstRow(window):
        origNames = ["x_PSD_"+ str(psd_D[energy_type]) for energy_type in ['high', 'med', 'low']]
        firstRow = getFieldNames(origNames, ['is_freq_in_range '])
        rows = firstRow
        window = np.array(window[1:][:])
    else:
        window = np.array(window[:][:])
        rows = []

    print window.shape
    freqData = window[:,fields]
    means = freqData.mean(0)
    rows.append((FREQ_L < means) & (means < FREQ_H))

    return np.array(rows)


# operates on windows
def numSubWindowsInFreqRange(window, energy_type):
    fields = [accl_fields["x_PSD_"+ str(psd_D[energy_type]) + '_is_freq_in_range'] for energy_type in ['high', 'med', 'low']]
    freqData = np.array(window[:, fields])
    counts  = [len(np.where(column == 'True')) for column in freqData.T]
    origNames = ["x_PSD_"+ str(psd_D[energy_type]) for energy_type in ['high', 'med', 'low']]
    firstRow = getFieldNames(origNames, ['num_subWindows_in_freq_range'])
    rows = firstRow
    rows.append(counts)
    return np.array(rows)



#operates on entire data
def waveletCompressForAllColoumns(timeWindow, shortTimeWindows = None, windowType = 'long'):
    '''
    :param timeWindow:
    :param shortTimeWindows:
    :param windowType:
    :return: matrix as a list of lists
    '''
    rows = []
    fieldNames = timeWindow.dtype.names
    headers = getFieldNames(fieldNames, ['DCT_coeff_'+ str(i) for i in range(1,NUM_COEFFS + 1)])
    print "headers: ", len(fieldNames)
    coefficients = np.array([fft.dct(timeWindow[field]) for field in fieldNames]).T
    print "coeff: ", coefficients.shape
    coefficient_means = np.mean(np.array(coefficients), 0)
    print "coeff means: ", coefficient_means.shape
    sorted_indices = sorted(range(len(coefficient_means)), key= lambda x: coefficient_means[x], reverse= True)
    print "sorted idx: ", len(sorted_indices)
    top_indices = sorted_indices[:NUM_COEFFS]
    print "top idx: ", top_indices
    del sorted_indices
    mask = np.zeros(len(fieldNames), dtype = bool)
    print "mask: ", mask.shape

    mask[top_indices] = True
    # The following is the freq-domain representation after compression: compressed by taking the on-average-best coefficients
    top_coefficients = coefficients.T[mask, :]
    return headers,np.ravel(top_coefficients)

    # TODO: restore when we understand wavelet transform
    # # lists of lists of coefficients
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
                     (stats.tmean,'mean'),
                     (stats.tstd, 'std'),
                     (stats.skew, 'skew'),
                     (stats.kurtosis, 'kurtosis'),
                     (np.nanmedian, 'median'),
                     (_mode, 'mode'),
                     (_per_window_mean_TKEO, 'mean_TKEO'),
                     (_zero_crossing_rate, 'zero_crossings')
                     ] #TODO add more functionsdc

freq_domain_func_pointers = [()]

#operates in a window
def statisticsForAllColoumns(timeWindow, shortTimeWindows = None, windowType = 'long'):
    '''
    :param timeWindow:
    :param shortTimeWindows:
    :param windowType:
    :return: a list of names and an np.array of values
    '''
    names = [name for name in timeWindow.dtype.names if not name == "Is Sick"]
    fieldNames = getFieldNames(names, [touple[1] for touple in stat_func_pointers])
    row = np.atleast_2d([])
    columns = [timeWindow[fieldName] for fieldName in names]
    for column in columns:
        # print column
        features_from_col = [np.array((func(column))) for func, _ in stat_func_pointers]
        v= np.array([features_from_col])
        row = np.hstack((row, v))
    row = np.array(row)
    return fieldNames, row

#meant for 'entire' data
def averageOnWindows(timeWindow, longTimeWindows = None, windowType = 'entire'):
    columns = longTimeWindows.dtype.names
    means = [np.array(timeWindow[column]).mean() for column in columns]
    return columns, means

def statsForLongTimeWindow():
    return
