from ImagePreprocessor import ImagePreprocessor
#from FoldPlanner import FoldPlanner
import sys
from collections import Enum



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
  garment_type = argv[2]

  mask = imagePreprocessor.generate_garment_mask(filename, garment_type)

  df = skfmm.distance(mask)

  cv2.imshow('test', df)
  cv2.waitKey(0)

  gen_initial_vars()
  gen_garment_vars()

  secantLMMethod(params, curve, initial_vars, solver_vars, vars)

  points_list = imagePreprocessor.rescale_points(curve, vars)

  foldPlanner.mapping_trajectory(points_list, garment_type)

  
