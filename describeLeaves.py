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
import random
import numpy as np
import scipy as sp, scipy.spatial
random.seed(0)


def segmentLeaf(leafImage):
    (rows, cols, depth) = leafImage.shape
    linearImage = np.reshape(leafImage, (rows*cols, depth)).astype('float32')

    clusters = cv2.kmeans(
        linearImage,
        2,
        (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10),
        1,
        cv2.KMEANS_PP_CENTERS)[1]

    ignoreMap = np.zeros((rows, cols)).astype('uint8')

    for i in range(len(clusters)):
        if clusters[i] == 1:
            ignoreMap[i/cols, i%cols] = 1

    # Smooth and threshold to remove unwanted dots
    ignoreMap = cv2.GaussianBlur(ignoreMap, (0, 0), 2)
    ignoreMap = cv2.threshold(
        ignoreMap,
        .5,
        255.0,
        cv2.THRESH_BINARY)[1]#.astype('float32')

    return ignoreMap


def sampleEdgePoints(ignoreMap):
    edgeMap = cv2.Canny(ignoreMap, 1, 1)
    edgeList = []
    edgeTrace = []

    # Create a list of some edge points (just a few will suffice)
    for r in range(len(edgeMap)):
        for c in range(len(edgeMap[r])):
            if edgeMap[r, c]!=0 and not random.randint(0, 10):
                edgeList.append((0, c, r))

    lastPoint = edgeList.pop()[1:]
    curPoint = lastPoint
    edgeTrace.append(curPoint)
    dist = sp.spatial.distance.euclidean

    # Order the edge points in their trace order around the shape
    while len(edgeList)>0:
        edgeList = [(dist((x, y), curPoint), x, y) for d, x, y in edgeList]
        edgeList.sort()

        for i, (d, x, y) in enumerate(edgeList):
            if d <= dist((x, y), lastPoint):
                lastPoint = curPoint
                curPoint = (x, y)
                edgeTrace.append(curPoint)
                del edgeList[i]
                break

        else:
            lastPoint = curPoint
            curPoint = edgeList.pop()[1:]
            edgeTrace.append(curPoint)

    return edgeTrace


def buildEdgeGraph(edgeTrace, ignoreMap):
    edgeGraph = np.zeros((len(edgeTrace), len(edgeTrace)))
    dist = sp.spatial.distance.euclidean

    for i, (x0, y0) in enumerate(edgeTrace):
        for j, (x1, y1) in enumerate(edgeTrace[i+1:]):

            # Check whether (x0, y0) to (x1, y1) is contained within the shape
            for t in [x/100 for x in range(100)]:
                xt = (1-t)*x0 + t*x1
                yt = (1-t)*y0 + t*y1

                if ignoreMap[yt, xt] != 0:
                    break

            else:
                d = dist((x0, y0), (x1, y1))
                edgeGraph[j+i, i] = d
                edgeGraph[i, j+i] = d

    #edgeGraph /= np.max(edgeGraph)
    #edgeGraph *= 255
    #cv2.imwrite('output.png', edgeGraph)

    return edgeGraph


def innerDistanceShapeContext(edgeGraph, edgeTrace, ignoreMap):
    histList = []
    dist = sp.spatial.distance.euclidean
    logMaxDistance = log(dist((0, 0), ignoreMap.shape), 2)
    edgeDistances = scipy.sparse.csgraph.floyd_warshall(edgeGraph, directed=False)

    for i, (x0, y0) in enumerate(edgeTrace):
        hist = np.zeros((8, 8))

        # Calculate the contour tangent
        (px, py) = edgeTrace[i-1]
        (nx, ny) = edgeTrace[(i+1)%len(edgeTrace)]
        contourTangent = atan2(ny-py, nx-px)

        for j, (x1, y1) in enumerate(edgeTrace):
            if j==i: continue
            distance = edgeDistances[i, j]
            logDistance = log(distance, 2) if distance!=0 else logMaxDistance
            angleToOther = (contourTangent - atan2(y1-y0, x1-x0)) % (2*pi)
            distanceBucket = min(floor(logDistance / (logMaxDistance/8)), 7)
            angleBucket = min(angleToOther / (pi/4), 7)

            hist[angleBucket, distanceBucket] += 1

        histList.append(hist)

    return histList


def describeLeaf(leafImage):
    """Computes a descriptor vector for the given leaf image
    
    Arguments:
    leafImage -- a 2D numpy matrix of intensity values
    
    Returns:
    An n-dimensional vector describing the leaf

    """ 

    ignoreMap = segmentLeaf(leafImage)
    edgeTrace = sampleEdgePoints(ignoreMap)
    edgeGraph = buildEdgeGraph(edgeTrace, ignoreMap)
    descriptor = innerDistanceShapeContext(edgeGraph, edgeTrace, ignoreMap)

    return descriptor


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

        if os.path.isfile(leafDescriptorPath): continue

        # Write the pickled descriptor to the output file
        leafImage = cv2.imread(leafPath)
        leafDescriptor = describeLeaf(leafImage)
        pickle.dump(leafDescriptor, open(leafDescriptorPath, 'wb'))

if __name__ == '__main__':
    main()
