from PIDPATH.main import PIDCoords
from simple_pid import PID
import math
import numpy as np

class PidController:
    # #straight
    # KPstraight = 2.5
    # KIstraight = 0.1
    # KDstraight = 12
    
    # #corner
    # KPcorner = 2.5
    # KIcorner = 0.1
    # KDcorner = 12

     #straight
    KPstraight = 2.5
    KIstraight = 0.1
    KDstraight = 12
    
    #corner
    KPcorner = 2.5
    KIcorner = 0.1
    KDcorner = 12


    def __init__(self):
        self.pidStraight = PID(self.KPstraight, self.KIstraight, self.KDstraight)
        self.pidCorner = PID(self.KPcorner, self.KIcorner, self.KDcorner)
        self.idealPath = PIDCoords(cleanedCSV="./pidpathDataL3/output_clean.csv", resolution='cm')
        self.pidCorner.output_limits = (-255, 255)
        self.pidStraight.output_limits = (-255, 255)


        print("Pid controller setup done!")

    # Steer strength R[-255, 255]
    def getSteer(self, position):
        shiftX = 0
        xPos = round(position["x"]-shiftX, 1)
        print("xPos: ", xPos)
        if xPos > 340: return 0
        if xPos < -34: raise ValueError("Ran out of coordinates")

        yRef = self.idealPath.getY(xPos)
        distance_to_ideal = self.getClosestPointY(xPos, position["y"]) 
        
        print("y: ", position["y"], "yRef: ", yRef)
        self.pidStraight.setpoint = 0
        steer = int(self.pidStraight(distance_to_ideal))
        
        # if(xPos > 160 and xPos < 200):
        #     self.pidCorner.setpoint = yRef
        #     steer = int(self.pidCorner(position["y"]))
        #     print("corner")
        # elif (xPos > 75 and xPos < 112):
        #     self.pidCorner.setpoint = yRef
        #     steer = int(self.pidCorner(position["y"]))
        #     print("corner")
        # else:
        #     self.pidStraight.setpoint = yRef
        #     steer = int(self.pidStraight(position["y"]))
        #     print("straight")
        
        return steer

    def getClosestPointY(self, xRef, yRef):
        maxX = self.idealPath.getMaxX()
        xValues = np.arange(0, round(maxX, 0), 1)
        # xValues = [round(maxX ,0)]
        # yValues = []
        smallest_distance_found = 10e10
        sign = 1

        for xPoint in xValues:
            yPoint = self.idealPath.getY(round(xPoint, 1))
            distance = math.sqrt((xPoint - xRef)**2 + (yPoint - yRef)**2)
            if(distance < smallest_distance_found):
                smallest_distance_found = distance
                if(yRef < yPoint):
                    sign = -1
                else:
                    sign = 1

        
        return smallest_distance_found * sign
        

    def getXY(self):
        return self.idealPath.getAll()