__author__ = 'Jonathan'

from dataManipulation.DataArrange import arrangeData
from dataManipulation.createFeatureCSVs import createFeatures
from utils.constants import *
from dataManipulation.splitToPatients import splitToPatients
from optimizationAndPrediction.predict import predict
from utils.utils import *
from scale import scaleData
from optimizationAndPrediction.visualization import visualFeatures

# orig_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\EXTRACTED MJFF Partial Data - orig'
# testing_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\EXTRACTED MJFF Partial Data'

#orig_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample_orig'
#testing_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample'

#orig_data_folder = 'C:\ML\parkinson\DATA bckp'
#testing_data_folder = 'C:\ML\parkinson\DATA'

orig_data_folder = 'C:\ML\parkinson\FIRSTDATA - Copy'
testing_data_folder = 'C:\ML\parkinson\FIRSTDATA'


print "here we go!"

# restore_data(orig_data_folder, testing_data_folder)
# print "data restored from orig!"

# print "arranging data..."
# arrangeData()
# print "data arranged!"

# print "splitting data into patient files..."
# splitToPatients()
# print "data split! done"

print "creating features..."
createFeatures()
print "features created!"

# print "scaling data..."
# scaleData()
# print "data scaled!"

# predict()
# print "predictors where tested!"
#
# visualFeatures()
# print "top features visualized!"

print "all done!"
