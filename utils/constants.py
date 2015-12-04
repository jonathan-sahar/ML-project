__author__ = 'Jonathan'
import  os
LONG_TIME_WINDOW = 300
SHORT_TIME_WINDOW = 5
ENTROPY_RADIUS = 5
DFA_WINDOW_LEN = 10 # no. of lines
NUM_OF_BASIC_FEATURES = 50

CONTROL = ['APPLE', 'DAFODIL', 'LILLY', 'ORANGE', 'ROSE', 'SUNFLOWER', 'SWEETPEA'] # 'LILY'
SICK_PATIENTS = ['CHERRY', 'CROCUS', 'DAISY',  'FLOX', 'IRIS', 'MAPLE', 'ORCHID', 'PEONY', 'VIOLET'] # 'DAISEY'
PATIENTS = SICK_PATIENTS+CONTROL

PATIENTS_test = PATIENTS # TODO: for testing!

# ROOT_DATA_FOLDER = 'C:\ML\parkinson\FIRSTDATA
# UNIFIED_TABLES_FOLDER = 'C:\ML\parkinson\FIRSTDATA\Unified Tables'
# DATA_TABLE_FILE_PATH = 'C:\ML\parkinson\Unified Tables\DATAFile.csv'
# SHORT_TABLE_FILE_PATH = 'C:\ML\parkinson\FIRSTDATA\Unified Tables\SHORTFile.csv'
# LONG_TABLE_FILE_PATH = 'C:\ML\parkinson\FIRSTDATA\Unified Tables\LONGFile.csv'
# ENTIRE_TABLE_FILE_PATH = 'C:\ML\parkinson\FIRSTDATA\Unified Tables\ENTIREFile.csv'

SHORT_TABLE_PREFIX = 'SHORTFILE'
LONG_TABLE_PREFIX = 'LONGFILE'
ENTIRE_TABLE_PREFIX = 'ENTIREFILE'

#Jonathan
#ROOT_DATA_FOLDER = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample'

#Tomer
#ROOT_DATA_FOLDER = 'C:\ML\parkinson\DATA'
#ROOT_DATA_FOLDER = 'C:\ML\parkinson\FIRSTDATA'

#Server
#ROOT_DATA_FOLDER = '/homes/jonathan.s/workspace/data/data_sample'
#ROOT_DATA_FOLDER = '/homes/jonathan.s/workspace/data/configuration_runs/1_feature_by_feature/'
ROOT_DATA_FOLDER = '/homes/jonathan.s/workspace/data/configuration_runs/2_time_windows_and_stat_features/'
#ROOT_DATA_FOLDER = '/homes/jonathan.s/workspace/data/configuration_runs/3_feature_selection/'
#ROOT_DATA_FOLDER = '/homes/jonathan.s/workspace/data/configuration_runs/4_scaling/'
#ROOT_DATA_FOLDER = '/homes/jonathan.s/workspace/data/configuration_runs/5_dimentionality_reduction_features/'
#ROOT_DATA_FOLDER = '/homes/jonathan.s/workspace/data/configuration_runs/6_variance_across_features/'
#ROOT_DATA_FOLDER = '/homes/jonathan.s/workspace/data/configuration_runs/7_cleanNoise/'
#ROOT_DATA_FOLDER = '/homes/jonathan.s/workspace/data/configuration_runs/8_committee/'
#ROOT_DATA_FOLDER = '/homes/jonathan.s/workspace/data/configuration_runs/9_clustering/'

UNIFIED_TABLES_FOLDER = os.path.join(ROOT_DATA_FOLDER, 'Unified Tables')

#comment below for configuration_runs/1_feature_by_feature
DATA_TABLE_FILE_PATH = os.path.join(UNIFIED_TABLES_FOLDER, 'unified_table.csv')

#uncomment below for configuration_runs/1_feature_by_feature
#DATA_TABLE_FILE_PATH = os.path.join(UNIFIED_TABLES_FOLDER, 'unified_data.csv')
#LABELS_FOR_DATA_TABLE_FILE_PATH = os.path.join(UNIFIED_TABLES_FOLDER, 'unified_labels.csv')

UNIFIED_ENTIRE_DATA_PATH = os.path.join(UNIFIED_TABLES_FOLDER, 'unified_entire.csv')
UNIFIED_AGGREGATED_DATA_PATH = os.path.join(UNIFIED_TABLES_FOLDER, 'unified_aggregated_subWindows.csv')

SCALED_UNIFIED_ENTIRE_DATA_PATH = os.path.join(UNIFIED_TABLES_FOLDER, 'scaled_unified_entire.csv')
SCALED_UNIFIED_AGGREGATED_DATA_PATH = os.path.join(UNIFIED_TABLES_FOLDER, 'scaled_unified_aggregated_subWindows.csv')

UNIFIED_ENTIRE_LABELS_FILENAME = 'unified_entire_labels.csv'
UNIFIED_AGGREGATED_LABELS_FILENAME = 'unified_aggregated_labels.csv'
UNIFIED_AGGREGATED_PATIENT_NAMES_FILENAME = 'unified_aggregated_names.csv'
UNIFIED_ENTIRE_LABELS_PATH = os.path.join(UNIFIED_TABLES_FOLDER ,UNIFIED_ENTIRE_LABELS_FILENAME)
UNIFIED_AGGREGATED_LABELS_PATH = os.path.join(UNIFIED_TABLES_FOLDER ,UNIFIED_AGGREGATED_LABELS_FILENAME)
UNIFIED_AGGREGATED_PATIENT_NAMES_PATH = os.path.join(UNIFIED_TABLES_FOLDER ,UNIFIED_AGGREGATED_PATIENT_NAMES_FILENAME)

RESULTS_FOLDER = os.path.join(ROOT_DATA_FOLDER,"results")

SVM_RES_ENTIRE_PATH = os.path.join(RESULTS_FOLDER, "svm_res_instance_per_entire_data.csv")
SVM_RES_WINDOWS_PATH = os.path.join(RESULTS_FOLDER, "svm_res_instance_per_aggregated_window.csv")
LOGISTIC_RES_ENTIRE_PATH = os.path.join(RESULTS_FOLDER, "logistic_res_instance_per_entire_data.csv")
LOGISTIC_RES_WINDOWS_PATH = os.path.join(RESULTS_FOLDER, "logistic_res_instance_per_aggregated_window.csv")
FOREST_RES_ENTIRE_PATH = os.path.join(RESULTS_FOLDER, "randForest_res_instance_per_entire_data.csv")
FOREST_RES_WINDOWS_PATH = os.path.join(RESULTS_FOLDER, "randForest_res_instance_per_aggregated_window.csv")
UNIFIED_RESULTS_PATH = os.path.join(RESULTS_FOLDER, "unified_prediction_results.csv")

FEATURE_SELECTION_LOGISTIC_RES_WINDOWS_PATH = os.path.join(RESULTS_FOLDER, "selected_features.csv")


NUMBER_OF_ENTIRE_FEATURES = 40 #TODO not correct
NUMBER_OF_FIVE_MINUTES_FEATURES = 40 #TODO not correct
NUMBER_OF_FOLDS = 2


entireFeatures = []
longWindowsFeatures = []

NUM_COEFFS = 5

FREQ_L = 0.0161267947405577 #Hz?
FREQ_H = 0.059893537312746

MAX_TIME_DIFF = 2 #seconds

delete = False


selectedFeatures1 = ['MFCC_12_max', 'PSD_250_max_average_on_windows', 'z_PSD_10_max', \
                        'MFCC_3_max_average_on_windows','y_max_deviation_max_average_on_windows', 'MFCC_7_max_average_on_windows']

selectedFeatures2 = ['MFCC_3_max_average_on_windows', 'x_PSD_6_max_average_on_windows', 'y_PSD_3_max', \
                        'z_PSD_6_max','PSD_500_max', 'PSD_250_max']

selectedFeatures3 = ['z_PSD_1_max_average_on_windows', 'MFCC_9_max_average_on_windows', 'MFCC_10_max', \
                        'MFCC_9_max','y_PSD_1_max_average_on_windows']

selectedFeaturesT = ['x_max_deviation_DCT_coeff_2', 'MFCC_6_DCT_coeff_3', 'y_PSD_10_DCT_coeff_3', 'MFCC_12_DCT_coeff_2', \
                            'x_PSD_10_DCT_coeff_4', 'z_PSD_1_DCT_coeff_1', 'MFCC_2_DCT_coeff_4']


selectedFeaturesAgg1 = ['MFCC_12_max', 'z_PSD_10_max', 'y_PSD_3_max', \
                        'z_PSD_6_max','PSD_500_max', 'PSD_250_max', 'MFCC_9_max', 'MFCC_10_max']


# GRIDSEARCH_RESOLUTION = 10 # number of values to check per parameter
GRIDSEARCH_RESOLUTION = 5 # number of values to check per parameter
# GRIDSEARCH_FOLDS = 4 # number of folds to base the gridSearch score on
GRIDSEARCH_FOLDS = 1 # number of folds to base the gridSearch score on





