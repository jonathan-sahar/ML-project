__author__ = 'Jonathan'

from dataManipulation.DataArrange import arrangeData
from dataManipulation.createFeatureCSVs import createFeatures
from utils.constants import *
from dataManipulation.splitToPatients import splitToPatients
from optimizationAndPrediction.predict import predict
from utils.utils import *
from scale import scaleData
from optimizationAndPrediction.visualization import visualFeatures
from dataManipulation.NoiseClean import cleanNoise

# orig_data_folder = '/homes/jonathan.s/workspace/data/data_sample_orig'
# testing_data_folder = '/homes/jonathan.s/workspace/data/data_sample'

#orig_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample_orig'
#testing_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample'

#orig_data_folder = 'C:\ML\parkinson\DATA bckp'
#testing_data_folder = 'C:\ML\parkinson\DATA'

orig_data_folder = 'C:\ML\parkinson\FIRSTDATA - Copy'
testing_data_folder = 'C:\ML\parkinson\FIRSTDATA'
#testing_data_folder = 'C:\ML\parkinson\DATA'

print "here we go!"

# print "restoring data from orig..."
# restore_data(orig_data_folder, testing_data_folder)
# print "data restored from orig!"

#print "arranging data..."
#arrangeData()
#print "data arranged done!"
#
#
#print "splitting data into patient files..."
#splitToPatients()
#print "data split done!"

#print "cleaning noise in data..."
#cleanNoise()
#print "data cleaned of noise done!"
#

#print "creating features..."
#createFeatures()
#print "features created done!"

# print "scaling data..."
# scaleData()
# print "data scaled done!"

print "creating and testing predictors..."
predict()
print "predictors where tested done!"

# print "visualizing features results..."
# visualFeatures()
# print "top features visualized!"

print "all done!"
