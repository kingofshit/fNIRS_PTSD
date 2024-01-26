import os
import mne
from mne.io import read_raw_nirx
from mne.preprocessing.nirs import (optical_density, beer_lambert_law,temporal_derivative_distribution_repair)

import matplotlib.pyplot as plt

# First we obtain the path to the data

# fpath = "D:\\fNIRS_Data\\zishu\\raw\\ptsd"
# fname = "通用_2023-06-12_14-27-30_Eprime_test1_女_2005-06-12_TEST.snirf"
fnirs_raw_dir = "D:\\fNIRS_Data\\zishu\\raw\\ptsd"
# fnirs_data_folder = mne.datasets.fnirs_motor.data_path()
# fnirs_raw_dir = os.path.join(fnirs_data_folder, 'Participant-1')

# Next we read the data
raw_intensity = read_raw_nirx(fnirs_raw_dir).load_data()

# Convert signal to optical density and apply TDDR
raw_od = optical_density(raw_intensity)
corrected_tddr = temporal_derivative_distribution_repair(raw_od)

# Convert to haemoglobin concentration
raw_h = beer_lambert_law(corrected_tddr, ppf=6.)
print(raw_h._data.shape)
x = raw_h.times
y1 = raw_h._data[2]
y2 = raw_h._data[3]
plt.plot(x,y1, x, y2)
plt.show()
print("OK")