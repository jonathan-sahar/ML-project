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


def gridSearch(X, y,pred, param_grid):
    '''
    :param base: what base to use with given exponents
    :return:
    '''
    cv = StratifiedShuffleSplit(y, n_iter=NUMBER_OF_FOLDS, test_size=1./NUMBER_OF_FOLDS, random_state=42)
    grid = GridSearchCV(pred, param_grid=param_grid, cv=cv, scoring=lossScorer)
    grid.fit(X, y)
    return grid



def DEPRICATED_optimzeSVM(X, y, c_low=-5, c_high=10, gamma_low=-10, gamma_high=5):
    '''

    :param X: data set to optimize on
    :param y: corresponding labels
    :param initial_low_C, initial_high_C, initial_low_gamma, initial_high_gamma: inittial grid borders given as **exponents** for base 10
    :return: a predictor created using optimal parameters, and trained on input data
    '''
    C_range = np.logspace(c_low, c_high, 10)
    gamma_range = np.logspace(gamma_low, gamma_high, 10)
    param_grid = dict(gamma=gamma_range, C=C_range)

    print 'searching grid (base {}):\nC: {}\ngamma: {}'.format(10, C_range, gamma_range)
    grid = gridSearch(X, y, param_grid)
    pred = grid.estimator
    bestParamsFromCoarseSearch = pred.get_params()
    print bestParamsFromCoarseSearch
    coarse_c = bestParamsFromCoarseSearch['C']
    coarse_gamma = bestParamsFromCoarseSearch['gamma']

    print("The best parameters (coarse) are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))
    plotGridSearch(grid, C_range, gamma_range)

    #get base-2 exponents, and define new grid limits
    margin = 2
    c_exp_base2 = np.rint(np.log2(coarse_c))
    gamma_exp_base2 = np.rint(np.log2(coarse_gamma))
    print 'c_exp_base2: ', c_exp_base2
    print 'gamma_exp_base2: ', gamma_exp_base2

    c_low = c_exp_base2 - margin
    c_high = c_exp_base2 + margin
    gamma_low = gamma_exp_base2 - margin
    gamma_high = gamma_exp_base2 + margin

    C_range = np.logspace(c_low, c_high, 10, base =2)
    gamma_range = np.logspace(gamma_low, gamma_high, 10, base =2)
    param_grid = dict(gamma=gamma_range, C=C_range)

    print 'searching grid (base {}):\nC: {}\ngamma: {}'.format(10, C_range, gamma_range)
    grid = gridSearch(X, y, param_grid)
    pred = grid.estimator
    bestParamsFromFineSearch = pred.get_params()
    fine_c = bestParamsFromFineSearch['C']
    fine_gamma = bestParamsFromFineSearch['gamma']

    print("The best parameters (fine) are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))
    plotGridSearch(grid, C_range, gamma_range)

    return pred


def optimizeHyperParams(X, y, predictorType):
    if predictorType == 'SVM':
        paramDict = {'C':{'min': -5, 'max':10},\
                     'gamma':{'min': -10, 'max':5}
        }
        pred = SVC()
        return  genericOptimzer(X,y,pred, paramDict)

    if predictorType == 'RF':
        return


def genericOptimzer(X, y, pred, paramDict):
    '''

    :param X: data
    :param y: labels
    :param paramDict: of structure:
                                    pDict = {'param_1':{'min': -5, 'max':1 for param, borders in params.items0}
                                             'param_2':{'min': -5, 'max':1 for param, borders in params.items0}
                                             .
                                             .
                                             .
                                    }
    :return: trained and tuned estimator
    '''
    parameters = paramDict.keys()
    param_grid = {param: np.logspace(borders['min'], borders['max']) for param, borders in paramDict.items()}

    print 'searching grid (base {}):\nparams: {}'.format(10,paramDict)
    grid = gridSearch(X, y, pred, param_grid)
    pred = grid.best_estimator_
    bestParamsFromCoarseSearch = pred.get_params()

    coarseParams = {param: bestParamsFromCoarseSearch[param] for param in parameters}
    print 'coarseParams:', coarseParams
    print("The best parameters (coarse) are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))
    # plotGridSearch(grid, C_range, gamma_range) #todo fixme

    #get base-2 exponents, and define new grid limits
    margin = 2
    exponentsInBase2 = {param: np.rint(np.log2(value)) for param, value in coarseParams.items() }

    newParamDict = {'param':\
                        {'min': coarseExponent - margin ,\
                         'max': coarseExponent + margin\
                            }
                    for param, coarseExponent in exponentsInBase2.items()}

    newParam_grid = {param: np.logspace(borders['min'], borders['max']) for param, borders in newParamDict.items()}
    print 'searching grid (base {}):\nparams: {}'.format(2, paramDict)
    grid = gridSearch(X, y, pred, newParam_grid)
    pred = grid.best_estimator_
    bestParamsFromFineSearch = pred.get_params()
    fineParams = {param: bestParamsFromCoarseSearch[param] for param in parameters}
    print("The best parameters (fine) are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))
    # plotGridSearch(grid, C_range, gamma_range)

    return pred