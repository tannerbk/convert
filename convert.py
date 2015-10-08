#!/usr/bin/env python2.7
import sys 
import numpy as np
import h5py
''' Convert ASCII CAEN files to .hdf5 files ''' 

''' Count files ''' 
def count_files(ascii_filename):
    with open(ascii_filename) as a:
        for i, l in enumerate(a):
            pass
    files = i + 1
    return files

''' Parse the ASCII data file to extract relevant information.
Assumed number of sample (1024) and number of events/file (1000)
are constants.
'''
def parse_file(ascii_filename, channel_number):
    samples = 1024
    files = count_files(ascii_filename)
    total_events = files*1000
    print total_events
    voltage = np.empty([total_events, samples], dtype='f')
    eventcounter = 0
    
    with open(ascii_filename) as ff:
        filename = ff.readlines()
        for k in range(0,len(filename)):
            fline = filename[k]
            fline = fline.strip()
            print fline
            with open(fline) as f:
                lines = f.readlines()
                for i in range(0,len(lines)):
                    line = lines[i]
                    line = line.strip()
                    if ('CH: %d' % channel_number) in line:
                        line2 = lines[i+1]
                        samplecounter = 0
                        for dpoint in line2.split():
                            dpoint = float(dpoint)
                            voltage[eventcounter,samplecounter] = dpoint
                            samplecounter += 1
                            continue
                        eventcounter += 1
    return voltage

''' Save to an hdf5 dataset '''
def get_dataset(f, ascii_filename, num_channels):
     files = count_files(ascii_filename)
     events = files*1000
     samples = 1002
     for i in range(0,num_channels+1):
         channel_name = 'channel%d' % i
         print channel_name
         channel_info = parse_file(ascii_filename,i)
     dataset = f.create_dataset(channel_name,data=channel_info,dtype='f4')
     channel_info = np.empty([events,samples])
     return dataset

''' Accept user inputs '''
if (__name__=="__main__"):
     import argparse
     parser = argparse.ArgumentParser(description='Accept ASCII file to convert.')
     parser.add_argument('ascii_filename', help='Name of ASCII File')
     parser.add_argument('hdf5_filename', help='Name of HDF5 file')
     parser.add_argument('num_channels', type=int, help='Number of channels')
     args = parser.parse_args()

     f = h5py.File(args.hdf5_filename,'w')
     get_dataset(f,args.ascii_filename,args.num_channels)
     f.close()
