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
import numpy as np
import scipy as sp, scipy.spatial


def describeLeaf(leafFile):
    """Computes a descriptor vector for the given leaf image
    
    Arguments:
    leafFile -- file path to leaf image
    
    Returns:
    An n-dimensional vector describing the leaf

    """
    


def buildSpeciesLookup(leafDescr, leafIndex):
    """Creates a lookup mapping each plant species name to a list of 
    descriptor vectors of images of that species.

    Arguments:
    leafDescr -- A dict mapping image names to descriptor vectors
    leadIndex -- The name of the file containing species info for each image

    Returns:
    A dictionary of {"species name": [list, of, descriptor, vectors]}

    """
    speciesLookup = {}

    for line in open(leafIndex):
        (species, fileRange) = line.strip().split(',')
        (fileFrom, fileTo) = (int(s) for s in fileRange.split('-'))
        speciesLookup[species] = []

        for i in range(fileFrom, fileTo):
            speciesLookup[species].append(leafDescr[str(i)])

    return speciesLookup 


def main():

    # Check for proper arguments
    if len(sys.argv) != 3:
        print 'Usage: %s [image directory] [index]' % sys.argv[0]
        return

    leafDir = sys.argv[1]
    leafIndex = sys.argv[2]

    # Compute a descriptor vector for each image
    imageDescr = {}
    fileName = lambda name : '.'.join(name.split('.')[:-1])

    for im in os.listdir(leafDir):
        imageDescr[fileName(im)] = describeLeaf(leafDir + '/' + im)

    # Build type lookup from images
    speciesLookup = buildSpeciesLookup(imageDescr, leafIndex)

if __name__ == '__main__':
    main()
