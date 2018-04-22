import numpy as np
import cv2

class ObjectSegmenter:

  def __init__(self):
    pass
    

  def process_watershed(self, image, garment_type):

    markers = self.create_watershed_marker(image, garment_type)
    cv2.imshow('markers', markers)
    cv2.waitKey(0)
    cv2.imshow('image', image)
    cv2.waitKey(0)

    print(image.dtype)
    print(markers.dtype)
    print(image.shape)
    print(markers.shape)

    markers = cv2.watershed(image, markers)

    return markers


  def create_watershed_marker(self, image, garment_type):

    #markers = cv2.Mat(image.shape[:2], cv2.CV_32SC1)
    print(cv2.CV_32SC1)

    markers = np.zeros(image.shape[:2], dtype=np.uint8)

    markers[0:5, 0:5] = 100
    markers[-5:, -5:] = 100
    markers[0:5, -5:] = 100
    markers[-5:, 0:5] = 100


    if False: #garment_type.PANTS:
      y = image.shape[0] * 3/4
      x = image.shape[1] * 1/2 
      
      markers[y-5:y+5, x-20:x+20] = 250

    else:
      y = image.shape[0] * 1/2
      x = image.shape[1] * 1/2 
      
      markers[y-2:y+2, x-2:x+2] = 250

    return markers
