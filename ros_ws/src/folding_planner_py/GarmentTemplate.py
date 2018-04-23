import numpy as np
from datatypes import SCurve, SVar, resize
from ImageUtil import GarmentType

def initGarmentTemplate():
    if type == GarmentType.SWEATER:
        return initSweaterTemplate()
    elif type == GarmentType.PANTS:
        return initPantsTemplate()
    else:
        return initTowelTemplate()


# void initSweaterTemplate(SCurve* io_curve, SVar& io_vars)
def initSweaterTemplate():
    closed = True
    nVerticies = 12
    io_curve = SCurve(closed, nVerticies, np.zeros(nVerticies), np.zeros(nVerticies), np.zeros(nVerticies))
    io_vars = SVar(np.ndarray((2,io_curve.nVertices)), np.zeros(nVerticies)

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

    return io_curve, io_vars

def initPantsTemplate():
    closed = True
    nVerticies = 12
    io_curve = SCurve(closed, nVerticies, np.zeros(nVerticies), np.zeros(nVerticies), np.zeros(nVerticies))
    io_vars = SVar(np.ndarray((2,io_curve.nVertices)), np.zeros(nVerticies)

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

    return io_curve, io_vars

def initTowelTemplate():
    closed = True
    nVerticies = 12
    io_curve = SCurve(closed, nVerticies, np.zeros(nVerticies), np.zeros(nVerticies), np.zeros(nVerticies))
    io_vars = SVar(np.ndarray((2,io_curve.nVertices)), np.zeros(nVerticies)

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

    return io_curve, io_vars
