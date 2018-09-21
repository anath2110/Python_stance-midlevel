# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 17:03:00 2017

@author: modified from Alonso's by Anindita Nath
University of Texas at ElPaso
"""

from prosprop import prosprop
import numpy as np
import scipy
from getAnnotations import getAnnotations

def predEval(aufileloc, annotationsDir, ppmfile):

# converted from original by Nigel Ward, UTEP, June 2017
# see ../doc/UTEP-prosody-overview.docx
# called from the top level, to predict and then evaluate the predictions

# predictions = prosprop(aufileloc, annotationsDir, ppmfile, 10, '');
    predictions, blvals = prosprop(aufileloc, annotationsDir, ppmfile, 100, 'l')

    annotations,propertyNames = getAnnotations(annotationsDir)
    #print(annotations.shape)
    actual = concatenateTargets(annotations)

    MSE = comparePropVals(predictions, actual, 'Predictions', True)
    comparePropVals(np.matlib.repmat(blvals, np.shape(actual)[0], 1), actual, 'Baseline', False)
    return predictions, MSE

# ------------------------------------------------------------------
def comparePropVals(predictions, actual, title, printAll):

    if printAll:
        printRows(actual, 'Annotations')
        printRows(predictions, title)


    difference = actual - predictions
    MSE = np.mean(np.multiply(difference,difference),axis=0)

    print('')
    printRow(("MSE for %s"% title), MSE)
    print("overall MSE is %.2f" % np.mean(MSE))
    # Save as matlab variables
    scipy.io.savemat('testregression', {'predictionspy': predictions})   # for regression testing
    return MSE


# ------------------------------------------------------------------
def printRows(matrix, title):
    print("%s" % title)
    for i in range(matrix.shape[0]):
        printRow(("%.2d " % i), matrix[i,:])

# ------------------------------------------------------------------
def printRow(name, values):
    print(name)
    for i in range(len(values)):
        print(" %.2f " % values[i])
    print('\n')

# ------------------------------------------------------------------
def concatenateTargets(annotations):
    nsegments = len(annotations)
    #print(nsegments)
    nproperties = len(annotations['properties'][0])

    actual = np.zeros((nsegments, nproperties))
    for i in range(nsegments):
        actual[i,:] = annotations['properties'][i]
    return actual
# ------------------------------------------------------------------
# test with
# cd testeng
# predEval('audio', 'annotations', 'smalltest-ppm.mat');
# Note that for this the training data is in the test data,
# so can obtain 100% if omit the leave-one-out flat, 'l' when calling prosprop

# larger test
# cd english
# predEval('audio', /annotation', 'ppmfiles/English-ppm.mat'); % takes 2 hours

# Turkish test
# cd turkish

