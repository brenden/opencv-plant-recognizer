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
    correct = 0

    for (probe, galMatch) in matches.items():
        print '%d (%s) <=> %d (%s)' % (probe, key[probe], galMatch, key[galMatch])
        if key[probe] == key[galMatch]: correct += 1

    accuracy = 1.0 * correct / len(matches)
    print 'accuracy:', accuracy

if __name__ == '__main__':
    main()
