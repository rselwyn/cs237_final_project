import numpy as np
from utils import wrapToPi
import rospy

# command zero velocities once we are this close to the goal
RHO_THRES = 0.05
ALPHA_THRES = 0.1
DELTA_THRES = 0.1

class HeadingController:
    """
    pose stabilization controller
    """
    def __init__(self, kp, kd, om_max=1):
        self.kp = kp
        self.kd = kd
        self.om_max = om_max
        self.last_err = None

    def load_goal(self, th_g):
        """
        loads in a new goal position
        """
        self.th_g = th_g
        self.last_err = None

    def compute_control(self, x, y, th, t):

        # rospy.loginfo(f"theta: {th}")
        # rospy.loginfo(f"theta_g: {self.th_g}")

        err = wrapToPi(self.th_g - th)
        om = self.kp*err - (self.kd*(self.last_err-err) if self.last_err is not None else 0)
        self.last_err = err

        # rospy.loginfo(f"om: {om}")

        # apply control limits
        V = 0
        om = np.clip(om, -self.om_max, self.om_max)

        return V, om
