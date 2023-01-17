rotate = lambda r, P: (cos(r)*P[0]-sin(r)*P[1], sin(r)*P[0]+cos(r)*P[1]
angleof = lambda P: atan2(P[1], P[0])
solve = lambda r, P, B: angleof(rotate(r, (B[0]-P[0], B[1]-P[1])))
# - r: the local angle between the robot and the botle #TODO invert or not?
# - P: the global position of the robot
# - B: the global position of the botle