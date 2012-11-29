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
    bestMatch = None
    bestMatchDist = np.inf
    dist = sp.spatial.distance.euclidean

    for (name, descriptor) in gallery:
        sys.stderr.write('   %s\n' % name)
        dists = []

        # For all pairs of probe and gallery subdescriptors
        for pDesc in probe:
            minDist = min([dist(pDesc.flat, gDesc.flat) for gDesc in descriptor])
            dists.append(minDist)
        
        dists.sort()
        avgDist = sum(dists[:10])/10.0
        
        if avgDist < bestMatchDist:
            bestMatch = name
            bestMatchDist = avgDist
    
    return bestMatch


def main():

    # Check for proper arguments
    if len(sys.argv) != 3:
        print 'Usage: %s [gallery directory] [probe directory]' % sys.argv[0]
        return

    galleryDir = sys.argv[1]
    probeDir = sys.argv[2]
    fileName = lambda name : '.'.join(name.split('.')[:-1])

    # Read all the gallery descriptors into a list
    gallery = []
    
    for galFile in os.listdir(galleryDir):
        if galFile == 'index.csv': continue

        galPath = galleryDir + '/' + galFile
        gallery.append((fileName(galFile), pickle.load(open(galPath, 'r'))))

    # Find the best match for each probe
    matches = {}

    for probeFile in os.listdir(probeDir): 
        sys.stderr.write('matching %s\n' % probeFile)
        probePath = probeDir + '/' + probeFile
        probe = pickle.load(open(probePath, 'r'))
        galMatch = matchLeaf(probe, gallery)
        matches[int(fileName(probeFile))] = int(galMatch)

    print pickle.dumps(matches)

if __name__ == '__main__':
    main()
