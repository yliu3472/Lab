# -*- coding: utf-8 -*-
import visa
import time
import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# set the RF power and frequency of MSG
def mxg_RF_power(frequency = 5, power = -20, power_status = 'ON'):
    MXG = rm.open_resource('GPIB0::1::INSTR')
    # print MXG.query('*IDN?')
    MXG.timeout = 2000
    MXG.write('*CLS')
    # MXG.write('*RST')
    MXG.write('SOURCE:POWER:ALC:STATE ON')
    # Harmonics option does not work in this MXG
    # MXG.write('SOURCE:POWER:HARMONICS:STATE ON')
    # print MXG.query('SOURCE:POWER:HARMONICS?')
    MXG.write('SOURCE:FREQUENCY:MODE CW')
    MXG.write('SOURCE:FREQUENCY:CW %s GHZ' %frequency)
    MXG.write('SOURCE:POWER:MODE FIXED')
    MXG.write('SOURCE:POWER %s' %power)
    # Noise optimization is not working
    # print MXG.query('SOURCE:POWER:NOISE:STATE?')
    MXG.write('OUTPUT:STATE %s' %power_status)
    MXG.close()
    # print 'finished'

def pna_RF_power(frequency = 5.002, power = -20, power_status = 'ON', continuous = 'ON'):
    PNA = rm.open_resource('GPIB0::3::INSTR')
    PNA.write('*CLS')

    if 1 == 0:
        # following example from keysight page, resets params makes a new S21 window with a measurement name
        PNA.write("SYST:FPReset")
        PNA.write("DISPlay:WINDow1:STATE ON")
        # pna.write("CALCulate:PARameter:DEFine:EXT 'CH1_1_S21',S21")
        PNA.write('CALCulate:PARameter:DEFine CH1_1_S11,S11')
        PNA.write('DISPlay:WINDow1:TRACe1:FEED CH1_1_S11')

    PNA.timeout = 2000

    PNA.write('SENSE1:SWEEP:TYPE CW')
    PNA.write('SENSE1:FREQUENCY:CW %s GHZ' %frequency)
    PNA.write('SENSE1:SWEEP:MODE CONTINUOUS')
    PNA.write('SENSE1:SWEEP:POINTS 2001')
    PNA.write('SENSE1:SWEEP:TIME:AUTO OFF')
    PNA.write('SENSE1:SWEEP:TIME 1')
    PNA.write('SOURCE1:POWER1:AMPLITUDE %s' %power)
    # initiate the trigger
    PNA.write('OUTPUT:STATE %s' %power_status)
    # when ini:cont: is OFF, ini:imme is needed to send a trigger signal
    PNA.write('INITIATE:CONTINUOUS %s' %continuous)
    time.sleep(1)
    # PNA.write('INITIATE:IMMEDIATE')
    # PNA.write('GTL')
    # print 'NUMBER:', PNA.query('SYST:COMM:VISA:RDEV:OPEN?')
    # PNA.write('SYSTEM:COMMUNICATE:GPIB:RDEVICE:CLOSE +0')
    # print 20
    PNA.close()

def psa_readout(center_frequency = 5.0, span = 4.0E-2, detuned_f = 5E-3, continus = 'ON', RBW = 39.0, average = 'ON', ave_count = 5, sweep_points = 2001):
    # frequency setting for SFDR3
    f_IMD3_lower = center_frequency - 3.0*detuned_f
    f_IMD3_upper = center_frequency + 3.0*detuned_f
    f_lower = center_frequency - detuned_f
    f_upper = center_frequency + detuned_f

    # frequency setting for SFDR2
    f_HD2_lower = 2.0*(center_frequency - detuned_f)
    f_HD2_upper = 2.0*(center_frequency + detuned_f)
    f_IMD2 = 2.0*center_frequency

    PSA = rm.open_resource('GPIB0::2::INSTR')
    # print PSA.query('*IDN?')
    PSA.write('INSTRUMENT:SELECT SA')
    # when performing average function, the previous measurement
    # needs to be aborted, and then initiate:immediate
    # if the 'continuous' is OFF
    PSA.write('*CLS')
    PSA.write('ABORT')
    PSA.write('INITIATE:CONTINUOUS %s' %continus)
    # set the sweeping mode
    PSA.write('TRACE1:MODE WRITE')
    PSA.write('SWEEP:TIME:AUTO ON')
    PSA.write('SWEEP:TIME:AUTO:RULES NORMAL')
    PSA.write('SWEEP:POINTS %s'%sweep_points)
    PSA.write('FORMAT:TRACE:DATA ASCII')
    PSA.write('FORMAT:BORDER NORMAL')
    # PSA.write('*WAI')
    # PSA.write('INITIATE:IMMEDIATE')
    # setting measurement window
    PSA.write('FREQUENCY:CENTER %s GHZ' %center_frequency)
    PSA.write('FREQUENCY:SPAN %s GHZ' %span)
    PSA.write('BANDWIDTH:RESOLUTION %s KHZ' %RBW)
    PSA.write('BANDWIDTH:VIDEO:RATIO:AUTO ON')
    # visualization
    PSA.write('DISPLAY:WINDOW:TRACE:Y:SCALE:PDIVISION 10 DB')
    PSA.write('DISPLAY:WINDOW:TRACE:Y:SCALE:RLEVEL 10 DBM')
    PSA.write('POWER:RF:ATTENUATION:AUTO ON')
    # detector mode
    # Normal is good for CW signal measurement
    PSA.write('DETECTOR:AUTO OFF')
    PSA.write('DETECTOR:FUNCTION NORMAL')
    # PSA.write('POWER:RF:ATTENUATION 10')
    # average option
    # LOG type is good for looking for signals near noise
    # AUTO use the default method of LOG
    if average is 'ON':
        PSA.write('AVERAGE:STATE ON')
        PSA.write('AVERAGE:TYPE:AUTO ON')
        # PSA.write('AVERAGE:TYPE LOG')
        PSA.write('AVERAGE:COUNT %s' %ave_count)
    else:
        PSA.write('AVERAGE:STATE OFF')

    # place markers for
    # foundamental signals and IMD3 measurements
    PSA.write('CALCULATE:MARKER1:STATE ON')
    PSA.write('CALCULATE:MARKER1:MODE POSITION')
    PSA.write('CALCULATE:MARKER1:X %s GHZ' %f_IMD3_lower)

    PSA.write('CALCULATE:MARKER2:STATE ON')
    PSA.write('CALCULATE:MARKER2:MODE POSITION')
    PSA.write('CALCULATE:MARKER2:X %s GHZ' %f_lower)

    PSA.write('CALCULATE:MARKER3:STATE ON')
    PSA.write('CALCULATE:MARKER3:MODE POSITION')
    PSA.write('CALCULATE:MARKER3:X %s GHZ' % f_upper)

    PSA.write('CALCULATE:MARKER4:STATE ON')
    PSA.write('CALCULATE:MARKER4:MODE POSITION')
    PSA.write('CALCULATE:MARKER4:X %s GHZ' % f_IMD3_upper)
    # functional markers
    # print PSA.query('CALCULATE:MARKER1:Y:READOUT?')
    # PSA.write('CALCULATE:MARKER:TABLE:STATE OFF')
    # PSA.write('CALCULATE:MARKER:AOFF')
    # PSA.write('CALCULATE:MARKER1:FUNCTION OFF')

    PSA.write('INITIATE:IMMEDIATE')
    # PSA.write('*WAI')
    time.sleep(3)
    p_IMD3_lower = PSA.query('CALCULATE:MARKER1:Y?')
    p_lower = PSA.query('CALCULATE:MARKER2:Y?')
    p_upper = PSA.query('CALCULATE:MARKER3:Y?')
    p_IMD3_upper = PSA.query('CALCULATE:MARKER4:Y?')
    spectrum1 = PSA.query_ascii_values('TRACE? TRACE1', container=np.array)

    # measurement window and markers for
    # HD2 and IMD2
    PSA.write('*CLS')
    PSA.write('ABORT')
    PSA.write('INITIATE:CONTINUOUS %s' % continus)
    # PSA.write('*WAI')
    # PSA.write('INITIATE:IMMEDIATE')
    # setting measurement window
    PSA.write('FREQUENCY:CENTER %s GHZ' %f_IMD2)
    PSA.write('FREQUENCY:SPAN %s GHZ' % span)
    PSA.write('BANDWIDTH:RESOLUTION %s KHZ' %RBW)

    PSA.write('CALCULATE:MARKER1:STATE ON')
    PSA.write('CALCULATE:MARKER1:MODE POSITION')
    PSA.write('CALCULATE:MARKER1:X %s GHZ' %f_HD2_lower)

    PSA.write('CALCULATE:MARKER2:STATE ON')
    PSA.write('CALCULATE:MARKER2:MODE POSITION')
    PSA.write('CALCULATE:MARKER2:X %s GHZ' %f_IMD2)

    PSA.write('CALCULATE:MARKER3:STATE ON')
    PSA.write('CALCULATE:MARKER3:MODE POSITION')
    PSA.write('CALCULATE:MARKER3:X %s GHZ' %f_HD2_upper)

    PSA.write('CALCULATE:MARKER4:STATE OFF')
    # PSA.write('CALCULATE:MARKER4:MODE POSITION')
    # PSA.write('CALCULATE:MARKER4:X %s GHZ' % f_IMD3_upper)
    PSA.write('INITIATE:IMMEDIATE')
    time.sleep(3)
    p_HD2_lower = PSA.query('CALCULATE:MARKER1:Y?')
    p_IMD2 = PSA.query('CALCULATE:MARKER2:Y?')
    p_HD2_upper = PSA.query('CALCULATE:MARKER3:Y?')
    # print 'frequency:', f_lower,f_upper,f_HD2_lower,f_HD2_upper,f_IMD2,f_IMD3_lower,f_IMD3_upper
    spectrum2 = PSA.query_ascii_values('TRACE? TRACE1', container=np.array)
    # print 'HD:', p_HD2_lower, type(p_HD2_lower)
    PSA.close()
    out_array = [p_lower, p_upper, p_HD2_lower, p_IMD2, p_HD2_upper, p_IMD3_lower,  p_IMD3_upper]
    # convert the output data type from unicode to string
    # strip the '\n' trailling in each string
    power_array = [str(x).rstrip() for x in out_array]
    # print 'type before:', type(power_array)
    # # power_array = str(power_array)
    # print 'type:', type(power_array)
    # print '1st type:', type(power_array[0])
    # print 'before return:', power_array
    # print spectrum1, spectrum2
    return power_array, spectrum1, spectrum2

def data_save(file_name, data, dir_name, f_head):
    # dir_name = 'SFDR_data'
    file_path = dir_name + '/' + file_name
    try:
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        else:
            print 'Directory exists'

        with open(file_path, 'wb') as csvfile:
            print 'start to write data:'
            fwriter = csv.writer(csvfile, delimiter = ',')
            # file_head = ('Input Power(dB)', 'Main power lower(dB)', 'Main power upper(dB)', 'HD2 lower(dB)',
            #     'IMD2 power(dB)' 'HD2 power(dB)', 'IMD3 lower(dB)', 'IMD3 upper(dB)')
            fwriter.writerow(f_head)
            for line in data:
                fwriter.writerow(line)
                # print 'writting'

    except Exception as err:
        print ('\nException in data saving', str(err.message))

    finally:
        print ('\n Data saved:', file_name)

def save_fig(x_range, data, frequency, power,head_name):
    try:
        fig_title = 'Spectrum_figure/'+str(frequency)+'GHz_'+str(head_name)+str(power)+'dBm.png'

        if not os.path.exists('Spectrum_figure'):
            os.mkdir('Spectrum_figure')
        else:
            print 'Directory exists'
        plt.figure()
        plt.clf()
        plt.plot(x_range, data)
        plt.title('Input RF power setting: '+ str(power)+'dBm')
        plt.xlabel('Freq (GHz)', fontsize=13)
        plt.ylabel('Norm Power (dB)', fontsize=13)
        plt.autoscale(enable=True, axis='x', tight=True)
        plt.savefig(fig_title)
        plt.close()


        # with PdfPages('Spectrum.pdf') as pdf:
        #     plt.figure()
        #     plt.clf()
        #     print 'print figure'
        #     plt.plot(x_range, data)
        #     # plt.show()
        #     plt.xlabel('Freq (GHz)', fontsize=13)
        #     plt.ylabel('Norm Power (dB)', fontsize=13)
        #     plt.tight_layout()
        #     pdf.savefig()
        #     plt.close()
    except Exception as err:
        print ('\nException in fig saving', str(err.message))

    finally:
        print ('\n Data saved:', fig_title)

def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")

try:
    a=time.time()
    # rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
    rm = visa.ResourceManager()
    # device_list = rm.list_resources()
    # print ("\nConnencted device list:\n", device_list)

    frequency_list = [1, 2, 4, 6, 7, 8, 9, 10, 12, 14]
    # frequency_list = [5]
    f_detuning = 5E-3
    span = 4.0E-2
    power_list = np.linspace(-20, 10, 31)
    file_head = ['Input Power(dB)', 'Main power lower(dB)', 'Main power upper(dB)', 'HD2 lower(dB)',
                 'IMD2 power(dB)' 'HD2 power(dB)', 'IMD3 lower(dB)', 'IMD3 upper(dB)']
    file_head1=['frequency (GHz)'] + [str(x)+'(dBm)' for x in power_list]
    # print file_head1
    running_count = len(power_list)*len(frequency_list)
    current_count = 0
    for frequency in frequency_list:
        c_frequency = frequency
        f_lower = c_frequency - f_detuning
        f_upper = c_frequency + f_detuning
        f_points = 2001
        frequency_range1=np.linspace(f_lower,f_upper,f_points)
        frequency_range2=np.linspace(f_lower,f_upper,f_points)
        # for x in range(len(power_list)):
        save_list = []
        save_list1 = np.zeros((len(power_list)+1,f_points))
        save_list2 = np.zeros((len(power_list)+1,f_points))
        save_list1[0][:] = frequency_range1
        save_list2[0][:] = frequency_range2
        file_name= '%s GHz frequency.csv'%c_frequency
        file_name1 = '%s GHz frequency_fundamental.csv' % c_frequency
        file_name2 = '%s GHz frequency_double.csv' % c_frequency

        for n, power_scan in enumerate(power_list):
            current_count+=1
            print 'Running counts: %s/%s'%(current_count,running_count)
            mxg_RF_power(frequency = f_lower, power = power_scan)
            pna_RF_power(frequency = f_upper, power = power_scan)
            power, spectrum1, spectrum2 = psa_readout(center_frequency = c_frequency, span= span, detuned_f = f_detuning, sweep_points = f_points)
            # time.sleep(1)
            # save data as tuples in a list
            # prepare to being written in csv files
            save_list.append(tuple([power_scan] + power))
            save_list1[n+1][:] = spectrum1
            save_list2[n+1][:] = spectrum2

            # time.sleep(1)
            save_fig(frequency_range1, spectrum1, frequency, power_scan,head_name='IMD3_')
            save_fig(frequency_range2, spectrum2, frequency, power_scan,head_name='HD2_')
            # print 'save:', save_list
        # turn off power and sweeping after measurement for equipment safety
        data_save(file_name, save_list, dir_name='SFDR_data',f_head=file_head)
        data_save(file_name1, zip(*save_list1), dir_name='Spectrum', f_head=file_head1)
        data_save(file_name2, zip(*save_list2), dir_name='Spectrum', f_head=file_head1)

        # mxg_RF_power(power_status='OFF')
        # pna_RF_power(power_status='OFF', continuous='OFF')
        time.sleep(1)
    mxg_RF_power(power_status='OFF')
    pna_RF_power(power_status='OFF', continuous='OFF')
    psa_readout(continus='OFF')
    b=time.time()
    print 'Running time: %s minutes' %((b-a)/60)


except Exception as err:
    print ('\nException', str(err.message))

finally:
    print ('\nEND')
