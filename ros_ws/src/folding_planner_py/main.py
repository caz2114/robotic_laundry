from ImagePreprocessor import ImagePreprocessor
#from FoldPlanner import FoldPlanner
import sys
import skfmm
import cv2
import numpy as np



imagePreprocessor = ImagePreprocessor()
#foldPlanner = FoldPlanner()

params = {
  'alpha':  0.001,
  'YA':  0.01,
  'fit':  20000.0,
  'conf':  100.0,
  'substep_fit':  16,
  'delta':  1.0e-4,
  'tau':  0.001,
  'kmax':  200,
  'epsilon_1':  1.0e-10,
  'epsilon_2':  1.0e-10,
  'region': {
    'left': -2.0,
    'right': 2.0,
    'top': 2.0,
    'bottom': -2.0,
  }
}

'''
curve = {
	closed = true
	nVertices = 64
	restAngles.resize(curve.nVertices)
        curve.restLengths.resize(curve.nVertices)
}'''


def gen_initial_vars():
  pass


if __name__ == "__main__":

  argv = sys.argv

  filename = argv[1]
  garmentType = argv[2]

  mask = imagePreprocessor.generateGarmentMask(filename, garmentType)

  df = skfmm.distance(mask)

  cv2.imshow('df', df/255)
  cv2.waitKey(0)

  genInitialVars()
  genGarmentVars()

  secantLMMethod(params, curve, initialVars, solverVars, vars)

  points_list = imagePreprocessor.rescalePoints(curve, vars)

  foldPlanner.mappingTrajectory(pointsList, garmentType)




