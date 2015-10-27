__author__ = 'Jonathan'
from collections import Counter
import logging
import re
import csv
import numpy as np
from constants import *

def print_doubled_fields(names):
    l = [item for item, count in Counter(names).items() if count > 1]
    if len(l) > 0:
        print "duplicate field names: {}".format(l)
    else:
        print "~ No duplicates! ~"


def restore_data(orig_data_folder, testing_data_folder):
    from distutils.dir_util import  copy_tree
    copy_tree(orig_data_folder, testing_data_folder)


LOG_LEVEL = 'WARN'
# LOG_LEVEL = 'INFO'
# LOG_LEVEL = 'DEBUG'
logger = logging.getLogger('tipper')
logger.addHandler(logging.StreamHandler())
logger.setLevel(getattr(logging, LOG_LEVEL, None))

def readFileToFloat(filePath, dt = float, names = True):
    '''
    Assumes file  contains headers
    :param filePath:
    :return:
    '''
    newFile = open(filePath, 'r')
    data = np.genfromtxt(filePath, dtype=dt, delimiter=',', names = names, case_sensitive=True)
    if not names:
        return data
    field_names = np.array(data.dtype.names)
    r = re.compile(r'(.*time.*|.*patient.*|.*sick.*)',re.IGNORECASE)
    vmatch = np.vectorize(lambda x:bool(r.match(x)))
    mask = ~vmatch(field_names) # mask is true where field name doesn't contain 'time' or 'patient'
    return data[list(field_names[mask])]


def readFileAsIs(filePath):
    newFile = open(filePath, 'r')
    reader = csv.reader(newFile)
    allLines = [row for row in reader]
    newFile.close()
    return allLines

def castStructuredArrayToRegular(arr):
    return arr.view((np.float, len(arr.dtype.names)))

def filter_fields_by_name(names, regex, inverse = False):
    '''
    :param names:
    :param regex:
    :return: an array of names that the regex matched on
    '''
    vmatch = np.vectorize(lambda x:bool(regex.match(x)))
    mask = vmatch(names) #mask is True where name is matched by the regex
    if inverse: mask = ~mask
    indices = np.where(mask)[0]
    return np.array(names)[indices]

def getRandomSample(percent):
    '''

    :param percent:  ratio of original data to return 1%, 10% etc
    :return:
    '''
    X = readFileToFloat(UNIFIED_AGGREGATED_DATA_PATH)
    y = readFileToFloat(UNIFIED_AGGREGATED_LABELS_PATH, names = None)
    patientNames = np.array(readFileAsIs(UNIFIED_AGGREGATED_PATIENT_NAMES_PATH)[0])
    if percent == 100:
        return (X, y, patientNames)

    idxs = np.random.randint(len(X), size = percent * len(X) / 100)
    X = X[idxs]
    y = y[idxs]
    patientNames = patientNames[idxs]

    return (X, y, patientNames)
    # return (X, y)
