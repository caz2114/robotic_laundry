import numpy as np

class ObjectSegmenter:

  def __init__(self):
    pass
    

  def process_watershed(self, image, garment_type):

    markers = self.create_watershed_marker(image, garment_type)

    markers = cv2.watershed(image, markers)

    return markers


  def create_watershed_marker(self, image, garment_type):

    markers = np.zeros(image.shape)

    markers[0:5, 0:5] = 100
    markers[-5:, -5:] = 100
    markers[0:5, -5:] = 100
    markers[-5:, 0:5] = 100


    if garment_type.PANTS:
      y = image.shape[0] * 3/4
      x = image.shape[1] * 1/2 
      
      markers[y-5:y+5, x-20:x+20] = 250

    else:
      y = image.shape[0] * 1/2
      x = image.shape[1] * 1/2 
      
      markers[y-2:y+2, x-2:x+2] = 250

    return markers
