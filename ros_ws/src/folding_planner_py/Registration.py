import math
import numpy as np
from copy import deepcopy
from datatypes import SPoint2D
import sys
import numba

# double ComputeAngle(const Eigen::Vector2d& input_one, const Eigen::Vector2d& input_two)

def ComputeAngle(input_one, input_two):
    r_sinT = input_one[0]*input_two[1] - input_one[1]*input_two[0]
    r_cosT = -1 * np.sum(np.dot(input_one, input_two))
    return np.arctan2(r_sinT, r_cosT)


def sgn(x):
    return 1.0 if x >= 0.0 else -1.0

# TODO: might be able to optimize, also check accuracy

def ComputeOmegaFromAngle(theta):
	sinT = math.sin(theta);
	cosT = math.cos(theta);
	tan_phi_over_2 = sgn(sinT) * math.sqrt((1.0+cosT)/(max(0.0, 1.0-cosT) + 1.0e-10));
	return 2.0 * tan_phi_over_2;


def computeOmega(input_one, input_two):
    return ComputeOmegaFromAngle(ComputeAngle(input_one, input_two))

# double sampleDistanceField(const SImage<double, 1>& in_df, const SRegion& in_region, const Eigen::Vector2d& x)
# TODO: check math

def sampleDistanceField(in_df, in_region, x):
    assert in_df.shape[0] == in_df.shape[1]
    assert in_region.right-in_region.left == in_region.top-in_region.bottom

    proj_x = x
    proj_x[0] = max(in_region.left,   min(in_region.right, x[0]))
    proj_x[1] = max(in_region.bottom, min(in_region.top,   x[1]))

    dist_scale = (in_region.right-in_region.left) / in_df.shape[1]

    fi = (proj_x[0] - in_region.left)   * in_df.shape[1] / (in_region.right - in_region.left)
    fj = (proj_x[1] - in_region.bottom) * in_df.shape[0] / (in_region.top - in_region.bottom)

    i  = max(0, min(in_df.shape[1]-1, int(fi)))
    j  = max(0, min(in_df.shape[0]-1, int(fj)))

    ip = min(in_df.shape[1]-1, i+1);
    jp = min(in_df.shape[0]-1, j+1);

    s = fi - int(fi)
    t = fj - int(fj)


    in_df_flat = in_df.flatten()
    dist_proj = (1.0 - t) * (s * in_df_flat[j*in_df.shape[1]+ip] + (1.0-s) * in_df_flat[j*in_df.shape[1]+i]) \
		+ t * (s * in_df_flat[jp*in_df.shape[1]+ip] + (1.0-s) * in_df_flat[jp*in_df.shape[1]+i])

    return dist_proj * dist_scale + np.linalg.norm(proj_x - x)

# double integrateDF2OverSegment(const SParameters* in_params, const Eigen::Vector2d& x1, const Eigen::Vector2d& x2, const double rest_length)

def integrateDF2OverSegment(in_params, x1, x2, rest_length):
    tot = 0.0
    length = rest_length / in_params.substep_fit

    for i in range(in_params.substep_fit):
        p1 = x1 + (x2-x1) * float(i)/float(in_params.substep_fit)
        p2 = x1 + (x2-x1) * float(i+1.0)/float(in_params.substep_fit)

        d1 = sampleDistanceField(in_params.df, in_params.region, p1)
        d2 = sampleDistanceField(in_params.df, in_params.region, p2)

        e1 = 0.5 * (math.exp(d1) + math.exp(-d1)) - 1.0
        e2 = 0.5 * (math.exp(d2) + math.exp(-d2)) - 1.0

        tot += 0.5 * (e1*e1+e2*e2) * length

    return tot

# inline double computeSegmentElasticEnergy(const Eigen::Vector2d& p1, const Eigen::Vector2d& p2, const double& YA, const double& rest_length)
# ignoring inline

def computeSegmentElasticEnergy(p1, p2, YA, rest_length):
    diff = p1 - p2

    return 0.5 * YA * rest_length * (np.linalg.norm(diff)/rest_length - 1.0)**2

# inline double computeSegmentBendingEnergy(const Eigen::Vector2d& pp, const Eigen::Vector2d& pc, const Eigen::Vector2d& pn,
# 	const double& alpha, const double& rest_length_p, const double& rest_length_n, const double& theta)
# ignoring inline

def computeSegmentBendingEnergy(pp, pc, pn, alpha, rest_length_p, rest_length_n, theta):
    e_im = pc - pp
    e_i = pn - pc

    omega = computeOmega(e_im, e_i)
    omega_bar = ComputeOmegaFromAngle(theta)

    return alpha * (omega - omega_bar)**2 / (rest_length_p+rest_length_n)


def computeEnergy_elastic(in_params, in_curve, in_position):
    nVert = in_curve.nVertices
    nSegs = nVert if in_curve.closed else (nVert -1)

    energy = 0.0

    for i in range(nSegs):
        # assuming in_posistion is a matric 2 by d
        energy += computeSegmentElasticEnergy(in_position[:,(i+1)%nVert], in_position[:,i], in_params.YA, in_curve.restLengths[i])

    return energy

# double computeEnergy_bending(const SParameters* in_params, const SCurve* in_curve, const Eigen::Matrix2Xd& in_position)

def computeEnergy_bending(in_params, in_curve, in_position):
    nVert = in_curve.nVertices
    nAngles = nVert if in_curve.closed else (nVert-2)

    energy = 0.0
    for i in range(nAngles):
        if in_curve.closed:
            iim = (i + nVert - 1) % nVert
            ii = i
            iip = (i + 1) % nVert

            restL_m = in_curve.restLengths[(i + nVert - 1) % nVert]
            restL = in_curve.restLengths[i]
        else:
            iim = i
            ii = i + 1
            iip = i + 2

            restL_m = in_curve.restLengths[i]
            restL = in_curve.restLengths[i+1]

        energy += computeSegmentBendingEnergy(in_position[:,iim], in_position[:,ii], in_position[:,iip],\
			in_params.alpha, restL_m, restL, in_curve.restAngles[i])
    return energy

# double computeEnergy_fit(const SParameters* in_params, const SCurve* in_curve, const Eigen::Matrix2Xd& in_position)

def computeEnergy_fit(in_params, in_curve, in_position):
    nVert = in_curve.nVertices
    nSegs = nVert if in_curve.closed else (nVert -1)

    energy = 0.0
    for i in range(nSegs):
        int_df_seg = integrateDF2OverSegment(in_params, in_position[:,i], in_position[:,(i+1)%nVert], in_curve.restLengths[i])
        energy += 0.5 * in_params.fit * int_df_seg

    return energy


def ComputeEnergy(in_params, in_curve, in_vars):
    E_elastic = computeEnergy_elastic(in_params, in_curve, in_vars.pos)
    E_bending = computeEnergy_bending(in_params, in_curve, in_vars.pos)
    E_fit = computeEnergy_fit(in_params, in_curve, in_vars.pos)
    return E_elastic + E_bending + E_fit


def compute_f_elastic(in_params, in_curve, in_position, io_f, offset_row):
    nSegs = in_curve.nVertices if in_curve.closed else (in_curve.nVertices -1)

    assert io_f.shape[0] >= nSegs + offset_row
    assert in_curve.nVertices == in_position.shape[1]

    for i in range(nSegs):
        # might be [:,i]
        diff = in_position[:,(i+1)%in_curve.nVertices] - in_position[:,i]
        io_f[i+offset_row] = math.sqrt(0.5 * in_params.YA * in_curve.restLengths[i]) * (np.linalg.norm(diff) / in_curve.restLengths[i] - 1)

# void compute_f_bending(const SParameters* in_params, const SCurve* in_curve, const Eigen::Matrix2Xd& in_position, Eigen::VectorXd& io_f, int offset_row)

def compute_f_bending(in_params, in_curve, in_position, io_f, offset_row):
    nAngles = in_curve.nVertices if in_curve.closed else (in_curve.nVertices-2)
    nVert = in_curve.nVertices

    assert io_f.shape[0] >= nAngles + offset_row
    assert in_curve.nVertices == in_position.shape[1]

    for i in range(nAngles):
        if in_curve.closed:
            iim = (i + nVert - 1) % nVert
            ii = i
            iip = (i + 1) % nVert

            restL_m = in_curve.restLengths[(i + nVert - 1) % nVert]
            restL = in_curve.restLengths[i]
        else:
            iim = i
            ii = i + 1
            iip = i + 2

            restL_m = in_curve.restLengths[i]
            restL = in_curve.restLengths[i+1]

        e_im = in_position[:,ii] - in_position[:,iim]
        e_i = in_position[:,iip] - in_position[:,ii]

        omega = computeOmega(e_im, e_i)
        omega_bar = ComputeOmegaFromAngle(in_curve.restAngles[i])
        io_f[i+offset_row] = math.sqrt(in_params.alpha/(restL_m + restL)) * (omega - omega_bar)


# void compute_f_fit(const SParameters* in_params, const SCurve* in_curve, const Eigen::Matrix2Xd& in_position, Eigen::VectorXd& io_f, int offset_row)

def compute_f_fit(in_params, in_curve, in_position, io_f, offset_row):
    nVert = in_curve.nVertices
    nSegs = nVert if in_curve.closed else (nVert -1)

    assert io_f.shape[0] >= nSegs + offset_row
    assert in_curve.nVertices == in_position.shape[1]

    for i in range(nSegs):
        int_df_seg = integrateDF2OverSegment(in_params, in_position[:,i], in_position[:,(i+1)%nVert], in_curve.restLengths[i])
        io_f[i+offset_row] = math.sqrt(in_params.fit * 0.5) * math.sqrt(int_df_seg)


# void Compute_f(const SParameters* in_params, const SCurve* in_curve, const SVar& in_vars, Eigen::VectorXd& io_f)

def Compute_f(in_params, in_curve, in_vars, io_f):
    nVert = in_curve.nVertices
    nSegs = nVert if in_curve.closed else (nVert -1)
    nAngles = nVert if in_curve.closed else (nVert -2)

    nElems = 2 * nSegs + nAngles

    assert io_f.shape[0] == nElems
    assert in_curve.nVertices == in_vars.pos.shape[1]

    compute_f_elastic(in_params, in_curve, in_vars.pos, io_f, 0)
    compute_f_bending(in_params, in_curve, in_vars.pos, io_f, nSegs)
    compute_f_fit(in_params, in_curve, in_vars.pos, io_f, nSegs+nAngles)

#
# void computeNumericalDerivative_elastic(const SParameters* in_params, const SCurve* in_curve, const Eigen::Matrix2Xd& in_position, double epsilon, Eigen::MatrixXd& io_jacobian, int offset_row)

def computeNumericalDerivative_elastic(in_params, in_curve, in_position, epsilon, io_jacobian, offset_row):
    nSegs = in_curve.nVertices if in_curve.closed else (in_curve.nVertices -1)

    assert io_jacobian.shape[0] >= nSegs + offset_row
    assert io_jacobian.shape[1] == in_curve.nVertices * 2

    dx = [epsilon, 0.0]
    dy = [0.0, epsilon]

	# dJ/dxi, dJ/dyi
    for i in range(nSegs):
		# l_i is a function of x_i, x_{i+1}, y_i and y_{i+1}
        ip = (i+1) % in_curve.nVertices

        xi = in_position[:,i]
        xip = in_position[:,ip]

        diff0 = xip - xi
        fi = math.sqrt(in_params.YA * in_curve.restLengths[i] * 0.5) * (np.linalg.norm(diff0) / in_curve.restLengths[i] - 1)

		# dJ/dxi_i
        xi_dx = xi + dx
        diff1 = xip - xi_dx
        fi_i_dx = math.sqrt(in_params.YA * in_curve.restLengths[i] * 0.5) * (np.linalg.norm(diff1) / in_curve.restLengths[i] - 1)
        io_jacobian[i+offset_row, i] = (fi_i_dx - fi) / epsilon

		# dJ/dyi_i
        xi_dy = xi + dy
        diff2 = xip - xi_dy
        fi_i_dy = math.sqrt(in_params.YA * in_curve.restLengths[i] * 0.5) * (np.linalg.norm(diff2) / in_curve.restLengths[i] - 1)
        io_jacobian[i+offset_row, i+in_curve.nVertices] = (fi_i_dy - fi) / epsilon

		# dJ/dxi_ip
        xip_dx = xip + dx
        diff3 = xip_dx - xi
        fi_ip_dx = math.sqrt(in_params.YA * in_curve.restLengths[i] * 0.5) * (np.linalg.norm(diff3) / in_curve.restLengths[i] - 1)
        io_jacobian[i+offset_row, ip] = (fi_ip_dx - fi) / epsilon

		# dJ/dyi_i
        xip_dy = xip + dy
        diff4 = xip_dy - xi
        fi_ip_dy = math.sqrt(in_params.YA * in_curve.restLengths[i] * 0.5) * (np.linalg.norm(diff4) / in_curve.restLengths[i] - 1)
        io_jacobian[i+offset_row, ip+in_curve.nVertices] = (fi_ip_dy- fi) / epsilon

#
# void computeNumericalDerivative_bending(const SParameters* in_params, const SCurve* in_curve, const Eigen::Matrix2Xd& in_position, double epsilon, Eigen::MatrixXd& io_jacobian, int offset_row)

def computeNumericalDerivative_bending(in_params, in_curve, in_position, epsilon, io_jacobian, offset_row):
    nSegs = in_curve.nVertices if in_curve.closed else (in_curve.nVertices -1)
    nAngles = in_curve.nVertices if in_curve.closed else (in_curve.nVertices-2)

    assert io_jacobian.shape[0] >= nSegs + offset_row
    assert io_jacobian.shape[1] == in_curve.nVertices * 2

    dx = [epsilon, 0.0]
    dy = [0.0, epsilon]

	# dB/dxi, dB/dyi
    for i in range(nAngles):
        if in_curve.closed:
            iim = (i + in_curve.nVertices - 1) % in_curve.nVertices
            ii = i
            iip = (i + 1) % in_curve.nVertices

            restL_m = in_curve.restLengths[(i + in_curve.nVertices - 1) % in_curve.nVertices]
            restL = in_curve.restLengths[i]
        else:
            iim = i
            ii = i + 1
            iip = i + 2

            restL_m = in_curve.restLengths[i]
            restL = in_curve.restLengths[i+1]

        xim = in_position[:,iim]
        xi = in_position[:,ii]
        xip = in_position[:,iip]

        xim_dx = xim + dx
        xim_dy = xim + dy
        xi_dx = xi + dx
        xi_dy = xi + dy
        xip_dx = xip + dx
        xip_dy = xip + dy

        e_prev = xi - xim
        e_next = xip - xi

        e_prev_im_dx = xi - xim_dx
        e_prev_im_dy = xi - xim_dy
        e_prev_i_dx = xi_dx - xim
        e_prev_i_dy = xi_dy - xim

        e_next_i_dx = xip - xi_dx
        e_next_i_dy = xip - xi_dy
        e_next_ip_dx = xip_dx - xi
        e_next_ip_dy = xip_dy - xi

        omega = computeOmega(e_prev, e_next)

        omega_im_dx = computeOmega(e_prev_im_dx, e_next)
        omega_im_dy = computeOmega(e_prev_im_dy, e_next)
        omega_i_dx = computeOmega(e_prev_i_dx, e_next_i_dx)
        omega_i_dy = computeOmega(e_prev_i_dy, e_next_i_dy)
        omega_ip_dx = computeOmega(e_prev, e_next_ip_dx)
        omega_ip_dy = computeOmega(e_prev, e_next_ip_dy)

        # omega_bar will be cancelled out, so omit i
        fi = math.sqrt(in_params.alpha/(restL_m + restL)) * omega
        fi_im_dx = math.sqrt(in_params.alpha/(restL_m + restL)) * omega_im_dx
        fi_im_dy = math.sqrt(in_params.alpha/(restL_m + restL)) * omega_im_dy
        fi_i_dx = math.sqrt(in_params.alpha/(restL_m + restL)) * omega_i_dx
        fi_i_dy = math.sqrt(in_params.alpha/(restL_m + restL)) * omega_i_dy
        fi_ip_dx = math.sqrt(in_params.alpha/(restL_m + restL)) * omega_ip_dx
        fi_ip_dy = math.sqrt(in_params.alpha/(restL_m + restL)) * omega_ip_dy

        io_jacobian[i+offset_row, iim] = (fi_im_dx - fi) / epsilon
        io_jacobian[i+offset_row, iim+in_curve.nVertices] = (fi_im_dy - fi) / epsilon

        io_jacobian[i+offset_row, ii] = (fi_i_dx - fi) / epsilon
        io_jacobian[i+offset_row, ii+in_curve.nVertices] = (fi_i_dy - fi) / epsilon

        io_jacobian[i+offset_row, iip] = (fi_ip_dx - fi) / epsilon
        io_jacobian[i+offset_row, iip+in_curve.nVertices] = (fi_ip_dy - fi) / epsilon

#
# void computeNumericalDerivative_fit(const SParameters* in_params, const SCurve* in_curve, const Eigen::Matrix2Xd& in_position, double epsilon, Eigen::MatrixXd& io_jacobian, int offset_row)

def computeNumericalDerivative_fit(in_params, in_curve, in_position, epsilon, io_jacobian, offset_row):
    nSegs = in_curve.nVertices if in_curve.closed else (in_curve.nVertices -1)

    assert io_jacobian.shape[0] >= nSegs + offset_row
    assert io_jacobian.shape[1] == in_curve.nVertices * 2

    dx = [epsilon, 0.0]
    dy = [0.0, epsilon]

	# dfit/dxi, dfit/dyi
    for i in range(nSegs):
	# l_i is a function of x_i, x_{i+1}, y_i and y_{i+1}
        ip = (i+1) % in_curve.nVertices

        xi = in_position[:,i]
        xip = in_position[:,ip]
        restL = in_curve.restLengths[i]

        fi = math.sqrt(in_params.fit * 0.5) * math.sqrt(integrateDF2OverSegment(in_params, xi, xip, restL))

		# dfit/dxi_i
        xi_dx = xi + dx
        fi_i_dx = math.sqrt(in_params.fit * 0.5) * math.sqrt(integrateDF2OverSegment(in_params, xi_dx, xip, restL))
        io_jacobian[i+offset_row, i] = (fi_i_dx - fi) / epsilon

		# dfit/dyi_i
        xi_dy = xi + dy;
        fi_i_dy = math.sqrt(in_params.fit * 0.5) * math.sqrt(integrateDF2OverSegment(in_params, xi_dy, xip, restL))
        io_jacobian[i+offset_row, i+in_curve.nVertices] = (fi_i_dy - fi) / epsilon

		# dfit/dxi_ip
        xip_dx = xip + dx;
        fi_ip_dx = math.sqrt(in_params.fit * 0.5) * math.sqrt(integrateDF2OverSegment(in_params, xi, xip_dx, restL))
        io_jacobian[i+offset_row, ip] = (fi_ip_dx - fi) / epsilon;

		# dfit/dyi_i
        xip_dy = xip + dy
        fi_ip_dy = math.sqrt(in_params.fit * 0.5) * math.sqrt(integrateDF2OverSegment(in_params, xi, xip_dy, restL))
        io_jacobian[i+offset_row, ip+in_curve.nVertices] = (fi_ip_dy - fi) / epsilon

# void ComputeNumericalDerivative(const SParameters* in_params, const SCurve* in_curve, const SVar& in_vars, double epsilon, Eigen::MatrixXd& io_jacobian)

def ComputeNumericalDerivative(in_params, in_curve, in_vars, epsilon, io_jacobian):
    nSegs = in_curve.nVertices if in_curve.closed else (in_curve.nVertices -1)
    nAngles = in_curve.nVertices if in_curve.closed else (in_curve.nVertices-2)

    computeNumericalDerivative_elastic(in_params, in_curve, in_vars.pos, epsilon, io_jacobian, 0)
    computeNumericalDerivative_bending(in_params, in_curve, in_vars.pos, epsilon, io_jacobian, nSegs)
    computeNumericalDerivative_fit(in_params, in_curve, in_vars.pos, epsilon, io_jacobian, nSegs+nAngles)


# void UpdateRestLength(const Eigen::Matrix2Xd& in_position, SCurve* io_curve)

def UpdateRestLength(in_position, io_curve):
    nSegs = in_curve.nVertices if in_curve.closed else (in_curve.nVertices -1)

    assert in_curve.nVertices == in_position.shape[1]

    for i in range(nSegs):
        ip = (i+1) % in_curve.nVertices
        diff = in_position[:,ip] - in_position[:i]
        io_curve.restLengths[i] = np.linalg.norm(diff)

# void UpdateCurveSubdivision(const SParameters* in_params, SVar& io_initial_vars, SVar& io_vars, SCurve* io_curve, SSolverVars& io_solver_vars)

def UpdateCurveSubdivision(in_params, io_initial_vars, io_vars, io_curve, io_solver_vars):
    nSegs = io_curve.nVertices if io_curve.closed else (io_curve.nVertices -1)
    pos = []
    angles = []
    vids = []

    subdivided = False

    for i in range(nSegs):
        p = SPoint2D()
        p.x[0] = io_vars.pos[:,i][0]
        p.x[1] = io_vars.pos[:,i][1]
        pos.append(p)
        vids.append(io_curve.vertexIDs[i])

        if i!=0 or io_curve.closed:
            angles.append(io_curve.restAngles[i])


        ip = (i+1) % io_curve.nVertices
        diff = io_vars.pos[:,ip] - io_vars.pos[:,i]
        if np.linalg.norm(diff) > in_params.refLength:
            p = SPoint2D()
            p.x[0] = (io_vars.pos[:,ip][0] + io_vars.pos[:,i][0]) * 0.5
            p.x[1] = (io_vars.pos[:,ip][1] + io_vars.pos[:,i][1]) * 0.5

            pos.append(p)
            angles.append(math.pi)
            vids.append(-1)
            subdivided = True

    if not io_curve.closed:
        ilast = io_curve.nVertices-1

        p = SPoint2D()
        p.x[0] = io_vars.pos[:,ilast][0]
        p.x[1] = io_vars.pos[:,ilast][1]
        pos.append(p)
        vids.append(io_curve.vertexIDs[ilast])
    io_curve.nVertices = len(pos)

    nSegs = io_curve.nVertices if io_curve.closed else (io_curve.nVertices -1)
    io_curve.restLengths = np.zeros(nSegs)
    nAngles = io_curve.nVertices if io_curve.closed else (io_curve.nVertices-2)
    io_curve.restAngles = np.zeros(nAngles)
    io_curve.vertexIDs = np.arange(io_curve.nVertices)
    io_vars.pos = np.ndarray((2,io_curve.nVertices))
    io_vars.conf = np.zeros(io_curve.nVertices)
    io_initial_vars.pos = np.ndarray((2,io_curve.nVertices))
    io_initial_vars.conf = np.zeros(io_curve.nVertices)

    nSegs = io_curve.nVertices if io_curve.closed else (io_curve.nVertices -1)
    for i in range(io_curve.nVertices):
        io_vars.pos[:,i][0] = pos[i].x[0]
        io_vars.pos[:,i][1] = pos[i].x[1]
        io_vars.conf[i] = 0.0
        io_curve.vertexIDs[i] = vids[i]

    for i in range(nSegs):
        ip = (i+1) % io_curve.nVertices
        diff = io_vars.pos[:,ip] - io_vars.pos[:,i]
        io_curve.restLengths[i] = np.linalg.norm(diff)
    for i in range(nAngles):
        io_curve.restAngles[i] = angles[i]
    io_initial_vars = io_vars
    initSolverVars(in_params, io_curve, io_initial_vars, io_solver_vars, True)


# bool SecantLMMethodSingleUpdate(const SParameters* in_params, const SCurve* in_curve, const SVar& in_initial_vars, SSolverVars& io_solver_vars, SVar& solution)

def SecantLMMethodSingleUpdate(in_params, in_curve, in_initial_vars, io_solver_vars, solution):
    if io_solver_vars.found or io_solver_vars.k >= in_params.kmax: return True
    io_solver_vars.k += 1
    io_solver_vars.A_muI = np.dot(io_solver_vars.B.T , io_solver_vars.B) + np.dot(io_solver_vars.mu, io_solver_vars.I)

    io_solver_vars.h = np.linalg.solve(io_solver_vars.A_muI, -1*io_solver_vars.g)

    if np.linalg.norm(io_solver_vars.h) <= in_params.epsilon_2 * (np.linalg.norm(io_solver_vars.x.pos) + in_params.epsilon_2) :
        io_solver_vars.found = True

    else:
        for q in range(io_solver_vars.nV):
            io_solver_vars.xnew.pos[0, q] = io_solver_vars.x.pos[0, q] + io_solver_vars.h[q]
            io_solver_vars.xnew.pos[1, q] = io_solver_vars.x.pos[1, q] + io_solver_vars.h[q + io_solver_vars.nV]

    Fnew = 0.5 * ComputeEnergy(in_params, in_curve, io_solver_vars.xnew)
    F = 0.5 * ComputeEnergy(in_params, in_curve, io_solver_vars.x)

    gain_denom = - io_solver_vars.h.dot(np.dot(io_solver_vars.B.transpose(),  io_solver_vars.f)) \
	 	- 0.5 * io_solver_vars.h.dot(np.dot(np.dot(io_solver_vars.B.transpose(), io_solver_vars.B), io_solver_vars.h))
    gain = (F - Fnew) / gain_denom

    if gain > 0:
        io_solver_vars.x = io_solver_vars.xnew

        Compute_f(in_params, in_curve, io_solver_vars.x, io_solver_vars.f)
        ComputeNumericalDerivative(in_params, in_curve, io_solver_vars.x, io_solver_vars.epsilon, io_solver_vars.B)

        io_solver_vars.g = np.dot(io_solver_vars.B.T, io_solver_vars.f)
        io_solver_vars.found = np.amax(np.abs(io_solver_vars.g)) <= in_params.epsilon_1

        print("k:{}, gain: {}, |g|_inf: {}".format(io_solver_vars.k, gain, np.amax(np.abs(io_solver_vars.g))))

        io_solver_vars.mu = io_solver_vars.mu * max(1.0/3.0, 1.0 - (2.0 * gain - 1.0)**3)
        io_solver_vars.nu = 2.0
    else:
        io_solver_vars.mu = io_solver_vars.mu * io_solver_vars.nu
        io_solver_vars.nu = io_solver_vars.nu * 2.0

    if io_solver_vars.found:
        print ("found in {} steps\n".format(io_solver_vars.k))

    solution = io_solver_vars.x
    return io_solver_vars.found or io_solver_vars.k > in_params.kmax

# void ShowFeaturePoints(const SCurve* in_curve, const SVar& solution)

def ShowFeaturePoints(in_curve, solution):
    print("Feature points:")
    for i in range(in_curve.nVertices):
        if in_curve.vertexIDs[i] >= 0:
            print("{}: {}, {}".format(in_curve.vertexIDs[i], solution.pos[0,i], solution.pos[0,i]))

# void SecantLMMethod(const SParameters* in_params, SCurve* in_curve, SVar& in_initial_vars, SSolverVars& io_solver_vars, SVar& solution)

def SecantLMMethod(in_params, in_curve, in_initial_vars, io_solver_vars, solution):
    ShowFeaturePoints(in_curve, solution)
    initSolverVars(in_params, in_curve, in_initial_vars, io_solver_vars)
    count = 0
    while(1):
        print "=============COUNT==============\n",count
        count += 1
    	if SecantLMMethodSingleUpdate(in_params, in_curve,        in_initial_vars, io_solver_vars, solution): break
        UpdateCurveSubdivision(in_params,        in_initial_vars, solution,        in_curve,       io_solver_vars)
    print("found in {} steps".format(io_solver_vars.k))
    solution = io_solver_vars.x

    ShowFeaturePoints(in_curve, solution)

    return in_curve,solution


# void initSolverVars(const SParameters* in_params, const SCurve* in_curve, const SVar& in_initial_vars, SSolverVars& io_vars, bool update)

def initSolverVars(in_params, in_curve, in_initial_vars, io_vars, update=False):
  if not update:
    io_vars.k = 3;
    io_vars.nu = 2.0;
    io_vars.j = 0;
    io_vars.epsilon = 1.0e-7;

  if not update or io_vars.x.pos.shape[1] != in_curve.nVertices:
    io_vars.x = deepcopy(in_initial_vars)
    io_vars.xnew = deepcopy(in_initial_vars)

    nSegs = in_curve.nVertices if in_curve.closed else in_curve - 1
    nAngles = in_curve.nVertices if in_curve.closed else in_curve - 2

    # io_vars is a SSolverVar type
    io_vars.m = nSegs + nAngles + nSegs
    io_vars.n = in_curve.nVertices * 2
    io_vars.nV = in_curve.nVertices

    io_vars.B = np.zeros((io_vars.m, io_vars.n))
    io_vars.g = np.zeros(io_vars.n)
    io_vars.f = np.zeros(io_vars.m)

    io_vars.A_muI = np.zeros((io_vars.n, io_vars.n))
    io_vars.h = np.zeros(io_vars.n)
    io_vars.g = np.zeros(io_vars.n)
    io_vars.I = np.identity(io_vars.n)
  from time import time
  start = time()
  ComputeNumericalDerivative(in_params, in_curve, io_vars.x, io_vars.epsilon, io_vars.B)
  print "Derivative calculated in",time()-start,"seconds"
  Compute_f(in_params, in_curve, io_vars.x, io_vars.f)
  io_vars.g = np.dot(np.transpose(io_vars.B), io_vars.f)

  io_vars.A_muI = np.dot(np.transpose(io_vars.B), io_vars.B)

  io_vars.mu = in_params.tau * np.amax(np.abs(io_vars.A_muI))

  io_vars.found = np.amax(np.abs(io_vars.g)) <= in_params.epsilon_1

  print("|g|_inf: {}\n".format(np.amax(np.abs(io_vars.g))))
