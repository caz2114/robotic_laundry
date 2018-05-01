import numpy as np
from collections import namedtuple

# all items are double
class SRegion:
  def __init__(self, left, right, top, bottom):
    self.left = left
    self.right = right
    self.top = top
    self.bottom = bottom

# bool, int, 1d np, 1d np, 1d np
class SCurve:
  def __init__(self, closed, nVertices, restAngles, restLengths, vertexIDs):
    self.closed = closed
    self.nVertices = nVertices
    self.restAngles = np.zeros((nVertices))
    self.restLengths = np.zeros((nVertices))
    self.vertexIDs = np.zeros((nVertices))


class SVar:
  def __init__(self, d):
    self.pos = np.zeros((2,d))
    self.conf = np.zeros((d))

    
class SSolverVars:
  def __init__(self):
    self.k = 0
    self.nu = 0.0
    self.x = SVar(0)
    self.xnew = SVar(0)
    
    self.m = 0
    self.n = 0
    self.nV = 0

    self.B = np.empty(0)
    self.epsilon = 0.0
    self.g = np.empty(0)
    self.f = np.empty(0)

    self.A_muI = np.empty(0)
    self.h = np.empty(0)

    self.mu = 0.0
    self.I = np.empty(0)
    self.found = False
    self.j = 0
  
    
class SPoint2D:
    def __init__(self):
        self.x = np.zeros(2)

SParameters = namedtuple('SParameters',['YA','alpha','fit','conf','df','region','kmax','epsilon_1',\
            'epsilon_2','tau','delta','substep_fit','refLength'])

GarmentType = namedtuple('garmentType', ['SWEATER', 'PANTS', 'TOWEL'])




