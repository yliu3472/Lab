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
    print len(device_list)
    # print rm.open_resource('GPIB16::19::INSTR')


except Exception as err:
    print ('\nException', str(err.message))

finally:
    print ('\nEND')
