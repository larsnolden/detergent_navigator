# importing the easy_trilateration module
from easy_trilateration.model import Circle, Point 
from easy_trilateration.least_squares import easy_least_squares  
from easy_trilateration.graph import create_circle, draw
import math


class cameraPos:
    def __init__(self, debug=False):
        self.debug = debug
        print("camera Positioning started!")

    # DECLARING FUNCTIONS
    def get_intersections(self, x0, y0, r0, x1, y1, r1):
        # circle 1: (x0, y0), radius r0
        # circle 2: (x1, y1), radius r1

        d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
        
        # non intersecting
        if d > r0 + r1 :
            return None
        # One circle within other
        if d < abs(r0-r1):
            return None
        # coincident circles
        if d == 0 and r0 == r1:
            return None
        else:
            a=(r0**2-r1**2+d**2)/(2*d)
            h=math.sqrt(r0**2-a**2)
            x2=x0+a*(x1-x0)/d   
            y2=y0+a*(y1-y0)/d   
            x3=x2+h*(y1-y0)/d     
            y3=y2-h*(x1-x0)/d 

            x4=x2-h*(y1-y0)/d
            y4=y2+h*(x1-x0)/d
            
            return (x3, y3, x4, y4)

    def triangulate(self, distB1, distB2):
        # 10,0 is start of end bottle, 100, 50 is position of the second bottle
        arr = [Circle(10, 0, distB1), Circle(100, 50, distB2)]
        result, meta = easy_least_squares(arr)  
        
        if self.debug: 
            create_circle(result, target=True) 
            draw(arr)

        # (x3,y3) and (x4,y4) are the two intersection points, choosing the one closest to our previous coordinates
        if self.get_intersections(10, 0, distB1, 100, 50, distB2) is not None:
            x3, y3, x4, y4 = self.get_intersections(10, 0, distB1, 100, 50, distB2)
            # determining closest position
            # if math.sqrt((x3 - previous_robot_x)**2 + (y3 - previous_robot_y)**2) < math.sqrt((x4 - previous_robot_x)**2 + (y4 - previous_robot_y)**2):
            #     robot_x = x3
            #     robot_y = y3
            # else:
            #     robot_x = x4
            #     robot_y = y4

            print(f"Positions: x:{x3} y:{y3} and x:{x4} y:{y4}")
            print(f"Trilateration circle position: x:{result.center.x} y:{result.center.y} and radius: r:{result.radius}")

    # # MAIN CODE
    # if __name__ == '__main__':
    #     # arr = [Circle(0, 0, first_bottle_distance), Circle(-50, 100, second_bottle_distance), Circle(50, 200, thrid_bottle_distance)]  
    #     # 10,0 is start of end bottle, 100, 50 is position of the second bottle
    #     arr = [Circle(10, 0, first_bottle_distance), Circle(100, 50, second_bottle_distance)]  
    #     result, meta = easy_least_squares(arr)  
    #     create_circle(result, target=True) 

    #     draw(arr) #printing a fancy graph

    #     if abs(result.radius) < 10:
    #         # position estimation worked reliably, output position
    #         robot_x = result.center.x
    #         robot_y = result.center.y
    #         method_details = 'Trilateration, accuracy: ' + str(abs(result.radius))
    #     else:
    #         # estimation is bad, or not three circles were visible. Let's estimate it by calculating the intersection of the two circles.
        
    #         if get_intersections(0,0, first_bottle_distance, -50, 100, second_bottle_distance): 
    #             #debug; hardcoding these coordinates right now
    #             robot_x = 0
    #             robot_y = 100
    #             previous_robot_x = robot_x
    #             previous_robot_y = robot_y
    #             x3, y3, x4, y4 = get_intersections(0,0, first_bottle_distance, -50, 100, second_bottle_distance)
    #             # (x3,y3) and (x4,y4) are the two intersection points, choosing the one closest to our previous coordinates
    #             if math.sqrt((x3 - previous_robot_x)**2 + (y3 - previous_robot_y)**2) < math.sqrt((x4 - previous_robot_x)**2 + (y4 - previous_robot_y)**2):
    #                 robot_x = x3
    #                 robot_y = y3
    #             else:
    #                 robot_x = x4
    #                 robot_y = y4
    #             method_details = "Intersection of two circles, because accuracy of other method was too low: " + str(abs(result.radius))

    #         else: 
    #             # no intersection result, use another method to estimate position
    #             method_details = "Fail."


    #     # CONSOLE OUTPUT
    #     print("x: ", robot_x)
    #     print("y: ", robot_y)
    #     print("Method: ", method_details)