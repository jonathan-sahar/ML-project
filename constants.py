__author__ = 'Jonathan'

LONG_TIME_WINDOW = 300
SHORT_TIME_WINDOW = 5
ENTROPY_RADIUS = 5

DFA_WINDOW_LEN = 10 # no. of lines

CONTROL = ['APPLE', 'DAFODIL', 'LILLY', 'LILY', 'ORANGE', 'ROSE', 'SUNFLOWER', 'SWEETPEA']
SICK_PATIENTS = ['CHERRY', 'CROCUS', 'DAISY', 'DAISEY', 'FLOX', 'IRIS', 'MAPLE', 'ORCHID', 'PEONY', 'VIOLET']
PATIENTS = SICK_PATIENTS+CONTROL

PATIENTS_test = ['VIOLET'] # TODO: for testing!

UNDERLINES_BEFORE_NAME = 2
DATA_LEN = 1000000000

ROOT_DATA_FOLDER = 'C:\ML\parkinson\FIRSTDATA'
UNIFIED_TABLES_PATH = 'C:\ML\parkinson\FIRSTDATA\Unified Tables'
DATA_TABLE_FILE_PATH = 'C:\ML\parkinson\Unified Tables\DATAFile.csv'
SHORT_TABLE_FILE_PATH = 'C:\ML\parkinson\FIRSTDATA\Unified Tables\SHORTFile.csv'
LONG_TABLE_FILE_PATH = 'C:\ML\parkinson\FIRSTDATA\Unified Tables\LONGFile.csv'
ENTIRE_TABLE_FILE_PATH = 'C:\ML\parkinson\FIRSTDATA\Unified Tables\ENTIREFile.csv'

# ROOT_DATA_FOLDER = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample'
# DATA_TABLE_FILE_PATH = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample\Unified Tables\unified_table.csv'
# UNIFIED_TABLES_PATH = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample\Unified Tables'
# SHORT_TABLE_FILE_PATH = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample\Unified Tables\SHORTFile.csv'
# LONG_TABLE_FILE_PATH = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample\Unified Tables\LONGFile.csv'
# ENTIRE_TABLE_FILE_PATH = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample\Unified Tables\ENTIREFile.csv'

NUM_COEFFS = 5

FREQ_H = 5 #Hz
FREQ_L = 10

MAX_TIME_DIFF = 2 #seconds

delete = False

#Set logging options


# LOG_LEVEL = 'DEBUG'
# numeric_level = getattr(logging, LOG_LEVEL, None)
# logging.basicConfig(level=numeric_level)

# FOR TESTING PURPOSES ONLY
from collections import Counter
def print_doubled_fields(names):
    l = [item for item, count in Counter(names).items() if count > 1]
    if len(l) > 0:
        print "duplicate field names: {}".format(l)
    else: print "~ No duplicates! ~"


def restore_data():
    from distutils.dir_util import  copy_tree
    orig_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample_orig'
    testing_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample'
    copy_tree(orig_data_folder, testing_data_folder)

import logging
LOG_LEVEL = 'INFO'
logger = logging.getLogger('tipper')
logger.addHandler(logging.StreamHandler())
logger.setLevel(getattr(logging, LOG_LEVEL, None))



