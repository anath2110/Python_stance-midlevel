# -*- coding: utf-8 -*-
"""
Created on Thur Dec 14 13:30:49 2017
@author:modified from Alonso by Anindita Nath
University of Texas at ElPaso
"""

import warnings

#import pickle
import _pickle as pickle
import time
import os
from prosodizeCorpus import prosodizeCorpus
from normalizeCorpus import normalizeCorpus
from getfeaturespec import getfeaturespec
from concatenateFeatures import concatenateFeatures
from getAnnotations import getAnnotations
import numbers
import scipy
import datetime
now = datetime.datetime.now()
import numpy as np
warnings.filterwarnings("ignore")
def makePPM(audioDir, annotationloc, fssfile, ppmfilename,lang):

 # Nigel Ward, UTEP, June 2017
 # creates a prosody-properties mapping file
 # similar to Jason's getStancePCdata
 #
 # to be called directly, on the top level
 # the return value is normally for debugging only
 # if fssfile is 0, compute and save only frame-level features

  provenance = audioDir + ' ' + annotationloc + ' ' +  str(now.month) + '-' + str(now.day) + ' '+ str(now.hour) + ':' + str(now.minute)

  if (isinstance(fssfile, numbers.Real) and fssfile == 0):
    featurespec = 0
    stride = 10
  else:
    featurespec = getfeaturespec(fssfile)
    stride = 100

  prosodized = prosodizeCorpus(audioDir, annotationloc, featurespec, stride,lang)

  [means, stddevs] = computeNormalizationParams(prosodized)
  normalized = normalizeCorpus(prosodized, means, stddevs)

  [propValues, propertyNames] = getAnnotations(annotationloc,lang)
 
  
  model = mergeInPropValues(normalized, propValues)

  algorithm = 'knn'
  
  #save ppmfile as .mat 
 
#  scipy.io.savemat(ppmfilename, {'provenancepy': provenance,'propertyNamespy':propertyNames,\
#  'featurespecpy':featurespec,'meanspy':means,'stddevspy':stddevs,'modelpy':model,'algorithmpy':algorithm})  
   
    #save the ppmfile as pickle file
    #if the file exists, append the new data, else create it 
  with open(ppmfilename, 'wb') as outfile:
          #pickle.dump([provenance,propertyNames,featurespec,means,stddevs,model],outfile, pickle.HIGHEST_PROTOCOL)
          pickle.dump([provenance,propertyNames,featurespec,means,stddevs,model],outfile, protocol=2)
    
  
  return model



# ------------------------------------------------------------------
def computeNormalizationParams(prosodized):
  allPatches = concatenateFeatures(prosodized, 0)
  means = np.mean(allPatches,axis=0)
  stddevs = np.std(allPatches,axis=0)
  return means, stddevs



# ------------------------------------------------------------------
def mergeInPropValues(featuresPlus, propertyValues):
  nsegments = np.shape(featuresPlus)[0]
  if np.shape(propertyValues)[0] != nsegments:
    print('size mismatch between audio files and annotations')
  for i in range(nsegments):
    featuresPlus[i].properties = propertyValues['properties'][i]
  merged = featuresPlus
  return merged


# ------------------------------------------------------------------
#testing
#start=time.time()
#print('creating the model')
#model= makePPM('../testeng/audio/', '../testeng/annotations/', '../testeng/mono4.fss', 'ppmtestpy','E')
#end=time.time()
#dur=end-start
#print('Time taken to create the model :' + str(dur) + '  secs')
#print(len(model))