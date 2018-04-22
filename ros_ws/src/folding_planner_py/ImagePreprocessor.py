import cv2
import numpy as np
from ObjectSegmenter import ObjectSegmenter


class ImagePreprocessor:

  def __init__(self):
    self.roi = ((0,100),(880,430));
    self.mask_size = 1000

    self.objectSegmenter = ObjectSegmenter()
    
  def generate_garment_mask(self,file_name, garment_type):
    img = self.crop_rect_roi(file_name)
    # cv.threshold
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)

    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)

    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers+1
    markers[unknown==255] = 0

    markers = cv2.watershed(img,markers)

    img[markers == -1] = [255,0,0]
    img[markers != -1] = [0,0,0]
    cv2.imshow('markers', img)
    cv2.waitKey(0)

    garment_mask = self.create_square_garment_mask(markers)

    return garment_mask

  def crop_rect_roi(self,file_name):
    img_load = cv2.imread(file_name, cv2.IMREAD_COLOR)
    (x1, y1), (x2, y2) = self.roi
    return img_load[y1:y2, x1:x2]

  def segment_object(self, img, garment_type):
    return self.objectSegmenter.process_watershed(img, garment_type)

  def create_square_garment_mask(self, img):

    y1 = max(0, img.shape[0] / 2 - self.mask_size / 2 )
    x1 = max(0, img.shape[1] / 2 - self.mask_size / 2 )

    print(y1,x1)
    return img[y1:, x1:, :]
  

    
