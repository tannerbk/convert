#!/usr/bin/env python2.7
import sys 
import numpy as np
import h5py
import os 
 
def parse_file(anin, j): 
    '''
    Parse the ASCII data file to extract relevant information. 
    Assumed number of sample (1024) and number of events/file (500)
    are constants. You can extract the following from the converted
    .hdf5 file: 
    -- Array of voltages per channel  
    -- Length of each trace 
    -- Total number of events 
    '''
 
    # Count the number of lines -> events 
    with open(anin) as a:
        for i, l in enumerate(a):
            pass
    events = i + 1

    samples = 1024 
    total_events = events*500
    print total_events 
    voltage = np.zeros([total_events, samples])
    eventcounter = 0
    
    ''' Loop through every file 
        Get each filename 
        For each filename, open each line
        Look for "Ch: %d in each line
        If its there, the voltage info is next line 
        Convert voltage array in list of floats 
        Keep track of event number 
        Return voltage array 
        Size (total events, samples)
    '''
    with open(anin) as ff:
        filename = ff.readlines()
        for k in range(0,len(filename)):
            fline = filename[k]
            fline = fline.strip()
            print fline, 
            print '(CH %d) \r' % j 
            with open(fline) as f: 
                lines = f.readlines()
                for i in range(0,len(lines)):
                    line = lines[i]  
                    line = line.strip()     
                    if ('CH: %d' % j) in line: 
                        line2 = lines[i+1] 
                        k = 0 
                        for dpoint in line2.split():
                            dpoint = float(dpoint)
                            voltage[eventcounter,k] = dpoint 
                            k += 1
                            continue
                        eventcounter += 1
    return voltage

if (__name__=="__main__"):
     # Get array of voltages for each channel 
     channel0 = parse_file("anin.text",0)
     channel1 = parse_file("anin.text",1)
     f = h5py.File("PMYQ.hdf5",'w')
     dset0 = f.create_dataset("channel0",data=channel0,dtype='f8')     
     dset1 = f.create_dataset("channel1",data=channel1,dtype='f8')
     f.close()
