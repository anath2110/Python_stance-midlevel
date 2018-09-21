# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 18:48:49 2017

@author: Anindita Nath
University of Texas at ElPaso
"""

import numpy as np
import os
def featurizeKeystrokes(audioFilename, player, nframes):
    
#Creates vectors of frame-level keystroke-related data
# for subsequent aggregation into into mid-level features
#Load up the keystroke file corresponding to the specified audio file
# and return the runningfraction, jump count, and motion initiation count 
# computed over 10 millisecond frames.  
#For each output vector, the first value is for
# a 10-ms region centered at 5ms, and so on. 
#converted from original code by Nigel Ward, UTEP, February 2015
#
#player is either 'W' for Watergirl or 'F' for Fireboy
    print("fakefeaturizeKeystrokes")
#    frameSize = 10  # milliseconds
#    rf = np.zeros(nframes + 1,)
#    ju = np.zeros(nframes + 1,)
#    mi = np.zeros(nframes + 1,)
#    
#    [path, basename] = os.path.split(audioFilename)
#    [name,ext]=os.path.splitext(basename)
#    filename = path + '/' + name + '.ks'
#    print('Reading ' + player + ' actions from keystroke file ' + filename)
#    fileContents = importdata(filename)
#    
#    indices = strmatch(player, fileContents.textdata(:,1))
#    
#    if isempty(indices):
#      print('found no %s player actions in keystroke file %s', player, filename);
#      return 
#    
#    for i = indices'
#       kname = fileContents.textdata(i,2)
#       kname = kname{1}
#       kpress = fileContents.data(i,1)
#       krelease = fileContents.data(i,2)
#       initialSlice = floor(kpress/frameSize)   # slice in which keypress happens
#    
#    #   print('processing %s by %s from %d to %d\n', \
#    #	   kname, player, kpress, krelease)
#       if kname=='^':         
#           ju[initialSlice] = 1 + ju[initialSlice]
#    
#        elif (kname=='>' or kname=='<'):
#           mi[initialSlice] = 1 + mi[initialSlice] 
#    
#           #find all 20-ms slices that overlap this keydown region
#           #and add to them the amount of milliseconds that overlap
#           initialSliceStartTime = initialSlice * frameSize
#           overlapOverInitialSlice = (initialSliceStartTime + frameSize) - kpress
#           rf(initialSlice) = overlapOverInitialSlice + rf(initialSlice)
#    
#           finalSlice = floor(krelease / frameSize)
#           finalSliceStartTime = finalSlice * frameSize
#           overlapOverFinalSlice = krelease - finalSliceStartTime
#           rf(finalSlice) = overlapOverFinalSlice + rf(finalSlice)
#    
#           for slice = initialSlice+1:finalSlice-1
#              rf(slice) = rf(slice) + frameSize
#        
#         otherwise
#           warning.warn('unexpected keystroke type, not ^, <, or >')
#    
#    
#    rf = rf(1:end-1)
#    ju = ju(1:end-1)
#    mi = mi(1:end-1)
#   return rf,ju,mi

#test with 
#     [a b c] = featureizeKeystrokes('test', 'W', 700);
# then with
#     [a b c] = featureizeKeystrokes('game01.au', 'W', 100000);
# then examine a(500:700),  b(500:700),  c(500:700), 