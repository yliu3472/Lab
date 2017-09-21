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
    MXG = rm.open_resource('GPIB0::1::INSTR')
    print MXG.query('*IDN?')
    MXG.write('*CLS')
    MXG.write('*RST')
    MXG.write('SOURCE:POWER:ALC:STATE ON')
    # Harmonics option does not work in this MXG
    # MXG.write('SOURCE:POWER:HARMONICS:STATE ON')
    # print MXG.query('SOURCE:POWER:HARMONICS?')
    MXG.write('SOURCE:FREQUENCY:MODE CW')
    MXG.write('SOURCE:FREQUENCY:CW 4.995GHZ')
    MXG.write('SOURCE:POWER:MODE FIXED')
    MXG.write('SOURCE:POWER -10')
    # Noise optimization is not working
    # print MXG.query('SOURCE:POWER:NOISE:STATE?')
    MXG.write('OUTPUT:STATE 1')
    print 'finished'
    MXG.close()
    # MXG.write('INITIATE:IMMEDIATE')


except Exception as err:
    print ('\nException', str(err.message))

finally:
    print ('\nEND')
