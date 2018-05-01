import numpy as np
from ImageUtil import ImageUtil
from ImagePreprocessor import ImagePreprocessor
from math import sqrt
from GarmentTemplate import initGarmentTemplate
from Registration import SecantLMMethod, initSolverVars
from datatypes import SParameters, SSolverVars, GarmentType
import sys
import skfmm
import cv2
import numpy as np
from collections import namedtuple

def initParams(df):
  YA = 0.01
  alpha = 0.001
  fit = 20000.0
  conf = 100.0
  df = df
  region_gen = namedtuple('region', ['left', 'right', 'top', 'bottom'])
  region = region_gen(-2.0, 2.0, 2.0, -2.0)

  kmax = 10
  epsilon_1 = 1.0e-10
  epsilon_2 = 1.0e-10
  tau = 0.001
  delta = 1.0e-4
  substep_fit = 16
  refLength = 1.0e-1

  return SParameters(YA, alpha, fit, conf, df, region, kmax, epsilon_1, epsilon_2, tau, delta, substep_fit, refLength)

class FoldPlanner:
    # WARNING! MAY NOT BE BEST WAY TO INITIALIZE... MAY LEAD TO ERRORS
    # keyPoint has .id,.x,.y
    # point_list = np.array([]) # vector<keyPoint>* 
    traj_load = [] # vector<np.array> 
    mapped_traj = [] # vector<cv::Point3f> 

    start_pos = np.array([]) # np.array  
    end_pos = np.array([]) # np.array 

    def __init__(self):
        pass
    
    def initParams(self,df):
        YA = 0.01
        alpha = 0.001
        fit = 20000.0
        conf = 100.0
        df = df
        region_gen = namedtuple('region', ['left', 'right', 'top', 'bottom'])
        region = region_gen(-2.0, 2.0, 2.0, -2.0)
        
        kmax = 10
        epsilon_1 = 1.0e-10
        epsilon_2 = 1.0e-10
        tau = 0.001
        delta = 1.0e-4
        substep_fit = 16
        refLength = 1.0e-1
        
        return SParameters(YA, alpha, fit, conf, df, region, kmax, epsilon_1, epsilon_2, tau, delta, substep_fit, refLength)

    
    def MappingTrajectory(self, point_list, garment):
        if garment.PANTS:
            self.PantsPlanner(point_list)
        elif garment.TOWEL:
            self.TowelPlanner(point_list)
        else: # garment == SWEATER:
            self.SweaterPlanner(point_list)
    
    def SweaterPlanner(self, point_list):
        # From 2&3 to 7
        self.LoadTrajectory("maya_trajectory_sweater/trajectory_left_arm_fold.txt")
        # np.array
        start_pos = np.array([(point_list[2].x + point_list[3].x) / 2.0, (point_list[2].y + point_list[3].y) / 2.0])
            
        end_pos = np.array([point_list[7].x, point_list[7].y])
        self.Interpolate3D(start_pos, end_pos)
    
        # From 9&8 to 4
        self.LoadTrajectory("maya_trajectory_sweater/trajectory_right_arm_fold.txt")
        start_pos = np.array([(point_list[8].x + point_list[9].x)/2.0,(point_list[8].y + point_list[9].y)/2.0])
        end_pos = np.array([point_list[4].x, point_list[4].y])
        self.Interpolate3D(start_pos, end_pos)
    
        # Bottom up: 5->1
        self.LoadTrajectory("maya_trajectory_sweater/trajectory_left_arm_bottom_up.txt")
        start_pos = np.array([point_list[5].x, point_list[5].y])
        end_pos   = np.array([point_list[1].x, point_list[1].y])
        self.Interpolate3D(start_pos, end_pos)
    
        # Bottom up: 6->10
        self.LoadTrajectory("maya_trajectory_sweater/trajectory_right_arm_bottom_up.txt")
        start_pos = np.array([point_list[6].x, point_list[6].y])
        end_pos   = np.array([point_list[10].x, point_list[10].y])
        self.Interpolate3D(start_pos, end_pos)
    
        # Write all converted trajectories to file.
        self.WriteMappedTrajToFile()
        
    def PantsPlanner(self, point_list):
    
        # Bottom up: 5->2
        self.LoadTrajectory("maya_trajectory_pants/trajectory_left_arm_bottom_up.txt")
        start_pos = np.array([point_list[5].x, point_list[5].y])
        end_pos   = np.array([point_list[2].x, point_list[2].y])
        self.Interpolate3D(start_pos, end_pos)
        
        # Bottom up: 4->3
        self.LoadTrajectory("maya_trajectory_pants/trajectory_right_arm_bottom_up.txt")
        start_pos = np.array([point_list[4].x, point_list[4].y])
        end_pos   = np.array([point_list[3].x, point_list[3].y])
        self.Interpolate3D(start_pos, end_pos)
        
        # From 1&2 to (3+4)/2&3
        self.LoadTrajectory("maya_trajectory_pants/trajectory_left_arm_fold.txt")
        start_pos = np.array([(point_list[1].x + point_list[2].x)/2.0,(point_list[1].y + point_list[2].y)/2.0])
        end_pos   = np.array([((point_list[3].x + point_list[4].x)/2.0 + point_list[3].x)/2, ((point_list[3].y + point_list[4].y)/2.0 + point_list[3].y)/2.0])
        self.Interpolate3D(start_pos, end_pos)
    
        # Write all converted trajectories to file.
        self.WriteMappedTrajToFile()
    
    
    def TowelPlanner(self, point_list):
    
        # Bottom up 2->3
        self.LoadTrajectory("maya_trajectory_towel/trajectory_right_arm_bottom_up.txt")
        start_pos = np.array([point_list[2].x, point_list[2].y])
        end_pos   = np.array([point_list[3].x, point_list[3].y])
        self.Interpolate3D(start_pos, end_pos)
    
        # Bottom up 0->1
        self.LoadTrajectory("maya_trajectory_towel/trajectory_left_arm_bottom_up.txt")
        start_pos = np.array([point_list[1].x, point_list[1].y])
        end_pos   = np.array([point_list[0].x, point_list[0].y])
        self.Interpolate3D(start_pos, end_pos)
    
        # Left arm fold
        self.LoadTrajectory("maya_trajectory_towel/trajectory_left_arm_fold.txt")
        start_pos = np.array([((point_list[2].x + point_list[3].x)/2.0 + point_list[3].x)/2.0, ((point_list[2].y + point_list[3].y)/2.0 + point_list[3].y)/2.0])
        end_pos   = np.array([((point_list[0].x + point_list[1].x)/2.0 + point_list[0].x)/2.0, ((point_list[0].y + point_list[1].y)/2.0 + point_list[0].y)/2.0])
        self.Interpolate3D(start_pos, end_pos)
    
        # Write all converted trajectories to file.
        self.WriteMappedTrajToFile()
    
    
    def Interpolate3D(self, startPos, endPos):
    
        xOffset = endPos[0] - startPos[0]
        yOffset = endPos[1] - startPos[1]
        dist = sqrt((startPos[0] - endPos[0])*(startPos[0] - endPos[0]) + (startPos[1] - endPos[1])*(startPos[1] - endPos[1]))
    
        for i in range(len(FoldPlanner.traj_load)):
        
            print("Loaded trajectory {} {}\n".format(FoldPlanner.traj_load[i][0], FoldPlanner.traj_load[i][1]))
            x = startPos[0] + FoldPlanner.traj_load[i][0] * xOffset 
            y = startPos[1] + FoldPlanner.traj_load[i][0] * yOffset
            z = FoldPlanner.traj_load[i][1] * dist
            FoldPlanner.mapped_traj.append(np.array([x, y, z]))
        
    
        # Add a mark for each trajectory.
        FoldPlanner.mapped_traj.append(np.array([-1.0,-1.0,-1.0]))
    
    
    def LoadTrajectory(self, fileName):
        # Clear previous loaded trajectory.
        FoldPlanner.traj_load = []
        # Read trajectory
        with open(fileName, "r") as f:
            for line in f:
                f1,f2 = line.split(" ")
                f1,f2 = float(f1), float(f2)
                #print(FoldPlanner.traj_load, f1, f2)
                FoldPlanner.traj_load.append(np.array([f1, f2]))

    
    def WriteMappedTrajToFile(self):
        with open("mapped_keypoints.txt", "w") as fp: 
            for i in FoldPlanner.mapped_traj:
                if i[0] == -1.0:
                    fp.write("\n")
                    continue
                fp.write("{} {} {} \n".format(i[0], i[1], i[2]))
        
        for i in FoldPlanner.mapped_traj:
            pass

    def planFold(self, img_file):

        debug = False
        imagePreprocessor = ImagePreprocessor()
        mask, garmentTypeStr = imagePreprocessor.generateGarmentMaskAndType(filename, debug)

        if garmentTypeStr[0] =='R':
            print "Please rotate the", garmentTypeStr[1:]
            sys.exit()
        elif garmentTypeStr == 'SWEATER':
            garmentType = GarmentType(True, False, False)
        elif garmentTypeStr == 'PANTS':
            garmentType = GarmentType(False, True, False)
        elif garmentTypeStr == 'TOWEL':
            garmentType = GarmentType(False, False, True)

        df = skfmm.distance(mask)
        params = self.initParams(df)
        curve, vars = initGarmentTemplate(garmentType) 
        initialVars = vars
        solverVars = SSolverVars()
        initSolverVars(params, curve, initialVars, solverVars)
        cuve, vars = SecantLMMethod(params, curve, initialVars, solverVars, vars)
        pointList = imagePreprocessor.rescalePoints(curve, vars)
        self.MappingTrajectory(pointList, garmentType)

        return FoldPlanner.mapped_traj, garmentTypeStr
