import visa
import time
import numpy as np
import matplotlib.pyplot as plt


try:
    a=time.time()
    # rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
    rm = visa.ResourceManager()
    # device_list = rm.list_resources()
    # print ("\nConnencted device list:\n", device_list)
    # print len(device_list)
    PSA = rm.open_resource('GPIB0::2::INSTR')
    PSA.timeout = 20000
    print PSA.query('*IDN?')
    PSA.write('*CLS')
    PSA.write('*RST')
    PSA.write('INSTRUMENT:SELECT SA')

    ####################
    PSA.write('TRACE1:MODE WRITE')
    PSA.write('SWEEP:TIME:AUTO ON')
    PSA.write('SWEEP:TIME:AUTO:RULES NORMAL')
    PSA.write('SWEEP:POINTS 1001')
    PSA.write('FORMAT:TRACE:DATA ASCII')
    PSA.write('FORMAT:BORDER NORMAL')
    ###################
    # when performing average function, the previous measurement
    # needs to be aborted, and then initiate:immediate
    # if the 'continuous' is OFF
    PSA.write('ABORT')
    PSA.write('INITIATE:CONTINUOUS ON')
    # PSA.write('*WAI')
    # PSA.write('INITIATE:IMMEDIATE')
    # setting measurement window
    PSA.write('FREQUENCY:CENTER 5 GHZ')
    PSA.write('FREQUENCY:SPAN 3E-2 GHZ')
    PSA.write('BANDWIDTH:RESOLUTION 100 KHZ')
    # # visualization
    PSA.write('DISPLAY:WINDOW:TRACE:Y:SCALE:PDIVISION 10 DB')
    PSA.write('DISPLAY:WINDOW:TRACE:Y:SCALE:RLEVEL 10 DBM')
    PSA.write('POWER:RF:ATTENUATION:AUTO ON')
    # detector mode
    # Normal is good for CW signal measurement
    PSA.write('DETECTOR:AUTO OFF')
    PSA.write('DETECTOR:FUNCTION NORMAL')
    # # average option
    # LOG type is good for looking for signals near noise
    # AUTO use the default method of LOG
    PSA.write('AVERAGE:STATE ON')
    PSA.write('AVERAGE:TYPE:AUTO ON')
    # PSA.write('AVERAGE:TYPE LOG')
    PSA.write('AVERAGE:COUNT 5')
    # # place markers
    PSA.write('CALCULATE:MARKER1:STATE ON')
    PSA.write('CALCULATE:MARKER1:MODE POSITION')
    PSA.write('CALCULATE:MARKER1:X 4.995 GHZ')
    PSA.write('CALCULATE:MARKER2:STATE OFF')
    PSA.write('CALCULATE:MARKER2:MODE POSITION')
    PSA.write('CALCULATE:MARKER2:X 5.005 GHZ')

    # PSA.write('CALCULATE:MARKER2:STATE OFF')
    PSA.write('CALCULATE:MARKER3:STATE OFF')
    PSA.write('CALCULATE:MARKER4:STATE OFF')
    marker1 = PSA.query('CALCULATE:MARKER1:Y?')
    marker2 = PSA.query('CALCULATE:MARKER2:Y?')
    # # functional markers
    # print PSA.query('CALCULATE:MARKER1:X:READOUT?')
    # PSA.write('CALCULATE:MARKER:TABLE:STATE OFF')
    # PSA.write('CALCULATE:MARKER:AOFF')
    # PSA.write('CALCULATE:MARKER1:FUNCTION OFF')
    #
    #
    # PSA.write('INITIATE:IMMEDIATE')
    print 'mark1:',marker1, marker2
    # PSA.write('INITIATE:CONTINUOUS OFF')
    # PSA.write('*CLS')
    save = PSA.query_ascii_values('TRACE? TRACE1',container= np.array)
    # PSA.write('*WAI')
    print len(save), save
    x=np.linspace(0,1001,1001)
    plt.figure()
    plt.plot(x,save)
    plt.show()
    plt.close()
    # PSA.write("MMEMORY:STORE:TRACE TRACE1,'C:\YANG3.CSV'")
    PSA.close()

    # time.sleep(3)

    print 'finished'




except Exception as err:
    print ('\nException', str(err.message))

finally:
    print ('\nEND')
