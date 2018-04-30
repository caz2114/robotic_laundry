import numpy as np
from datatypes import SCurve, SVar
from Registration import ComputeAngle

def initGarmentTemplate(garmentType):
    if garmentType.SWEATER:
        return initSweaterTemplate()
    elif garmentType.PANTS:
        return initPantsTemplate()
    else:
        return initTowelTemplate()


# void initSweaterTemplate(SCurve* io_curve, SVar& io_vars)
def initSweaterTemplate():
    closed = True
    nVertices = 12
    io_curve = SCurve(closed, nVertices, np.zeros(nVertices), np.zeros(nVertices), np.arange(nVertices))
    io_vars = SVar(nVertices)

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
    io_vars.pos[0][10] = -1 * io_vars.pos[0][1]
    io_vars.pos[1][10] =  1 * io_vars.pos[1][1]
    io_vars.pos[0][11] = -1 * io_vars.pos[0][0]
    io_vars.pos[1][11] =  1 * io_vars.pos[1][0]

    nSegs = io_curve.nVertices

    for i in range(nSegs):
        im = (i + nSegs -1) % nSegs
        ip = (i + 1) % nSegs

        e_im = io_vars.pos[:, i] - io_vars.pos[:, im]
        e_i = io_vars.pos[:, ip] - io_vars.pos[:, i]

        # theta
        io_curve.restAngles[i] = ComputeAngle(e_im, e_i)
        io_curve.restLengths[i] = np.linalg.norm(e_i)

    return io_curve, io_vars

def initPantsTemplate():
    closed = True
    nVertices = 7
    io_curve = SCurve(closed, nVertices, np.zeros(nVertices), np.zeros(nVertices), np.arange(nVertices))
    io_vars = SVar(nVertices)

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

        e_im = io_vars.pos[:, i] - io_vars.pos[:, im]
        e_i = io_vars.pos[:, ip] - io_vars.pos[:, i]

        # theta
        io_curve.restAngles[i] = ComputeAngle(e_im, e_i)
        io_curve.restLengths[i] = np.linalg.norm(e_i)

    return io_curve, io_vars

def initTowelTemplate():
    closed = True
    nVertices = 4
    io_curve = SCurve(closed, nVertices, np.zeros(nVertices), np.zeros(nVertices), np.arange(nVertices))
    io_vars = SVar(nVertices)

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

        e_im = io_vars.pos[:, i] - io_vars.pos[:, im]
        e_i = io_vars.pos[:, ip] - io_vars.pos[:, i]

        # theta
        io_curve.restAngles[i] = ComputeAngle(e_im, e_i)
        io_curve.restLengths[i] = np.linalg.norm(e_i)

    return io_curve, io_vars
