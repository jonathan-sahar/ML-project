
accl = [
  "diffSecs",
  "N_samples",
  "x_mean",
  "x_absolute_deviation",
  "x_standard_deviation",
  "x_max_deviation",
  "x_PSD_1",
  "x_PSD_3",
  "x_PSD_6",
  "x_PSD_10",
  "y_mean",
  "y_absolute_deviation",
  "y_standard_deviation",
  "y_max_deviation",
  "y_PSD_1",
  "y_PSD_3",
  "y_PSD_6",
  "y_PSD_10",
  "z_mean",
  "z_absolute_deviation",
  "z_standard_deviation",
  "z_max_deviation",
  "z_PSD_1",
  "z_PSD_3",
  "z_PSD_6",
  "z_PSD_10",
  "time",
  "Is_sick"
]

audio = [
  "diffSecs",
  "absolute_deviation",
  "standard_deviation",
  "max_deviation",
  "PSD_250",
  "PSD_500",
  "PSD_1000",
  "PSD_2000",
  "MFCC_1",
  "MFCC_2",
  "MFCC_3",
  "MFCC_4",
  "MFCC_5",
  "MFCC_6",
  "MFCC_7",
  "MFCC_8",
  "MFCC_9",
  "MFCC_10",
  "MFCC_11",
  "MFCC_12",
  "time",
  "Is_sick"
]

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

psd_D = {
    "low": 1,
    "med": 3,
    "high":6
}
