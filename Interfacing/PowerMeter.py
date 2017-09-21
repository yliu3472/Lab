import visa
import time
import numpy as np
import matplotlib.pyplot as plt

def power_fetch(average = 50, wavelength = 1550, ext_attenuation = 0, dBm_W = 'DBM', PM_address = 'USB0::0x1313::0x8072::P2001779::0::INSTR'):
    # rm = visa.ResourceManager()
    power_meter = rm.open_resource(PM_address)
    power_meter.timeout = 1000
    power_meter.write('CLS')
    print 'Connected to :', power_meter.query('*IDN?')

    # send settings to the power meter
    power_meter.write('AVERAGE:COUNT %s' %average)
    # print 'Average count: %d' % int(power_meter.query('AVERAGE:COUNT?'))
    power_meter.write('CORRECTION:LOSS ' + str(ext_attenuation))
    # print 'Correction:', power_meter.query('CORRECTION:LOSS?')
    power_meter.write('CORRECTION:WAVELENGTH %s' % wavelength)
    # print 'WAVELENGTH', power_meter.query('CORRECTION:WAVELENGTH?')
    power_meter.write('POWER:RANGE:AUTO 1')
    power_meter.write('POWER:UNIT ' + dBm_W)
    # print 'unit', power_meter.query('POWER:UNIT?')

    # configure the power meter for the following measurements
    # 'configure has to come after the POWER UNIT setting'
    power_meter.write('CONFIGURE:SCALAR:POWER')
    power_meter.write('MEASURE:SCALAR:POWER')
    # start measurement
    power_meter.write('INITIATE:IMMEDIATE')

    time.sleep(average*3e-3)
    measured_power = power_meter.query('FETCH?')
    print 'measured_power:', measured_power
    # print 'Power measurement finished'
    # power_meter.write('INITIATE:IMMEDIATE')
    # print 'initiate'
    # time.sleep(average * 3e-3)
    # print power_meter.query('READ?')
    power_meter.close()

    return measured_power

try:
    a=time.time()

    rm = visa.ResourceManager()
    device_list = rm.list_resources()
    print ("\nConnencted device list:\n", device_list)

    num_measurement = 5
    power = np.zeros(num_measurement)
    for x in range(num_measurement):
        power[x] = (power_fetch(average = 100, dBm_W = 'dBm'))
        print power[x]
    # power = np.array(power)
    plt.figure()
    plt.clf()
    plt.plot(range(num_measurement), power)
    plt.savefig('power.png')
    plt.show()
    plt.close()

    data = (range(num_measurement), power)
    print data
    np.savetxt('data.csv', data, delimiter = ',')



except Exception as err:
    print ('\nException', str(err.message))

finally:
    print ('\nEND')
