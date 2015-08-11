__author__ = 'Jonathan'
from DataArrange import arrangeData
from createFeatureCSVs import createFeatures
from utils.constants import *
from splitToPatients import splitToPatients
from predict import predict
from utils.utils import *
from scale import scaleData
from visualization import visualFeatures


# orig_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\EXTRACTED MJFF Partial Data - orig'
# testing_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\EXTRACTED MJFF Partial Data'

#orig_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample_orig'
#testing_data_folder = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample'

#orig_data_folder = 'C:\ML\parkinson\DATA bckp'
#testing_data_folder = 'C:\ML\parkinson\DATA'

orig_data_folder = 'C:\ML\parkinson\SECONDDATA - Copy'
testing_data_folder = 'C:\ML\parkinson\SECONDDATA'


print "here we go!"

restore_data(orig_data_folder, testing_data_folder)
print "data restored from orig!"

arrangeData()
print "data arranged!"

splitToPatients()
print "data split into patient files!"

createFeatures()
print "features created!"

scaleData()
print "data scaled!"

predict()
print "predictors where tested!"

visualFeatures()
print "top features visualized!"

print "all done!"
