__author__ = 'Jonathan'
from   utils.utils import *
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.svm import SVC
import itertools
import operator
from optimize import optimizeHyperParams
from sklearn.cross_validation import LeavePLabelOut
from predict import lossFunction

NUM_CLUSTERS = 50

def tuneAndTrainForClustering(predictorType, data, labels, patientIds, numFolds, lossFunction = lossFunction):
    '''
    :param data: data matrix, a structured array.
    :param predictorType: one of: {'SVM', 'RF'}
    :param patientIds: May be ints, strings, etc. denoting which patient every line is taken from.
    :return: the mean error of an optimized predictor of type predictorType, and the optimized, trained predictor.
    '''
    folds = LeavePLabelOut(patientIds, p=2) #
    errors = []
    folds = [tup for tup in folds]
    for trainIndices, testIndices in folds[:numFolds]:
        #Tuning
        #get actual data and labels for current fold
        trainData = data[trainIndices]
        trainLabels = labels[trainIndices]
        trainNames = patientIds[trainIndices]
        testData = data[testIndices]
        testLabels = labels[testIndices]
        testNames = patientIds[testIndices]
        if np.all(trainLabels == trainLabels[0]):
            continue #can't train on elements that are all from the same group

        # todo: for testing - skip feature selection
        # selectedFeatures = SelectFeatures(trainData, trainLabels)
        # selectedTrainData = [trainData[f] for f in selectedFeatures]
        # selectedTestData = [testData[f] for f in selectedFeatures]

        # todo: for testing clustering
        selectedTrainData, trainLabels, scaler, km = createClusterFeatures(trainData, trainLabels, trainNames)
        selectedTestData, testlabels, _s, _K = createClusterFeatures(testData, testLabels, testNames, scaler = scaler, km=km)

        # to get the data in a list-of-list format that optimizeHyperParams expects.
        selectedTrainData = [list(tup) for tup in selectedTrainData]
        selectedTestData = [list(tup) for tup in selectedTestData]

        predictor = optimizeHyperParams(selectedTrainData, trainLabels, predictorType)

        #Training
        #predictor.fit(selectedFeaturesTrainData, trainLabels)

        #Testing
        errors.append(lossFunction(predictor, selectedTestData, testLabels))
    return np.array(errors).mean()

def createClusterFeatures(X, y, patientNames, scaler = None, km=None):
    '''

    :param X: data
    :param y: labels
    :param patientNames: names
    :param scaler: standartScaler object fitted on other data - to be used when creating features for test data
    :param km: KMeans object fitted on other data - to be used when creating features for test data
    :return: a structured array, a line per every patient, with features being the number of windows taken from that patient that belong to every cluster.
             (every cluster is a separate feature)
    '''
    X = castStructuredArrayToRegular(X)
    if km != None:
        X = scaler.transform(X)
        labels = km.predict(X)
    else:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        km = KMeans(n_clusters=NUM_CLUSTERS)
        km.fit(X)

        labels = km.labels_

    # the following block creates a list of tuples:
    #       tup[0] is the patient name
    #       tup[1] is a list of the cluster labels associated with all the time windows belonging to that patient
    sortedLabels = sorted(zip(patientNames, labels), key=operator.itemgetter(0))
    patientLabels = []
    for patient,group in itertools.groupby(sortedLabels,operator.itemgetter(0)):
        # keys are patient names, values are arrays of labels of windows that came from that patient.
        l = list(item[1] for item in group)
        patientLabels.append((patient,l))

    # the following block creates a list of tuples:
    #       tup[0] is the patient name
    #       tup[1] is the list of feature values (feature-i = how many windows belong to the i-th cluster)
    # using NUM_CLUSTERS+1 because the last bin in the histogram includes both edges.
    patientFeatures = [(patient, np.histogram(labels, range(NUM_CLUSTERS+1))[0]) for patient, labels in patientLabels]
    patientFeatures = sorted(patientFeatures, key=operator.itemgetter(0))


    # the following block creates arrays from the previous list of tuples
    newNames = np.array([tup[0] for tup in patientFeatures])
    newData = np.array([tup[1] for tup in patientFeatures])
    newLabels = np.array([int(tup[0] in SICK_PATIENTS) for tup in patientFeatures])
    print newData

    # the following block creates the final structured array
    header = ['cluster_{}'.format(i) for i in range(NUM_CLUSTERS)]
    dt = zip(header, len(header)*['f4']) # TODO: set the field type in a constant. are 4 bytes enough?
    rows = [tuple(row) for row in newData]
    assert len(rows[0]) == len(dt), 'number of fields does not match number of values in row!'
    newData = np.array(rows, dtype=dt)

    return  newData, newLabels, scaler, km

# Testing
X, y, patientNames = getRandomSample(30)
res = tuneAndTrainForClustering('SVM', X, y, patientNames, NUMBER_OF_FOLDS)
print "average success rate : ", res

def oldCode():
    r = re.compile(r'(.*_PSD_.*_mean)')
    psd_fields = filter_fields_by_name(np.array(X.dtype.names), r)
    X = X[psd_fields]


    X = castStructuredArrayToRegular(X)
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    # Compute KMeans
    NUM_CLUSTERS = 3
    km = KMeans(n_clusters=NUM_CLUSTERS)
    km.fit(X)
    labels = km.labels_

    patientLabels = []
    sortedLabels = sorted(zip(patientNames, labels), key=operator.itemgetter(0))
    for patient,group in itertools.groupby(sortedLabels,operator.itemgetter(0)):
        # keys are patient names, values are arrays of labels of windows that came from that patient.
        l = list(item[1] for item in group)
        patientLabels.append((patient,l))
        # use NUM_CLUSTERS+1 because the last bin in the histogram includes both edges.
    patientFeatures = [(patient, np.histogram(labels, range(NUM_CLUSTERS+1))[0]) for patient, labels in patientLabels]
    patientFeatures = sorted(patientFeatures, key=operator.itemgetter(0))
    newNames = np.array([tup[0] for tup in patientFeatures])
    newData = np.array([tup[1] for tup in patientFeatures])
    newLabels = np.array([int(tup[0] in SICK_PATIENTS) for tup in patientFeatures])
    print newData

    header = ['cluster_{}'.format(i) for i in range(NUM_CLUSTERS)]
    dt = zip(header, len(header)*['f4']) # TODO: set the field type in a constant. are 4 bytes enough?
    rows = [tuple(row) for row in newData]
    assert len(rows[0]) == len(dt), 'number of fields does not match number of values in row!'
    newData = np.array(rows, dtype=dt)

    res = tuneAndTrainForClustering('SVM', newData, newLabels, newNames, NUMBER_OF_FOLDS)
    print res