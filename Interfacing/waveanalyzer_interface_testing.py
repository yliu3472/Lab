import requests
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.backends.backend_pdf import PdfPages


# ok try my own averaging
averages = 8

now = time.time()
# run one measurement to initiliase an array for grabbing more on top, determine length etc,
m = requests.get('http://192.168.2.8/wanl/data/json')
data_array = np.array(m.json()['data'])
grab_power = data_array[:, 1]/1e3

power_length = len(grab_power)
# make an empty set of arrays for casting in the loop
record = np.empty((averages, power_length))

for steps in xrange(averages):
    m = requests.get('http://192.168.2.8/wanl/data/json')
    # loop_data_array = np.array(m.json()['data'])
    # loop_grab_power = loop_data_array[:, 3]/1e3
    # 2nd column is absolute power data

    record[steps] = np.array(m.json()['data'])[:, 1]/1e3

after = time.time()

freq = data_array[:, 0]/1e6
power = data_array[:, 1]/1e3

cut_left = int(len(freq)*0.4)
cut_right = int(len(freq)*0.6)

print "took so long:", after - now
# print record

# do the mean over the recorded arrays
averaged = record.mean(axis=0)

# plotting
pp = PdfPages("testing_thing_osa_fun" + ".pdf")
plt.figure()
plt.clf()

# plt.plot(freq, power)
plt.plot(freq, averaged)
# plt.axis([freq[cut_left], freq[cut_right], -70, np.max(power)*0.95])
plt.show()
# pp.savefig(bbox_inches='tight', pad_inches=0.04)
# pp.close()

# this all works great, but the issue is that the output data is completely raw and does not include
# the processing to achieve the 150MHz spectral bandwidth
