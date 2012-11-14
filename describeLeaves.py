#!/usr/bin/env python

"""
CSE 40535
Brenden Kokoszka
Project
"""

from math import *
import sys
import os
import cv2
import pickle
import numpy as np
import scipy as sp, scipy.spatial


def describeLeaf(leafImage):
    """Computes a descriptor vector for the given leaf image
    
    Arguments:
    leafFile -- a 2D numpy matrix of intensity values
    
    Returns:
    An n-dimensional vector describing the leaf

    """ 


def main():

    # Check for proper arguments
    if len(sys.argv) != 3:
        print 'Usage: %s [leaf directory] [descriptor directory]' % sys.argv[0]
        return

    leafDir = sys.argv[1]
    descriptorDir = sys.argv[2]

    # Describe every lead in the leaf directory
    fileName = lambda name : '.'.join(name.split('.')[:-1])

    for leafFile in os.listdir(leafDir): 
        if leafFile == 'index.csv': continue

        leafPath = leafDir + '/' + leafFile
        leafDescriptorPath = descriptorDir + '/' + fileName(leafFile) + '.p'

        # Write the pickled descriptor to the output file
        leafImage = cv2.imread(leafPath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        leafDescriptor = describeLeaf(leafImage)
        pickle.dump(leafDescriptor, open(leafDescriptorPath, 'wb'))

        print leafFile

if __name__ == '__main__':
    main()
