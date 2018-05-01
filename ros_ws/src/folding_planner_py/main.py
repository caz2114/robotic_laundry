from ImagePreprocessor import ImagePreprocessor
from GarmentTemplate import initGarmentTemplate
from Registration import SecantLMMethod, initSolverVars
from datatypes import SParameters, SSolverVars
from FoldPlanner import FoldPlanner
import sys
# import skfmm
import cv2
import numpy as np
from collections import namedtuple
import sys

'''
SParameters params;
SCurve curve;
SVar initialVars;
SVar vars;
SDisplayParams displayParams;
SSolverVars solverVars;
'''

imagePreprocessor = ImagePreprocessor()
foldPlanner = FoldPlanner()
GarmentType = namedtuple('garmentType', ['SWEATER', 'PANTS', 'TOWEL'])


def genInitialVars():
  curve = SCurve(True, 64, np.zeros((64,)), np.zeros((64,)), np.zeros((64,)))




if __name__ == "__main__":

  argv = sys.argv

  filename = argv[1]
  garmentType = None

  mask, garmentTypeStr = imagePreprocessor.generateGarmentMaskAndType(filename)


  if garmentTypeStr[0] =='R':
    print "Please rotate the", garmentTypeStr[1:]
    sys.exit()
  elif garmentTypeStr == 'SWEATER':
    garmentType = GarmentType(True, False, False)
  elif garmentTypeStr == 'PANTS':
    garmentType = GarmentType(False, True, False)
  elif garmentTypeStr == 'TOWEL':
    garmentType = GarmentType(False, False, True)

  print "The garment is a type of", garmentTypeStr

  df = skfmm.distance(mask)

  params = initParams(df)

  # determine type of cloths

  curve, vars = initGarmentTemplate(garmentType)

  initialVars = vars

  solverVars = SSolverVars()

  initSolverVars(params, curve, initialVars, solverVars)

  cuve, vars = SecantLMMethod(params, curve, initialVars, solverVars, vars)

  pointList = imagePreprocessor.rescalePoints(curve, vars)

  foldPlanner.MappingTrajectory(pointList, garmentType)
