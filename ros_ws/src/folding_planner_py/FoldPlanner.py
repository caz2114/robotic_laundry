import numpy as np
from ImageUtil import ImageUtil
from ImagePreprocesser import ImagePreprocesser
from math import sqrt

class FoldPlanner:
    # WARNING! MAY NOT BE BEST WAY TO INITIALIZE... MAY LEAD TO ERRORS
    # keyPoint has .id,.x,.y
    point_list = np.array([]) # vector<keyPoint>* 
    traj_load = np.array([]) # vector<np.array> 
    mapped_traj = np.array([]) # vector<cv::Point3f> 

    start_pos = np.array([]) # np.array  
    end_pos = np.array([]) # np.array 

    def __init__(self):
        pass
    
    def MappingTrajectory(self,point_list,garment):
        if garment == PANTS:
            self.PantsPlanner(point_list)
        elif garment == TOWEL:
            self.TowelPlanner(point_list)
        else: # garment == SWEATER:
            self.SweaterPlanner(point_list)
    
    def SweaterPlanner(self,point_list):
        # From 2&3 to 7
        self.LoadTrajectory("maya_trajectory_sweater/trajectory_left_arm_fold.txt")
        # np.array
        start_pos = np.array((point_list[2].x + point_list[3].x) / 2.0, (point_list[2].y + point_list[3].y) / 2.0)
            
        end_pos = np.array(point_list[7], point_list[7])
        self.Interpolate3D(start_pos, end_pos)
    
        # From 9&8 to 4
        self.LoadTrajectory("maya_trajectory_sweater/trajectory_right_arm_fold.txt")
        start_pos = np.array((point_list[8] + point_list[9])/2.0,(point_list[8] + point_list[9])/2.0)
        end_pos = np.array(point_list[4], point_list[4])
        self.Interpolate3D(start_pos, end_pos)
    
        # Bottom up: 5->1
        self.LoadTrajectory("maya_trajectory_sweater/trajectory_left_arm_bottom_up.txt")
        start_pos = np.array(point_list[5], point_list[5])
        end_pos   = np.array(point_list[1], point_list[1])
        self.Interpolate3D(start_pos, end_pos)
    
        # Bottom up: 6->10
        self.LoadTrajectory("maya_trajectory_sweater/trajectory_right_arm_bottom_up.txt")
        start_pos = np.array(point_list[6], point_list[6])
        end_pos   = np.array(point_list[10], point_list[10])
        self.Interpolate3D(start_pos, end_pos)
    
        # Write all converted trajectories to file.
        self.WriteMappedTrajToFile()
        
    def PantsPlanner(point_list):
    
        # Bottom up: 5->2
        self.LoadTrajectory("maya_trajectory_pants/trajectory_left_arm_bottom_up.txt")
        start_pos = np.array(point_list[5], point_list[5])
        end_pos   = np.array(point_list[2], point_list[2])
        self.Interpolate3D(start_pos, end_pos)
        
        # Bottom up: 4->3
        self.LoadTrajectory("maya_trajectory_pants/trajectory_right_arm_bottom_up.txt")
        start_pos = np.array(point_list[4], point_list[4])
        end_pos   = np.array(point_list[3], point_list[3])
        self.Interpolate3D(start_pos, end_pos)
        
        # From 1&2 to (3+4)/2&3
        self.LoadTrajectory("maya_trajectory_pants/trajectory_left_arm_fold.txt")
        start_pos = np.array((point_list[1] + point_list[2])/2.0,(point_list[1] + point_list[2])/2.0)
        end_pos   = np.array(((point_list[3] + point_list[4])/2.0 + point_list[3])/2, ((point_list[3] + point_list[4])/2.0 + point_list[3])/2.0)
        self.Interpolate3D(start_pos, end_pos)
    
        # Write all converted trajectories to file.
        self.WriteMappedTrajToFile()
    
    
    def TowelPlanner(point_list):
    
        # Bottom up 2->3
        self.LoadTrajectory("maya_trajectory_towel/trajectory_right_arm_bottom_up.txt")
        start_pos = np.array(point_list[2], point_list[2])
        end_pos   = np.array(point_list[3], point_list[3])
        self.Interpolate3D(start_pos, end_pos)
    
        # Bottom up 0->1
        self.LoadTrajectory("maya_trajectory_towel/trajectory_left_arm_bottom_up.txt")
        start_pos = np.array(point_list[1], point_list[1])
        end_pos   = np.array(point_list[0], point_list[0])
        self.Interpolate3D(start_pos, end_pos)
    
        # Left arm fold
        self.LoadTrajectory("maya_trajectory_towel/trajectory_left_arm_fold.txt")
        start_pos = np.array(((point_list[2] + point_list[3])/2.0 + point_list[3])/2.0, ((point_list[2] + point_list[3])/2.0 + point_list[3])/2.0)
        end_pos   = np.array(((point_list[0] + point_list[1])/2.0 + point_list[0])/2.0, ((point_list[0] + point_list[1])/2.0 + point_list[0])/2.0)
        self.Interpolate3D(start_pos, end_pos)
    
        # Write all converted trajectories to file.
        self.WriteMappedTrajToFile()
    
    
    def Interpolate3D(startPos, endPos):
    
        xOffset = endPos[0] - startPos[0]
        yOffset = endPos[1] - startPos[1]
        dist = sqrt((startPos[0] - endPos[0])*(startPos[0] - endPos[0]) + (startPos[1] - endPos[1])*(startPos[1] - endPos[1]))
    
        for i in range(len(traj_load)):
        
            printf("Loaded trajectory %f %f \n", traj_load[i][0], traj_load[i][1])
            x = startPos[0] + traj_load[i][0] * xOffset 
            y = startPos[1] + traj_load[i][0] * yOffset
            z = traj_load[i][1] * dist
            mapped_traj = np.append(mapped_traj,np.array(x, y, z))
        
    
        # Add a mark for each trajectory.
        mapped_traj = np.append(mapped_traj,np.array(-1.0,-1.0,-1.0))
    
    
    def LoadTrajectory(fileName):
        # Clear previous loaded trajectory.
        traj_load = np.array([])
        # Read trajectory
        with open(fileName, "r") as f:
            for line in f:
                f1,f2 = line.split(" ")
                f1,f2 = float(f1),float(f2)
                traj_load = np.append(traj_load,np.array(f1, f2))
    
    def WriteMappedTrajToFile():
        # Write to file.
        with open("mapped_keypoints.txt", "w") as fp: 
            for i in mapped_traj:
                if i[0] == -1.0:
                    fp.write("\n")
                    continue
                fp.write("{} {} {} \n".format(i[0], i[1], i[2]))
        
        
        # printf("xOffset = %f \n", xOffset)
        # printf("yOffset = %f \n", yOffset)
        # printf("dist = %f \n", dist)
        # printf("start pos: %f, %f \n", startPos[0], startPos[1])
        # printf("end pos: %f, %f \n", endPos[0], endPos[1])
    
        print "The size is {}".format(len(mapped_traj))
        print "I am after."
        for i in mapped_traj:
            print "Mapped trajectory points: {}  {}  {}".format(i[0], i[1], i[2])