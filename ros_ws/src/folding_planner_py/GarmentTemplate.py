import numpy as np
from datatypes import SCurve, SVar, resize
from ImageUtil import GarmentType

def initGarmentTemplate(io_curve, io_vars, Garmentype):
    if type == GarmentType.SWEATER:
        initSweaterTemplate(io_curve, io_vars)
    elif type == GarmentType.PANTS:
        initPantsTemplate(io_curve, io_vars)
    else:
        initTowelTemplate(io_curve, io_vars)


# void initSweaterTemplate(SCurve* io_curve, SVar& io_vars)
def initSweaterTemplate(io_curve, io_vars):
    io_curve.closed = True
    io_curve.nVertices = 12
    io_curve.restAngles = np.zeros(io_curve.nVertices)
    io_curve.restLengths = np.zeros(io_curve.nVertices)
    io_curve.vertexIDs = np.arrange(io_curve.nVertices)

    io_vars.pos = np.ndarray((2,io_curve.nVertices))
    io_vars.conf = np.zeros(io_curve.nVertices)

    io_vars.pos[0][0] = -0.2
    io_vars.pos[1][0] =  0.9
    io_vars.pos[0][1] = -0.5
    io_vars.pos[1][1] =  1.0
    io_vars.pos[0][2] = -1.8
    io_vars.pos[1][2] =  0.4
    io_vars.pos[0][3] = -1.7
    io_vars.pos[1][3] = -0.4
    io_vars.pos[0][4] = -0.6
    io_vars.pos[1][4] =  0.0
    io_vars.pos[0][5] = -0.6
    io_vars.pos[1][5] = -1.0
    io_vars.pos[0][6] = -1 * io_vars.pos[0][5]
    io_vars.pos[1][6] =  1 * io_vars.pos[1][5]
    io_vars.pos[0][7] = -1 * io_vars.pos[0][4]
    io_vars.pos[1][7] =  1 * io_vars.pos[1][4]
    io_vars.pos[0][8] = -1 * io_vars.pos[0][3]
    io_vars.pos[1][8] =  1 * io_vars.pos[1][3]
    io_vars.pos[0][9] = -1 * io_vars.pos[0][2]
    io_vars.pos[1][9] =  1 * io_vars.pos[1][2]
    io_vars.pos[0][0] = -1 * io_vars.pos[0][1]
    io_vars.pos[1][0] =  1 * io_vars.pos[1][1]
    io_vars.pos[0][1] = -1 * io_vars.pos[0][0]
    io_vars.pos[1][1] =  1 * io_vars.pos[1][0]

    nSegs = io_curve.nVertices

    for i in range(nSegs):
        im = (i + nSegs -1) % nSegs
        ip = (i + 1) % nSegs

        e_im = np.diff(io_vars.pos.col[i],io_vars.pos.col[im])
        e_i = np.diff(io_vars.pos.col[ip], io_vards.pos.col[i])

        # theta
        io_curve.restAngles[i] = ComputeAngle(e_im, e_i)
        io_curve.restLengths[i] = np.linalg.norm(e_i)

def initPantsTemplate(io_curve, io_vars):
    io_curve.closed = True
    io_curve.nVertices = 4
    io_curve.restAngles = np.zeros(io_curve.nVertices)
    io_curve.restLengths = np.zeros(io_curve.nVertices)
    io_curve.vertexIDs = np.arrange(io_curve.nVertices)

    io_vars.pos = np.ndarray((2,io_curve.nVertices))
    io_vars.conf = np.zeros(io_curve.nVertices)

    io_vars.pos[0][0] =  0.2
    io_vars.pos[1][0] =  0.0
    io_vars.pos[0][1] = -1.2
    io_vars.pos[1][1] =  0.2
    io_vars.pos[0][2] = -1.2
    io_vars.pos[1][2] =  0.9
    io_vars.pos[0][3] =  1.3
    io_vars.pos[1][3] =  0.7
    io_vars.pos[0][4] =  1 * io_vars.pos[0][3]
    io_vars.pos[1][4] = -1 * io_vars.pos[1][3]
    io_vars.pos[0][5] =  1 * io_vars.pos[0][2]
    io_vars.pos[1][5] = -1 * io_vars.pos[1][2]
    io_vars.pos[0][6] =  1 * io_vars.pos[0][1]
    io_vars.pos[1][6] = -1 * io_vars.pos[1][1]

    nSegs = io_curve.nVertices

    for i in range(nSegs):
        im = (i + nSegs -1) % nSegs
        ip = (i + 1) % nSegs

        e_im = np.diff(io_vars.pos.col[i],io_vars.pos.col[im])
        e_i = np.diff(io_vars.pos.col[ip], io_vards.pos.col[i])

        # theta
        io_curve.restAngles[i] = ComputeAngle(e_im, e_i)
        io_curve.restLengths[i] = np.linalg.norm(e_i)

def initTowelTemplate(io_curve, io_vars):
    io_curve.closed = True
    io_curve.nVertices = 4
    io_curve.restAngles = np.zeros(io_curve.nVertices)
    io_curve.restLengths = np.zeros(io_curve.nVertices)
    io_curve.vertexIDs = np.arrange(io_curve.nVertices)

    io_vars.pos = np.ndarray((2,io_curve.nVertices))
    io_vars.conf = np.zeros(io_curve.nVertices)

    io_vars.pos[0][0] =  1.5;
    io_vars.pos[1][0] =  1.0
    io_vars.pos[0][1] =   1 * io_vars.pos[0][0]
    io_vars.pos[1][1] = - 1 * io_vars.pos[1][0]
    io_vars.pos[0][2] = - 1 * io_vars.pos[0][0]
    io_vars.pos[1][2] = - 1 * io_vars.pos[1][0]
    io_vars.pos[0][3] = - 1 * io_vars.pos[0][0]
    io_vars.pos[1][3] =   1 * io_vars.pos[1][0]

    nSegs = io_curve.nVertices

    for i in range(nSegs):
        im = (i + nSegs -1) % nSegs
        ip = (i + 1) % nSegs

        e_im = np.diff(io_vars.pos.col[i],io_vars.pos.col[im])
        e_i = np.diff(io_vars.pos.col[ip], io_vards.pos.col[i])

        # theta
        io_curve.restAngles[i] = ComputeAngle(e_im, e_i)
        io_curve.restLengths[i] = np.linalg.norm(e_i)
