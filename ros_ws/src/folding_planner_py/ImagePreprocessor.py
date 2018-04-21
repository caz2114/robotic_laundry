import cv2
from ObjectSegmenter import ObjectSegmenter


class ImagePreprocessor:

  def __init__(self):
    self.roi = ((0,100),(600,300));
    self.mask_size = 800

    self.objectSegmenter = ObjectSegmenter()
    
  def generate_garment_mask(self,file_name, garment_type):
    self.crop_rect_roi(file_name)
    seg_result = self.segment_object(garment_type)

    # cv.threshold
    ret, seg_result = cv2.threshold(seg_result, 200, 255, cv2.THRESH_BINARY_INV)

    garment_mask = self.create_square_garment_mask(seg_result)

    return garment_mask

  def crop_rect_roi(self,file_name):
    img_load = cv2.imread(file_name, cv2.IMREAD_COLOR)
    (x1, y1), (x2, y2) = self.roi
    self.img_cropped = img_load[y1:y2, x1:x2]

  def segment_object(self, garment_type):
    return self.objectSegmenter.process_watershed(self.img_cropped, garment_type)

  def create_square_garment_mask(self, img):
    x1 = self.mask_size / 2 - img.shape[1] / 2
    y1 = self.mask_size / 2 - img.shape[0] / 2

    return img[y1:, x1:]
  

    
