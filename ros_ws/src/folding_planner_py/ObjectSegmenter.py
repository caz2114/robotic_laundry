import numpy as np
import cv2
from math import acos, degrees

class ObjectSegmenter:

  def __init__(self):
    pass

  def preprocess(self, img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)

    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    return thresh, kernel, opening

  def processWatershed(self, img, kernel, opening):
    # Filtering backgroud background area
    sureBg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    distTransform = cv2.distanceTransform(opening,cv2.DIST_L2,5)

    ret, sureFg = cv2.threshold(distTransform,0.7*distTransform.max(),255,0)

    # Finding unknown region
    sureFg = np.uint8(sureFg)

    unknown = cv2.subtract(sureBg, sureFg)

    markers = self.createWatershedMarker(sureFg, unknown)

    markers = cv2.watershed(img, markers)

    # make sure border of image is not 'marker'
    markers[:5, :] = 1
    markers[-5:, :] = 1
    markers[:, -5:] = 1
    markers[:, :5] = 1

    img[markers == -1] = [255, 0,0]
    img[markers != -1] = [0,0,0]

    return markers


  def createWatershedMarker(self, image, unknown):
    ret, markers = cv2.connectedComponents(image)

    markers += 1

    markers[unknown==255] = 0

    return markers
