__author__ = 'Jonathan'

LONG_TIME_WINDOW = 300
SHORT_TIME_WINDOW = 5
ENTROPY_RADIUS = 5

DFA_WINDOW_LEN = 10 # no. of lines

CONTROL = ['APPLE', 'DAFODIL', 'LILLY', 'LILY', 'ORANGE', 'ROSE', 'SUNFLOWER', 'SWEETPEA']
PATIENTS = [''' TODO sick dudes '''].concatanate(CONTROL)
UNDERLINES_BEFORE_NAME = 2
DATA_LEN = 1000000000

DATA_TABLE_FILE_PATH = 'C:\ML\parkinson\FAKEDATA'
SHORT_TABLE_FILE_PATH = 'C:\ML\parkinson\FAKEDATA'
LONG_TABLE_FILE_PATH = 'C:\ML\parkinson\FAKEDATA'
ENTIRE_TABLE_FILE_PATH = 'C:\ML\parkinson\FAKEDATA'

delete = False

accl = ["diffSecs",
  "N.samples",
  "x.mean",
  "x.absolute.deviation",
  "x.standard.deviation",
  "x.max.deviation",
  "x.PSD.1",
  "x.PSD.3",
  "x.PSD.6",
  "x.PSD.10",
  "y.mean",
  "y.absolute.deviation",
  "y.standard.deviation",
  "y.max.deviation",
  "y.PSD.1",
  "y.PSD.3",
  "y.PSD.6",
  "y.PSD.10",
  "z.mean",
  "z.absolute.deviation",
  "z.standard.deviation",
  "z.max.deviation",
  "z.PSD.1",
  "z.PSD.3",
  "z.PSD.6",
  "z.PSD.10",
  "time",

"Is sick"]

audio = ["diffSecs",
  "absolute.deviation",
  "standard.deviation",
  "max.deviation",
  "PSD.250",
  "PSD.500",
  "PSD.1000",
  "PSD.2000",
  "MFCC.1",
  "MFCC.2",
  "MFCC.3",
  "MFCC.4",
  "MFCC.5",
  "MFCC.6",
  "MFCC.7",
  "MFCC.8",
  "MFCC.9",
  "MFCC.10",
  "MFCC.11",
  "MFCC.12",
  "time",
  "Is sick"]

i = 0
accl_fields = {}
for s in accl:
    accl_fields[s] = i
    i += 1
audio_fields = {}
i=0
for s in audio:
    audio_fields[s] = i
    i += 1
