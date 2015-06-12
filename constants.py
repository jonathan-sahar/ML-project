from chaco.tests.serializable_base import Root

__author__ = 'Jonathan'
import  os
LONG_TIME_WINDOW = 300
SHORT_TIME_WINDOW = 5
ENTROPY_RADIUS = 5
DFA_WINDOW_LEN = 10 # no. of lines

CONTROL = ['APPLE', 'DAFODIL', 'LILLY', 'ORANGE', 'ROSE', 'SUNFLOWER', 'SWEETPEA'] # 'LILY'
SICK_PATIENTS = ['CHERRY', 'CROCUS', 'DAISY',  'FLOX', 'IRIS', 'MAPLE', 'ORCHID', 'PEONY', 'VIOLET'] # 'DAISEY'
PATIENTS = SICK_PATIENTS+CONTROL

PATIENTS_test = ['APPLE'] #, 'VIOLET', 'DAISY'] # TODO: for testing!

# ROOT_DATA_FOLDER = 'C:\ML\parkinson\FIRSTDATA'
# UNIFIED_TABLES_FOLDER = 'C:\ML\parkinson\FIRSTDATA\Unified Tables'
# DATA_TABLE_FILE_PATH = 'C:\ML\parkinson\Unified Tables\DATAFile.csv'
# SHORT_TABLE_FILE_PATH = 'C:\ML\parkinson\FIRSTDATA\Unified Tables\SHORTFile.csv'
# LONG_TABLE_FILE_PATH = 'C:\ML\parkinson\FIRSTDATA\Unified Tables\LONGFile.csv'
# ENTIRE_TABLE_FILE_PATH = 'C:\ML\parkinson\FIRSTDATA\Unified Tables\ENTIREFile.csv'

SHORT_TABLE_PREFIX = 'SHORTFILE'
LONG_TABLE_PREFIX = 'LONGFILE'
ENTIRE_TABLE_PREFIX = 'ENTIREFILE'

# ROOT_DATA_FOLDER = 'D:\Documents\Technion - Bsc Computer Science\ML Project\EXTRACTED MJFF Partial Data'
ROOT_DATA_FOLDER = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample'
UNIFIED_TABLES_FOLDER = os.path.join(ROOT_DATA_FOLDER, 'Unified Tables')

DATA_TABLE_FILE_PATH = os.path.join(UNIFIED_TABLES_FOLDER, 'unified_data.csv')

UNIFIED_ENTIRE_PATH = os.path.join(UNIFIED_TABLES_FOLDER, 'unified_entire.csv')
UNIFIED_AGGREGATED_PATH = os.path.join(UNIFIED_TABLES_FOLDER, 'unified_aggregated_subWindows.csv')

UNIFIED_ENTIRE_LABELS_FILENAME = 'unified_entire_labels.csv'
UNIFIED_AGGREGATED_LABELS_FILENAME = 'unified_aggregated_labels.csv'
UNIFIED_ENTIRE_LABELS_PATH = os.path.join(UNIFIED_TABLES_FOLDER ,UNIFIED_ENTIRE_LABELS_FILENAME)
UNIFIED_AGGREGATED_LABELS_PATH = os.path.join(UNIFIED_TABLES_FOLDER ,UNIFIED_AGGREGATED_LABELS_FILENAME)


NUMBER_OF_ENTIRE_FEATURES = 40 #TODO not correct
NUMBER_OF_FIVE_MINUTES_FEATURES = 40 #TODO not correct
NUMBER_OF_FOLDS = 3 #16 choose 2


entireFeatures = []
longWindowsFeatures = []

NUM_COEFFS = 5

FREQ_L = 0.0161267947405577 #Hz?
FREQ_H = 0.059893537312746

MAX_TIME_DIFF = 2 #seconds

delete = False


# FOR TESTING PURPOSES




