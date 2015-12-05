__author__ = 'Jonathan'
import numpy as np

from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import  make_scorer
from sklearn.linear_model import LogisticRegressionCV
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import ticker
from sklearn.ensemble import RandomForestClassifier

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


runtime = {}
runtime['plot_num'] = 1

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

    # get the scores for all (c, gamma) pairs in a 2D grid.
    scores = [x[1] for x in grid.grid_scores_]
    scores = np.array(scores).reshape(len(gamma_range), len(C_range))

    # create the figure object, add a plotting area and adjust its size and locaation
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111)
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.2, top=0.95)

    # set a formatter to display all values as exponents - **currently doesn't work for some reason**
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))

    # get the mean of the top-5 pairs, for normalizing the colorbar
    top_values_mean = np.sort(scores)[:5].mean()
    # print "top_values_mean: ", top_values_mean

    # draw the image in the axes (ax) object + the colorbar
    cax = ax.imshow(scores, interpolation='nearest', cmap=plt.cm.hot,
               norm=MidpointNormalize(vmin=0.2, midpoint=top_values_mean))
    cbar = fig.colorbar(cax)

    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # set all the labels, titles, etc.
    ax.set_ylabel('C', alpha=0.6, fontsize=20)
    ax.set_yticks(np.arange(len(C_range)))
    ax.set_yticklabels(C_range, rotation=45)

    ax.set_xlabel('gamma', alpha=0.6, fontsize=20)
    ax.set_xticks(np.arange(len(gamma_range)))
    ax.set_xticklabels(gamma_range, rotation=45)

    plt.title('Hyperparameter scores')
    plt.savefig(os.path.join(RESULTS_FOLDER,'{}.png'.format(gridName)))
    # plt.show()

def gridSearch(X, y,pred, param_grid):
    '''
    :param base: what base to use with given exponents
    :return:
    '''
    print "got param_grid: {}".format(param_grid)
    cv = StratifiedShuffleSplit(y, n_iter=NUMBER_OF_FOLDS, test_size=1./NUMBER_OF_FOLDS, random_state=42)
    grid = GridSearchCV(pred, param_grid=param_grid, cv=cv, scoring=lossScorer)
    grid.fit(X, y)
    return grid


def genericOptimzer(X, y, pred, paramDict, gridType = 'logarithmic'):
    '''
    TODO: add parameter: a dict that holds ready lists of parameters for the grid, and append this dict to newParam_grid
    :param X: data
    :param y: labels
    :param paramDict: of structure:
                                    pDict = {
                                            'param_1':{
                                                        'min': -5,
                                                        'max': 1 
                                                        }
                                            'param_2':{
                                                        'min': -100,
                                                        'max':500
                                                        }
                                                .
                                                .
                                                .
                                    }
    :param gridType: one of {'logarithmic', 'equidistance'}, sets the way we 
                                distribute values of params in the given range.
                                All ranges are distributed in the same way.
    :return: trained and tuned estimator
    '''
    plot_num = runtime['plot_num']
    parameters = paramDict.keys()
    assert  gridType == 'logarithmic' or gridType == 'equidistance'
    if gridType == 'logarithmic':
        param_grid = {param: np.logspace(borders['min'], borders['max'], num=GRIDSEARCH_RESOLUTION) for param, borders in paramDict.items()}
    elif gridType == 'equidistance':
        param_grid = {param: list(np.unique(np.rint(np.linspace(borders['min'], borders['max'], num=GRIDSEARCH_RESOLUTION))).astype(int)) for param, borders in paramDict.items()}
        print '[genericOptimzer] passing on equidistance grid'
    print '[genericOptimzer] searching grid (coarse):\nparams: {}\nparam_grid: {}'.format(paramDict, param_grid)
    grid = gridSearch(X, y, pred, param_grid)
    pred = grid.best_estimator_
    bestParamsFromCoarseSearch = pred.get_params()

    bestCoarseParams = {param: bestParamsFromCoarseSearch[param] for param in parameters}
    print("[genericOptimzer] The best parameters (coarse) are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))

    # C_range = param_grid['C']
    # gamma_range = param_grid['gamma']
    # print "[genericOptimzer] saving coarse grid to file..."
    # plotGridSearch(grid, C_range, gamma_range, 'coarse_grid_{}'.format(plot_num))

    if gridType == 'logarithmic':
        margin = 1
        #get base-2 exponents, and define new grid limits
        exponents = {param: np.floor(np.log10(value)) for param, value in bestCoarseParams.items() }
    
        newParamDict = {param: \
                            {'min': coarseExponent, \
                             'max': coarseExponent + margin \
                                }
                        for param, coarseExponent in exponents.items()}
    elif gridType == 'equidistance':
        margin = 10
        newParamDict = {param: \
                            {'min': val - margin, \
                             'max': val + margin\
                                }
                        for param,  val in exponents.items()}

    if gridType == 'logarithmic':
       newParam_grid = {param: np.logspace(borders['min'], borders['max'], num=GRIDSEARCH_RESOLUTION)\
                                                                for param, borders in newParamDict.items()}
    elif gridType == 'equidistance':
        newParam_grid = {param: np.unique(np.rint(np.linspace(borders['min'], borders['max'], num=GRIDSEARCH_RESOLUTION))).astype(int)\
                                                                for param, borders in newParamDict.items()}
    print '[genericOptimzer] searching grid (fine):\nparams: {}\nparam_grid: {}'.format(paramDict, param_grid)
    grid = gridSearch(X, y, pred, newParam_grid)
    pred = grid.best_estimator_
    bestParamsFromFineSearch = pred.get_params()
    fineParams = {param: bestParamsFromCoarseSearch[param] for param in parameters}
    print("[genericOptimzer] The best parameters (fine) are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))

    # C_range = newParam_grid['C']
    # gamma_range = newParam_grid['gamma']
    # print "[genericOptimzer] saving fine grid to file..."
    # plotGridSearch(grid, C_range, gamma_range, 'fine_grid_{}'.format(plot_num))
    # runtime['plot_num'] += 1

    return pred


def optimizeHyperParams(X, y, predictorType):
    '''

    :param X: list of lists, same as predictor.fit() expects to get.
    :param y:
    :param predictorType:
    :return:
    '''
    if predictorType == 'SVM':
        # paramDict = {'C':{'min': -5, 'max':10},\
        #              'gamma':{'min': -10, 'max':5}
        # }
        paramDict = {'C':{'min': -3, 'max':5},\
                     'gamma':{'min': -5, 'max':3}
        }
        pred = SVC()
        return  genericOptimzer(X,y,pred, paramDict)

    if predictorType == 'RF':
        n_features = len(X[0])
        pred = RandomForestClassifier()
        paramDict = {
              #'n_estimators': {'min': 40, 'max': 650},\
              #'max_features': {'min': 1, 'max': 20}}
              n_estimators': {'min': 20, 'max': 90},\
              max_features': {'min': 6, 'max': n_features - 20}}
              #"max_depth": [3, None],
              #"bootstrap": [True, False],
              #"criterion": ["gini", "entropy"]}
        return genericOptimzer(X,y,pred, paramDict, gridType='equidistance')
    if predictorType == 'logisticReg':
        return LogisticRegressionCV(Cs=10).fit(X,y)




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

def DEPRICATED_optimzeRandomForest(data, labels):
    '''
    param data: data set to optimize on
    param labels: corresponding labels
    param initial_low_C, initial_high_C, initial_low_gamma, initial_high_gamma: inittial grid borders given as **exponents** for base 10
    return: a predictor created using optimal parameters
    '''
    estimator = RandomForestClassifier()
    param_grid = {
              "n_estimators": [10,50,100],
              "max_depth": [3, None],
              "max_features": [1, 3, 10],
              "min_samples_split": [1, 3, 10],
              "min_samples_leaf": [1, 3, 10],
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}

    clf = GridSearchCV(estimator, param_grid)
    #start = time()
    clf.fit(data, labels)
    return clf

def DEPRICATED_genericOptimzer(X, y, pred, paramDict):
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
    param_grid = {param: np.logspace(borders['min'], borders['max'], num=GRIDSEARCH_RESOLUTION) for param, borders in paramDict.items()}

    print 'searching grid (base {}):\nparams: {}'.format(10,paramDict)
    grid = gridSearch(X, y, pred, param_grid)
    pred = grid.best_estimator_
    bestParamsFromCoarseSearch = pred.get_params()

    coarseParams = {param: bestParamsFromCoarseSearch[param] for param in parameters}
    print("The best parameters (coarse) are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))

    C_range = param_grid['C']
    gamma_range = param_grid['gamma']
    plotGridSearch(grid, C_range, gamma_range, 'coarse_grid')

    #get base-2 exponents, and define new grid limits
    margin = 2
    exponentsInBase2 = {param: np.rint(np.log2(value)) for param, value in coarseParams.items() }

    newParamDict = {param:\
                        {'min': coarseExponent - margin ,\
                         'max': coarseExponent + margin\
                            }
                    for param, coarseExponent in exponentsInBase2.items()}

    newParam_grid = {param: np.logspace(borders['min'], borders['max'], num=GRIDSEARCH_RESOLUTION) for param, borders in newParamDict.items()}
    print 'searching grid (base {}):\nparams: {}'.format(2, newParamDict)
    grid = gridSearch(X, y, pred, newParam_grid)
    pred = grid.best_estimator_
    bestParamsFromFineSearch = pred.get_params()
    fineParams = {param: bestParamsFromCoarseSearch[param] for param in parameters}
    print("The best parameters (fine) are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))

    C_range = param_grid['C']
    gamma_range = param_grid['gamma']
    plotGridSearch(grid, C_range, gamma_range, 'fine_grid')
    return pred

