from ImagePreprocessor import ImagePreprocessor
from GarmentTemplate import initGarmentTemplate
from datatypes import initSolverVars, SParameters
from FoldPlanner import FoldPlanner
import sys
import skfmm
import cv2
import numpy as np

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

def genInitialVars():
  curve = SCurve(True, 64, np.zeros((64,)), np.zeros((64,)), np.zeros((64,)))

def initParams(df):
  YA = 0.01
  alpha = 0.001
  fit = 20000.0
  conf = 100.0
  df = df
  region_gen = namedtuple('region', ['left', 'right', 'top', 'bottom'])
  region = region_gen(-2.0, 2.0, 2.0, -2.0)
  
  kmax = 200
  epsilon_1 = 1.0e-10
  epsilon_2 = 1.0e-10
  tau = 0.001
  delta = 1.0e-4
  substep_fit = 16
  refLength = 1.0e-1

  return SParameters(YA, alpha, fit, conf, df, region, kmax, epsilon_1, epsilon_2, tau, delta, substep_fit, refLength)
  


if __name__ == "__main__":

  argv = sys.argv

  filename = argv[1]
  garmentType = argv[2]

  mask = imagePreprocessor.generateGarmentMask(filename, garmentType)

  df = skfmm.distance(mask)

  curve, vars = initGarmentTemplate() 
  params = initParams(df)
  
  


  Registration.secantLMMethod(params, curve, initialVars, solverVars, vars)

  points_list = imagePreprocessor.rescalePoints(curve, vars)

  foldPlanner.mappingTrajectory(pointsList, garmentType)



