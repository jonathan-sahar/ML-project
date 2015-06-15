__author__ = 'Inspiron'

from utils.utils import *
from utils.constants import *
import matplotlib.pyplot as plt
import numpy as np


def fuck():
    #healthIdxs = [i for i,x in enumerate(labelsData) if x == '0.0']
    #sickIdxs =[i for i,x in enumerate(labelsData) if x == '1.0']

    #for feature in selectedFeatures:


    #print visualData[healthIdxs]
    #putting healthy patients before sick
    #print [np.array((np.array(visualData).T)[index] for index in healthIdxs).T]
    #visualData = ([((np.array(visualData).T)[index] for index in healthIdxs).T] + ((np.array(visualData).T)[sickIdxs]).T)
    #[a[index] for index in b]
    '''
    for feature in selectedFeatures:
        # Plot calibration plots
        #fig.patch.set_alpha(0.5)
        ax1 = fig.add_subplot(111)
        #ax.patch.set_alpha(0.5)
        #ax1.plot(range(0, len(plottingData1)), plottingData1, lw=2, alpha=0.5)
        ax1.plot(range(0, len(visualData[feature])), visualData[feature], 'o', lw=3, alpha=0.5)
        ax1.set_xlabel('instance')
        ax1.set_ylabel('value')
    '''
    return 0


def createOnlyBestColumns(SCALED_DATA_PATH):

    entireData = readFileToFloat(SCALED_DATA_PATH)
    #entireData = readFileToFloat('C:\ML\parkinson\orEstimation\scaled_unified_entire.csv')

    data = []
    for feature in selectedFeatures:
       data.append(entireData[feature])
    return data

def visualization(visualData, labeledData):
    '''len of data is num of instances - X axis - the number of the instance
    0-1 is the values range - Y axis - the value of the feature
    every column is a graph'''

    labelsData = readFileAsIs(labeledData)
    #labelsData = readFileAsIs('C:\ML\parkinson\orEstimation\unified_entire_labels.csv')
    labelsData = labelsData[0]

    data = zip(np.array(visualData).T,labelsData)
    #print data
    data = sorted(data, key=lambda patient: patient[1])
    #print data

    plotData = []
    for patient,label in data:
        plotData.append(patient)
    plotData = np.array(plotData).T
    #print plotData

    plottingData1 = plotData[0]
    plottingData2 = plotData[1]
    plottingData3 = plotData[2]
    plottingData4 = plotData[3]
    plottingData5 = plotData[4]

    fig = plt.figure()
    #fig.patch.set_alpha(0.5)
    ax1 = fig.add_subplot(111)
    ax2 = fig.add_subplot(111)
    ax3 = fig.add_subplot(111)
    ax4 = fig.add_subplot(111)
    ax5 = fig.add_subplot(111)

    ax1.set_xlabel('instance')
    ax1.set_ylabel('value')
    plt.title('                       healthy', loc = 'left')
    plt.title('sick                                      ', loc = 'right')

    ax1.set_xticks(range(0, len(plottingData1)), minor=False)
    ax1.set_xticks(np.concatenate([np.arange(0.5, 15.5, 1.0), np.arange(6.4, 6.6, 0.01)]), minor=True)
    #ax1.xaxis.grid(True, which='major')
    ax1.xaxis.grid(True, which='minor')
    #ax1.xaxis.grid()

    ax1.plot(range(0, len(plottingData1)), plottingData1,'o', lw=3, label = selectedFeatures[0], alpha=0.5)
    ax2.plot(range(0, len(plottingData2)), plottingData2,'o', lw=3, label = selectedFeatures[1], alpha=0.5)
    ax3.plot(range(0, len(plottingData3)), plottingData3,'o', lw=3, label = selectedFeatures[2], alpha=0.5)
    ax4.plot(range(0, len(plottingData2)), plottingData4,'o', lw=3, label = selectedFeatures[3], alpha=0.5)
    ax5.plot(range(0, len(plottingData3)), plottingData5,'o', lw=6, label = selectedFeatures[4], alpha=0.5)

    xticks, xticklabels = plt.xticks()
    xmin = (3*xticks[0] - xticks[1])/2.
    # shaft half a step to the right
    xmax = (3*xticks[-1] - xticks[-2])/2.
    plt.xlim(xmin, xmax)
    yticks, yticklabels = plt.yticks()
    ymin = (3*yticks[0] - yticks[1])/2.
    # shaft half a step to the right
    ymax = (3*yticks[-1] - yticks[-2])/2.
    plt.ylim(ymin, ymax)

    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    box = ax3.get_position()
    ax3.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    box = ax4.get_position()
    ax4.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    box = ax5.get_position()
    ax5.set_position([box.x0, box.y0, box.width * 0.8, box.height])


    # Put a legend to the right of the current axis
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER,'visualization1.png'))

def visualFeatures():
    visualData = createOnlyBestColumns(SCALED_UNIFIED_ENTIRE_DATA_PATH)
    visualization(visualData, UNIFIED_ENTIRE_LABELS_PATH)
    #visualData = createOnlyBestColumns(SCALED_UNIFIED_AGGREGATED_DATA_PATH)
    #visualization(visualData, UNIFIED_AGGREGATED_LABELS_FILENAME)

if __name__=='__main__':
    visualFeatures()
