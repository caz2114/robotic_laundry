import numpy as np
from collections import namedtuple
from Registration import ComputeNumericalDerivative, Compute_f

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
  
    
SParameters = namedtuple('SParameters',['YA','alpha','fit','conf','df','region','kmax','epsilon_1',\
            'epsilon_2','tau','delta','substep_fit','refLength'])


# void initSolverVars(const SParameters* in_params, const SCurve* in_curve, const SVar& in_initial_vars, SSolverVars& io_vars, bool update)

def initSolverVars(in_params, in_curve, in_initial_vars, io_vars, update=False):
  if not update:
    io_vars.k = 0;
    io_vars.nu = 2.0;
    io_vars.j = 0;
    io_vars.epsilon = 1.0e-7;

    if not io_vars.x:
        io_vars.x = np.zeros(in_curve.nVertices) + in_initial_vars
        io_vars.x_new = np.zeros(in_curve.nVertices) + in_initial_vars

  if not update or io_vars.x.pos.shape()[1] != in_curve.nVertices:
    nSegs = in_curve.nVertices if in_curve.closed else in_curve - 1
    nAngles = in_curve.nVertices if in_curve.closed else in_curve - 2

    # io_vars is a SSolverVar type
    io_vars.m = nSegs + nAngles + nSegs
    io_vars.n = in_curve.nVertices * 2
    io_vars.nV = in_curve.nVertices

    io_vars.B = np.zeros((io_vars.m, io_vars.n))
    io_vars.g = np.zeros(io_vars.n)
    io_vars.f = np.zeros(io_vars.m)

    io_vars.A_muI = np.zeros(io_vars.n, io_vars.n)
    io_vars.h = np.zeros(io_vars.n)
    io_vars.g = np.zeros(io_vars.n)
    io_vars.I = np.identity(io_vars.n)


  ComputeNumericalDerivative(in_params, in_curve, io_vars.x, io_vars.epsilon, io_vars.B)
  Compute_f(in_params, in_curve, io_vars.x, io_vars.f)

  io_vars.g = np.multiply(np.transpose(io_vars.B),io_vars.f)
  io_vars.A_muI = np.multiply(np.transpose(io_vars.B),io_vars.B)

  io_vars.mu = in_params.tau * np.amax(np.abs(io_vars.A_muI))
  io_vars.found = np.amax(np.abs(io_vars.g)) <= in_params.epsilon_1

  print("|g|_inf: {}\n".format(np.amax(np.abs(io_vars.g))))


