__author__ = 'Jonathan'
import numpy as np

from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import  make_scorer
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


from utils.constants import *

def loss(y, y_predicted):
    y = np.array(y)
    y_predicted = np.array(y_predicted)
    errors = np.sum(np.abs(y-y_predicted))
    return 1-1.*errors/len(y) #1-makes the loss "greater is better"

lossScorer = make_scorer(loss,greater_is_better=True)


class MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

def plotGridSearch(grid, C_range, gamma_range, gridName = 'grid1'):
    '''
    Draws heatmap of the validation accuracy as a function of gamma and C

    The score are encoded as colors with the hot colormap which varies from dark
    red to bright yellow. As the most interesting scores are all located in the
    0.92 to 0.97 range we use a custom normalizer to set the mid-point to 0.92 so
    as to make it easier to visualize the small variations of score values in the
    interesting range while not brutally collapsing all the low score values to
    the same color.
    '''

    scores = [x[1] for x in grid.grid_scores_]
    scores = np.array(scores).reshape(len(C_range), len(gamma_range))
    print "scores: ", scores


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
    plt.savefig(os.path.join(RESULTS_FOLDER,'{}.png'.format(gridName)))
    # plt.show()

def gridSearch(X, y, c_low, c_high, gamma_low, gamma_high, base = 10):
    '''
    :param base: what base to use with given exponents
    :return:
    '''
    C_range = np.logspace(c_low, c_high, 10, base)
    gamma_range = np.logspace(gamma_low, gamma_high, 10, base)

    print 'searching grid (base {}):\nC: {}\ngamma: {}'.format(base, C_range, gamma_range)
    param_grid = dict(gamma=gamma_range, C=C_range)
    cv = StratifiedShuffleSplit(y, n_iter=NUMBER_OF_FOLDS, test_size=1./NUMBER_OF_FOLDS, random_state=42)
    grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv, scoring=lossScorer)
    grid.fit(X, y)

    print("The best parameters are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))
    plotGridSearch(grid, C_range, gamma_range)
    return  grid.best_params_



def optimzeSVM(X, y, initial_low_C=-5, initial_high_C=10, initial_low_gamma=-10, initial_high_gamma=5):
    '''

    :param X: data set to optimize on
    :param y: corresponding labels
    :param initial_low_C, initial_high_C, initial_low_gamma, initial_high_gamma: inittial grid borders given as **exponents** for base 10
    :return: a predictor created using optimal parameters
    '''
    params = gridSearch(X, y, initial_low_C, initial_high_C, initial_low_gamma, initial_high_gamma)
    coarse_c = params['C']
    coarse_gamma = params['gamma']

    margin = 2

    c_exp_base2 = np.rint(np.log2(coarse_c))
    print 'c_exp_base2: ', c_exp_base2
    low_c_exp_base2 = c_exp_base2 - margin
    high_c_exp_base2 = c_exp_base2 + margin

    gamma_exp_base2 = np.rint(np.log2(coarse_gamma))
    print 'gamma_exp_base2: ', gamma_exp_base2
    low_gamma_exp_base2 = gamma_exp_base2 - margin
    high_gamma_exp_base2 = gamma_exp_base2 + margin

    params =  gridSearch(X, y, low_c_exp_base2, high_c_exp_base2, low_gamma_exp_base2, high_gamma_exp_base2, base = 2)
    fine_c = params['C']
    fine_gamma = params['gamma']

    return SVC(fine_c, 'rbf', gamma=fine_gamma)

def optimzeRandomForest():
    #TODO: implement
    return

def optimizeHyperParams(X, y, predictorType):
    if predictorType == 'SVM':
        return  optimzeSVM(X,y)
    if predictorType == 'RF':
        return  optimzeRandomForest(X,y)
