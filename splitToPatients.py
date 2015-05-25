__author__ = 'Inspiron'

import csv
from constants import *


if __name__ == "__main__":
    allLines = []
    dataFile = open(DATA_TABLE_FILE_PATH, 'r')
    reader = csv.reader(dataFile)
    for row in reader:
    #for row in open(DATA_TABLE_FILE_PATH, 'r').readlines():
        allLines.append(row)

    for patient in PATIENTS:
        patientLines = [['diffSecs','N.samples','x.mean','x.absolute.deviation','x.standard.deviation','x.max.deviation','x.PSD.1','x.PSD.3','x.PSD.6','x.PSD.10','y.mean','y.absolute.deviation','y.standard.deviation','y.max.deviation','y.PSD.1','y.PSD.3','y.PSD.6','y.PSD.10','z.mean','z.absolute.deviation','z.standard.deviation','z.max.deviation','z.PSD.1','z.PSD.3','z.PSD.6','z.PSD.10','time','diffSecs','absolute.deviation','standard.deviation','max.deviation','PSD.250','PSD.500','PSD.1000','PSD.2000','MFCC.1','MFCC.2','MFCC.3','MFCC.4','MFCC.5','MFCC.6','MFCC.7','MFCC.8','MFCC.9','MFCC.10','MFCC.11','MFCC.12','time','Is sick','Patient']]
        shortAggregatedFile = open(DATA_TABLE_FILE_PATH[:-4]+'_'+patient+'.csv', 'w')
        #print DATA_TABLE_FILE_PATH[-4:]+'_'+patient+'.csv'
        for line in allLines:
            #print line[28]
            if line[28] == patient: #TODO magic number :(
                patientLines.append(line)
        writer = csv.writer(shortAggregatedFile, lineterminator='\n') #TODO why would dataTable have \n in the end (also other places)
        writer.writerows(patientLines)
        shortAggregatedFile.close()

    dataFile.close()