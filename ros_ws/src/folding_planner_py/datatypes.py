import numpy as np
from collections import namedtuple


# all items are double
SRegion = namedtuple('SRegion',['left','right','top','bottom'])

# bool, int, 1d np, 1d np, 1d np
SCurve = namedtuple('SCurve',['closed', 'nVertices', 'restAngles', 'restLengths', 'vertexIDs'])

# 2d np, 1d np
SVar = namedtuple('SVar',['pos', 'cond'])

SSolverVars = namedtuple('SSolverVars', ['k','nu','x','xnew','m','n','nV','B','epsilon','g','f','A_muI'\
            ,'h','mu','I','found','j'])

SParameters = namedtuple('SParameters',['YA','alpha','fit','conf','df','region','kmax','epsilon_1',\
            'epsilon_2','tau','delta','substep_fit','refLength'])


# void initSolverVars(const SParameters* in_params, const SCurve* in_curve, const SVar& in_initial_vars, SSolverVars& io_vars, bool update)
def initSolverVars(in_params, in_curve, in_initial_vars, io_vars, update):
    if not update:
        io_vars.k = 0;
		io_vars.nu = 2.0;
		io_vars.j = 0;
		io_vars.epsilon = 1.0e-7;

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
