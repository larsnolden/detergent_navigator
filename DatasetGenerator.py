# original file, replaced with pidpath module!
# import csv
# import math
# from svgelements import *
#
# print("PIDPATH generator started...")
#
# pathID = -1;
# STARTX = 50
# STARTY = 150
#
# SVG_FILE = 'PID_PATH.svg'
#
# svg = SVG.parse(SVG_FILE)
# path = None
#
# for svgElement in svg.elements():
#     if isinstance(svgElement, Group):
#         if len(svgElement) == 1:
#             if isinstance(svgElement[0], Path):
#                 if path is None:
#                     path = svgElement[0]
#                 if svgElement[0].length() > path.length():
#                     path = svgElement[0]
#
# if path is None:
#     print("Path not found!")
#     exit()
#
# print("Found PIDPATH!")
#
# f = open('./output_raw.csv', 'w')
# writer = csv.writer(f)
# writer.writerow(['x', 'y', 't'])
#
# print("Calculating raw x and y coordinated")
# for el in path:
#     if el.length() == 0:
#         continue
#     # offsetting back to 0 (X0) position and invert Y axis (x0, y0 is topleft in svg)
#     el = el * f"translate({-STARTX}, {-STARTY})" * "scale(1, -1)"
#     length = math.ceil(el.length()*100)
#     # pixels is in centimeters, (150 = 150cm), multiply with 100 to change to 0.01 cm resolution (oversampling)
#     for i in range(length+1):
#         pos = el.point(i/length)
#         writer.writerow([
#             pos.x,
#             pos.y,
#             i/length
#         ])
#
# f.close()
#
# print("Downsampling raw x and y coordinates...")
#
# cleanXY = dict()
#
# with open('output_raw.csv', 'r', newline='') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     next(reader)
#
#     for x, y, t in reader:
#         # x is in cm,mm. go to millimeters
#         cleanXY[int(round(float(x)*10, 0))] = int(round(float(y)*10, 0))
#
# print("Downsampled raw x and y coordinates, validating...")
#
# lastRead = next(iter(cleanXY))
# for x in cleanXY:
#     # first item, skip
#     if x == lastRead:
#         continue
#     # check if we have a sequential run from the start to end (no missing x values)
#     if x != lastRead+1:
#         print(f"{x} is not 1 more than previous {lastRead}! Missing X coordinate!")
#         exit()
#     lastRead = x
#
# print("Saving downsampled coordinates")
# f2 = open('./output_clean.csv', 'w')
# cleanwriter = csv.writer(f2)
# cleanwriter.writerow(['x', 'y'])
# for x in cleanXY:
#     cleanwriter.writerow([
#         x,
#         cleanXY[x]
#     ])
# f2.close()
#
# print("Saved downsampled coordinates to ./output_clean.csv")