import cv2
import numpy as np
from ObjectSegmenter import ObjectSegmenter
from collections import namedtuple

class KeyPt(namedtuple('KeyPt', ['ptId', 'x',  'y'])):
  __slots__ = ()


class ImagePreprocessor:

  def __init__(self):
    self.roi = ((0, 100),(600,400))
    self.roi_x = 0
    self.roi_y = 100
    self.roi_width = 600
    self.roi_height = 300
    
    self.maskSize = 800

    self.objectSegmenter = ObjectSegmenter()

    self.pointList = []
    
  def generateGarmentMask(self,fileName, garmentType):
    img = self.cropRectRoi(fileName)
    markers = self.objectSegmenter.processWatershed(img, garmentType)
    garmentMask = self.createSquareGarmentMask(markers)
    return garmentMask

  def cropRectRoi(self,fileName):
    imgLoad = cv2.imread(fileName, cv2.IMREAD_COLOR)
    (x1, y1), (x2, y2) = self.roi
    return imgLoad[y1:y2, x1:x2]

  def segmentObject(self, img, garmentType):
    return self.objectSegmenter.processWatershed(img, garmentType)

  def createSquareGarmentMask(self, img):
    garment_mask = np.ones((self.maskSize, self.maskSize)) 
    
    y1 = self.maskSize / 2 - img.shape[0] / 2 
    x1 = self.maskSize / 2 - img.shape[1] / 2 

    garment_mask[y1:y1+img.shape[0], x1:x1+img.shape[1]] = img

    return garment_mask

  def rescalePoints(self, ptId, ptPos):
    for i in range(len(ptId)):
      if ptId.vertexIDs[i] >= 0:
        x = ptPos.pos.col[i].x()
        y = ptPos.pos.col[i].y()

        x = x / 2 * self.mask_size / 2 + self.roi_width / 2
        y = (self.roi_width / 2) - (y / 2) * (self.maskSize / 2) + self.roi_y

        keyPoint = keyPt(ptId.vertexIDs[i], x, y)

        self.pointList.append(keyPoint) 

    self.testPoints()
    self.writePointToFile()

  def testPoints(self):
    for k in self.pointsList:
      x = k.y
      y = k.y

      self.img[y-4:y+4, x-4:x+4] = [0,0,255]
   
  def writePointToFile(self):
    with open('keypoints.txt', 'w') as f:
      for point in self.pointsList:
        f.write("%d %d %d \n" % (point.id, point.x, point.y))


