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

def matchLeaf(probe, gallery):
    return 'Chinese horse chestnut'

def main():

    # Check for proper arguments
    if len(sys.argv) != 3:
        print 'Usage: %s [gallery directory] [probe directory]' % sys.argv[0]
        return

    galleryDir = sys.argv[1]
    probeDir = sys.argv[2]

    # Read all the gallery descriptors into a list
    gallery = []
    
    for galFile in os.listdir(galleryDir):
        if galFile == 'index.csv': continue

        galPath = galleryDir + '/' + galFile
        gallery.append(pickle.load(open(galPath, 'r')))

    # Find the best match for each probe
    fileName = lambda name : '.'.join(name.split('.')[:-1])
    matches = {}

    for probeFile in os.listdir(probeDir): 
        probePath = probeDir + '/' + probeFile
        probe = pickle.load(open(probePath, 'r'))
        matchingSpecies = matchLeaf(probe, gallery)
        matches[int(fileName(probeFile))] = matchingSpecies

    print pickle.dumps(matches)

if __name__ == '__main__':
    main()
