# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 14:36:31 2017
@author: Anindita Nath
         University of Texas at El Paso         
"""
from filesWithExtension import filesWithExtension
import numpy as np
from readStanceSpreadsheet_madarin import readStanceSpreadsheet

def readStanceAnnotations(csvDirectory):

  #reads all csv files in the current directory, extracts stance-annotation info
  #NSstanceVals: a row for each news segment (NS), a column per stance
  #NStags: a column vector of NS informal names, like 'intro' or 'pollution'
  #To be linux-friendly, this code uses fileread etc. instead of xlsread
  
  # converted from code by Nigel Ward, 2016-2017 Kyoto University and UTEP, with Jason Carlson
  
  #=== first we read in all the segment info, from all annotators === 
  np.set_printoptions(threshold=np.inf)
  csvfiles = filesWithExtension(csvDirectory, ".csv")  
  #print(len(csvfiles))
 
  segmentsSoFar = 0 
  tagssofar=0  
  comtagssofar=0 
  stanceNames = []
  aufilelist=[]
  
  for filei in range(len(csvfiles)) : 
    filename = csvfiles[filei]
    #print("processing  : ", filei,filename )
    
    path = csvDirectory + filename

    [vals, tags, starts, aufile, stNames] = readStanceSpreadsheet(path)   
    #print(vals.shape)
    #print(aufile)
    #print(tags)
    
    # getting shape of numpy arrays for all segments all audios
    for tag in range (0,len(tags)):
      tagIx = tagssofar + tag
    tagssofar = tagssofar + len(tags)
    shapemax=tagIx+1 
    
    # getting shape of numpy array for combined segs for each audio
    aufilelist.append(aufile)
    if(filei==0):
        taglen1staudio=len(tags)
        #print(len(tags))
        
    else:
        if (aufilelist[filei-1]!=aufile):
            #if(len(tags)==1):
                
                #print(len(tags))
            for comtag in range (0,len(tags)):
                comtagIx = comtagssofar + comtag
            comtagssofar =comtagssofar + len(tags)
            taglenotheraudio=comtagIx+1 
            combinedshapemax=taglen1staudio+taglenotheraudio
  #print(shapemax)
  #print(combinedshapemax)
  for filei in range(len(csvfiles)) : 
    filename = csvfiles[filei]
    #print("processing  : ", filei,filename )
    
    path = csvDirectory + filename

    [vals, tags, starts, aufile, stNames] = readStanceSpreadsheet(path)
    #print(vals.shape)
    nsegsInThisBroadcast = len(tags)
    #print(len(tags))    
    
    
    if (filei==0):
        NSstanceVals = np.zeros(shape=(shapemax,14))
        NStags = np.empty(shape=(shapemax,),dtype='S256')
        NSaudioFiles = np.empty(shape=(shapemax,),dtype='S256')
        NSstartTimes = np.zeros(shape=(shapemax,))
        NSendTimes = np.zeros(shape=(shapemax,))
       
    for seg in range (0,nsegsInThisBroadcast):
      #print(seg)
      segIx = segmentsSoFar + seg
      #print(NSstanceVals.shape)
      #print(segIx)
      NSstanceVals[segIx,:] =vals[:,seg] 
      #print(tags[seg])
      NStags[segIx] = tags[seg]
      NSaudioFiles[segIx] = aufile
      #print(aufile)
      #print(NSstartTimes.shape)           
      NSstartTimes[segIx] = starts[seg]
      
      if seg > 0:
          NSendTimes[segIx -1]= starts[seg] #end of previous is start of this
     
    segmentsSoFar = segmentsSoFar + nsegsInThisBroadcast
    if(segmentsSoFar<shapemax):
        NSendTimes[segmentsSoFar] = 0   #a flag
    
    #probably should check that stanceNames are consistent across sheets
    if len(stanceNames)==0 and len(stNames)!=0:
      stanceNames = stNames
    stanceNames=np.asarray(stanceNames)
 	    
  
  # === second, we merge multiple annotators' views of the same segments ===
  
  nsegments = len(NSstartTimes)
  #print(nsegments)
  alreadyHandled =np.zeros(nsegments,)

  combinedVals = np.zeros(shape=(combinedshapemax,14))
  combinedTags = np.empty(shape=(combinedshapemax,),dtype='S256')
  combinedAuNames = np.empty(shape=(combinedshapemax,),dtype='S256')
  combinedEnds=np.zeros(shape=(combinedshapemax,))
  combinedStarts = np.zeros(shape=(combinedshapemax,))
  nUniqueSegments = 0

  for seg in range (nsegments):
    if (alreadyHandled[seg]==True):
      continue
   
    nUniqueSegments = nUniqueSegments + 1
    #print(nUniqueSegments)
    nAnnotationsForThisSegment = 1
    sumOfAnnotations = NSstanceVals[seg,:]
    for possibleMatch in range(seg+1,nsegments):
      if (NSstartTimes[seg] == NSstartTimes[possibleMatch] and \
	  (NSaudioFiles[seg]== NSaudioFiles[possibleMatch]) ):
   #print('found match for %d at %d, size(NSstanceVals) is %d,%d\n', ...
	#seg, possibleMatch, size(NSstanceVals));
          alreadyHandled[possibleMatch] = True
          nAnnotationsForThisSegment = nAnnotationsForThisSegment + 1
          sumOfAnnotations = sumOfAnnotations + NSstanceVals[possibleMatch,:]
      else:
	#no match, so we just skip it
          pass
    combinedVals[nUniqueSegments-1,:] = sumOfAnnotations / nAnnotationsForThisSegment
    combinedStarts[nUniqueSegments-1] = NSstartTimes[seg]
    combinedEnds[nUniqueSegments-1] = NSendTimes[seg]
    combinedTags[nUniqueSegments-1]= NStags[seg]
    combinedAuNames[nUniqueSegments-1] = NSaudioFiles[seg]
   
    
  return combinedVals, combinedTags, combinedStarts, combinedEnds,combinedAuNames, stanceNames

#to test
#cd ppm/testeng
#[combinedVals, combinedTags, combinedStarts, combinedEnds,combinedAuNames, stanceNames] =readStanceAnnotations('../Mandarin stance data/mandarin/trainAnnotationsCSV/')
#[combinedVals, combinedTags, combinedStarts, combinedEnds,combinedAuNames, stanceNames] =readStanceAnnotations('../EnglishDataset/Annotations/')
#print(combinedVals.shape)
#print(combinedTags.shape)
#print(combinedStarts.shape)
#print(combinedEnds.shape)
#print(combinedAuNames.shape)
#print(stanceNames.shape)


