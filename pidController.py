from PIDPATH.main import PIDCoords
from simple_pid import PID

class PidController:
    Kp = 1
    Ki = 0.1
    Kd = 0.05


    def __init__(self):
        self.idealPath = PIDCoords(resolution='cm')
        self.pid = PID(self.Kp, self.Ki, self.Kd, setpoint=1)
        self.pid.output_limits = (-255, 255)

        print("Pid controller setup done!")

    def getSteer(self, xPos, yPos):
        yRef = self.idaelPath.getY(xPos)
        self.pid.setpoint = yRef
        steer = int(self.pid(yPos))
        return steer