import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from modified_sklearn.svm import SVC
from modified_sklearn.preprocessing import StandardScaler
from modified_sklearn.cross_validation import StratifiedShuffleSplit
from modified_sklearn.grid_search import GridSearchCV
from modified_sklearn.metrics import  make_scorer

from utils.constants import *
from utils.utils import readFileToFloat, castStructuredArrayToRegular

# Utility function to move the midpoint of a colormap to be around
# the values of interest.

class MidpointNormalize(Normalize):

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

##############################################################################
# Load and prepare data set
#
# dataset for grid search

X = readFileToFloat(UNIFIED_AGGREGATED_DATA_PATH)
X = castStructuredArrayToRegular(X)


y = readFileToFloat(UNIFIED_AGGREGATED_LABELS_PATH, names = None)

# idxs = np.random.randint(len(X), size = len(X)/1)
# X = X[idxs]
# y = y[idxs]

# It is usually a good idea to scale the data for SVM training.
# We are cheating a bit in this example in scaling all of the data,
# instead of fitting the transformation on the training set and
# just applying it on the test set.

scaler = StandardScaler()
X = scaler.fit_transform(X)

##############################################################################
# Train classifiers
#
# For an initial search, a logarithmic grid with basis
# 10 is often helpful. Using a basis of 2, a finer
# tuning can be achieved but at a much higher cost.

def loss(y, y_predicted):
    y = np.array(y)
    y_predicted = np.array(y_predicted)
    errors = np.sum(np.abs(y-y_predicted))
    # return 1.*errors/len(y)
    return 1-1.*errors/len(y)

lossScorer = make_scorer(loss,greater_is_better=True)



C_range = np.logspace(1, 10, 10)
gamma_range = np.logspace(-10, -6, 5, base=2)
param_grid = dict(gamma=gamma_range, C=C_range)
cv = StratifiedShuffleSplit(y, n_iter=8, test_size=1./8, random_state=42)
grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv, scoring=lossScorer)
grid.fit(X, y)

print("The best parameters are %s with a score of %0.2f"
      % (grid.best_params_, grid.best_score_))


##############################################################################
# visualization
#
# draw visualization of parameter effects


# plot the scores of the grid
# grid_scores_ contains parameter settings and scores
# We extract just the scores
scores = [x[1] for x in grid.grid_scores_]
scores = np.array(scores).reshape(len(C_range), len(gamma_range))
print "scores: ", scores

# Draw heatmap of the validation accuracy as a function of gamma and C
#
# The score are encoded as colors with the hot colormap which varies from dark
# red to bright yellow. As the most interesting scores are all located in the
# 0.92 to 0.97 range we use a custom normalizer to set the mid-point to 0.92 so
# as to make it easier to visualize the small variations of score values in the
# interesting range while not brutally collapsing all the low score values to
# the same color.

plt.figure(figsize=(8, 6))
plt.subplots_adjust(left=.2, right=0.95, bottom=0.15, top=0.95)

top_values_mean = np.sort(scores)[:5].mean()
print "top_values_mean: ", top_values_mean
plt.imshow(scores, interpolation='nearest', cmap=plt.cm.hot,
           norm=MidpointNormalize(vmin=0.2, midpoint=top_values_mean))
plt.xlabel('gamma')
plt.ylabel('C')
plt.colorbar()
plt.xticks(np.arange(len(gamma_range)), gamma_range, rotation=45)
plt.yticks(np.arange(len(C_range)), C_range)
plt.title('Hyperparameter scores')
plt.savefig(os.path.join(RESULTS_FOLDER,'fine_grid.png'))
plt.show()
