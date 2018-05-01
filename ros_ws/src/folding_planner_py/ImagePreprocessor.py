import cv2
import numpy as np
from ObjectSegmenter import ObjectSegmenter
from collections import namedtuple
from copy import deepcopy

class KeyPt(namedtuple('KeyPt', ['id', 'x',  'y'])):
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
    self.img = None

  def generateGarmentMaskAndType(self, fileName):
  # def generateGarmentMask(self, fileName, garmentType):
    crop_img = self.cropRectRoi(fileName)
    thresh, kernel, opening = self.objectSegmenter.preprocess(crop_img)
    markers = self.objectSegmenter.processWatershed(crop_img, kernel, opening)

    garmentMask = self.createSquareGarmentMask(markers)
    garmentType = self.classifyGarment(crop_img, thresh, opening, markers)

    return garmentMask, garmentType

  def cropRectRoi(self, fileName):
    self.img = cv2.imread(fileName, cv2.IMREAD_COLOR)
    return deepcopy(self.img[self.roi_y:self.roi_y + self.roi_height, self.roi_x:self.roi_width + self.roi_x])

  def segmentObject(self, img):
    return self.objectSegmenter.processWatershed(img)

  def createSquareGarmentMask(self, img):
    garment_mask = np.ones((self.maskSize, self.maskSize))

    y1 = self.maskSize / 2 - img.shape[0] / 2
    x1 = self.maskSize / 2 - img.shape[1] / 2

    garment_mask[y1:y1+img.shape[0], x1:x1+img.shape[1]] = img

    return garment_mask

  def classifyGarment(self, img, thresh, opening, cnt):
    # Getting contour for clothing item
    cloth_cnt = np.zeros(np.shape(img)[:2], np.uint8)
    cloth_cnt[cnt == 1] = 0
    cloth_cnt[cnt != 1] = 255

    im2, contours, hierarchy = cv2.findContours(cloth_cnt, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = np.argmax([len(i) for i in contours])
    cnt = contours[max_contour]

    cv2.drawContours(img, [cnt], -1, (0,255,0), 1)

    # Bounding box around clothing
    hull = cv2.convexHull(cnt,returnPoints = False)
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    # Templates for comparision
    # clothing bound box
    cloth_bound = thresh[y:(y+h+1),x:(x+w+1)]

    #score
    towel_score = self.towelTemplate(cloth_bound, h, w)
    pant_score = self.pantTemplate(cloth_bound, h, w)
    shirt_score = self.shirtTemplate(cloth_bound, h, w)

    score = np.concatenate((towel_score, pant_score, shirt_score), axis = 0)
    garmentType = ['TOWEL','PANTS','RPANTS','RPANTS','RPANTS','SWEATER','RSWEATER','RSWEATER','RSWEATER']

    print "The percent difference between each item is", score, "for towel, pants, and sweater repectively."

    return garmentType[np.argmin(score)]

  # returns an single value
  def towelTemplate(self, cloth_bound, h, w):
    towel_template = 255*np.ones((h+1,w+1),np.uint8)
    towel_score = 1.0 * np.sum(np.not_equal(towel_template,cloth_bound))/((h+1)*(w+1))
    return [towel_score]

  # returns an array of 4 values with diff percent for different orientation
  def pantTemplate(self, cloth_bound, h, w):
    pant_template = np.zeros((h+1,w+1), np.uint8)
    pant_cnt = np.array([[0,18],[25,16],[25,2],[0,0],[0,7],[14,9],[0,11]])
    pant_resize = np.multiply(pant_cnt, [w/25.0,h/18.0]).astype(int)
    cv2.fillConvexPoly(pant_template, pant_resize, 255)

    pant_score = []
    for i in range(4):
        template = np.rot90(pant_template,i)
        template = cv2.resize(template, dsize=(w+1, h+1), interpolation=cv2.INTER_CUBIC)

        pant_score.append(1.0 * np.sum(np.not_equal(template,cloth_bound))/((h+1)*(w+1)))
    return pant_score

  # returns an array of 4 values with diff percent for different orientation
  def shirtTemplate(self, cloth_bound, h, w):
    shirt_template = np.zeros((h+1,w+1), np.uint8)
    shirt_cnt = np.array([[16, 19],[13 ,20],[ 0, 14],\
                        [ 1,  6],[12, 10],[12,  0],\
                        [24,  0],[24, 10],[35,  6],\
                        [36,  14],[23, 20],[20, 19]])
    shirt_resize = np.multiply(shirt_cnt, [w/36.0,h/20.0]).astype(int)
    # fillConvexPoly does not completely fill the shape, this is manually creating shirt
    cv2.fillConvexPoly(shirt_template, shirt_resize[2:5], 255)
    cv2.fillConvexPoly(shirt_template, shirt_resize[7:10],255)
    cv2.fillConvexPoly(shirt_template, shirt_resize, 255)
<<<<<<< HEAD

    shirt_score = []
    for i in range(4):
        template = np.rot90(shirt_template,i)
        template = cv2.resize(template, dsize=(w+1, h+1), interpolation=cv2.INTER_CUBIC)

        shirt_score.append(1.0 * np.sum(np.not_equal(template,cloth_bound))/((h+1)*(w+1)))
    return shirt_score
=======
    #score
    towel_score = 1.0 * np.sum(np.not_equal(towel_template,cloth_bound))/((h+1)*(w+1))
    pant_score = 1.0 * np.sum(np.not_equal(pant_template,cloth_bound))/((h+1)*(w+1))
    shirt_score = 1.0 * np.sum(np.not_equal(shirt_template, cloth_bound))/((h+1)*(w+1))

    score = [towel_score, pant_score, shirt_score]
    garmentType = ['TOWEL','PANTS','SWEATER']
>>>>>>> ea5383ae27282b4a421183cfff65f49c6fba8a1e


  def rescalePoints(self, ptId, ptPos):
    for i in range(ptId.nVertices):
      if ptId.vertexIDs[i] >= 0:
        x = ptPos.pos[0, i]
        y = ptPos.pos[1, i]
        print(x,y)

        #x = x / 2.0f * (float)(maskSize/2)   + (float)this->roi.width/2
        x = (x / 2.0) * (self.maskSize / 2.0) + (self.roi_width / 2.0)

        #y = (float)(this->roi.height/2) - y / 2.0f * (float)(maskSize/2) + (float)this->roi.y
        y = (self.roi_height / 2.0) - (y / 2.0) * (self.maskSize / 2.0) + self.roi_y

        keyPoint = KeyPt(ptId.vertexIDs[i], int(x), int(y))

        self.pointList.append(keyPoint)

    self.testPoints()
    self.writePointToFile()

    return self.pointList

  def testPoints(self):
    for k in self.pointList:
      x = k.x
      y = k.y

      print(x, y)
      self.img[y-4:y+4, x-4:x+4] = [0,0,255]

    cv2.imwrite('final_img.png', self.img)

  def writePointToFile(self):
    with open('keypoints.txt', 'w') as f:
      for point in self.pointList:
        f.write("{} {} {} \n".format(point.id, point.x, point.y))


  def printResults(self, towel_template, pant_template, shirt_template):
    pass
    # TODO pass in all the neccesary variables
    # print resized templates
    # cv2.imshow('image',towel_template)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imshow('image',pant_template)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imshow('image',shirt_template)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # print original templates
    # pant_ori = np.zeros((19,26))
    # cv2.fillConvexPoly(pant_ori, pant_cnt, 255)
    # cv2.imshow('image',pant_ori)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # shirt_ori = np.zeros((21,37))
    # cv2.fillConvexPoly(shirt_ori, shirt_cnt[2:5], 255)
    # cv2.fillConvexPoly(shirt_ori, shirt_cnt[7:10],255)
    # cv2.fillConvexPoly(shirt_ori, shirt_cnt, 255)
    # cv2.imshow('image',shirt_ori)

    # prints difference between template and garment
    # cv2.imshow('image',(255 * np.not_equal(towel_template,cloth_bound)).astype(np.uint8))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imshow('image',(255 * np.not_equal(pant_template,cloth_bound)).astype(np.uint8))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imshow('image',(255 * np.not_equal(shirt_template,cloth_bound)).astype(np.uint8))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

