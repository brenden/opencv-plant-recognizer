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

def parseKeyCSV(keyCSV):
    key = {}

    for line in open(keyCSV):
        (species, iFrom, iTo) = line.split(',')
        
        for i in range(int(iFrom), int(iTo)+1):
            key[i] = species

    return key

def main():

    # Check for proper arguments
    if len(sys.argv) != 3:
        print 'Usage: %s [matches pickle] [key CSV]' % sys.argv[0]
        return

    matches = pickle.load(open(sys.argv[1], 'r'))
    keyCSV = sys.argv[2]
    key = parseKeyCSV(keyCSV)

    # Calculate performance metrics
    matchInfo = {}
    matches = [matches[k] == key[k] for k in matches]
    matchInfo['accuracy'] = 1.0 * sum(matches) / len(matches)

    print matchInfo#pickle.dumps(matchInfo)

if __name__ == '__main__':
    main()
