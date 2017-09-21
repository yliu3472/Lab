import visa
import time
import numpy as np
import matplotlib.pyplot as plt


try:
    a=time.time()
    # rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
    rm = visa.ResourceManager()
    device_list = rm.list_resources()
    print ("\nConnencted device list:\n", device_list)
    # print len(device_list)
    PNA = rm.open_resource('GPIB0::3::INSTR')

    if 1==0:
        # following example from keysight page, resets params makes a new S21 window with a measurement name
        PNA.write("SYST:FPReset")
        PNA.write("DISPlay:WINDow1:STATE ON")
        # pna.write("CALCulate:PARameter:DEFine:EXT 'CH1_1_S21',S21")
        PNA.write('CALCulate:PARameter:DEFine CH1_1_S11,S11')
        PNA.write('DISPlay:WINDow1:TRACe1:FEED CH1_1_S11')

    PNA.timeout = 2000

    PNA.write('SENSE1:SWEEP:TYPE CW')
    PNA.write('SENSE1:FREQUENCY:CW 5.005 GHZ')
    PNA.write('SENSE1:SWEEP:MODE CONTINUOUS')
    PNA.write('SENSE1:SWEEP:POINTS 2001')
    PNA.write('SENSE1:SWEEP:TIME:AUTO OFF')
    PNA.write('SENSE1:SWEEP:TIME 1')
    PNA.write('SOURCE1:POWER1:AMPLITUDE -10')
    # initiate the trigger
    PNA.write('OUTPUT:STATE ON')
    # when ini:cont: is OFF, ini:imme is needed to send a trigger signal
    PNA.write('INITIATE:CONTINUOUS ON')
    # PNA.write('INITIATE:IMMEDIATE')
    # PNA.write('GTL')
    # print 'NUMBER:', PNA.query('SYST:COMM:VISA:RDEV:OPEN?')
    # PNA.write('SYSTEM:COMMUNICATE:GPIB:RDEVICE:CLOSE +0')
    # print 20
    PNA.close()
    # PNA.write


except Exception as err:
    print ('\nException', str(err.message))

finally:
    print ('\nEND')
