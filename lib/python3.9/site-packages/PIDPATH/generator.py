import csv
import math
from svgelements import *
import os

PREFIX = '[PIDPATH] '

def generateFile(svgFilename, outputDir='./pidpathData', xOffset=50, yOffset=150):
    if not os.path.exists(svgFilename):
        raise ValueError(f'{PREFIX}SVG file does not exist')

    try:
        os.mkdir(outputDir)
    except OSError as error:
        print(error)

    filePath = os.path.join('./', outputDir)

    print(f"{PREFIX}PIDPATH generator started...")

    pathID = -1;

    svg = SVG.parse(svgFilename)
    pidpath = None

    for svgElement in svg.elements():
        if isinstance(svgElement, Group):
            if len(svgElement) == 1:
                if isinstance(svgElement[0], Path):
                    if pidpath is None:
                        pidpath = svgElement[0]
                    if svgElement[0].length() > pidpath.length():
                        pidpath = svgElement[0]

    if pidpath is None:
        raise ValueError(f'{PREFIX}SVG pidpath not found!')

    print(f"{PREFIX}Found PIDPATH!")

    f = open(os.path.join(filePath, "output_raw.csv"), 'w')
    writer = csv.writer(f)
    writer.writerow(['x', 'y', 't'])

    print(f"{PREFIX}Calculating raw x and y coordinated")
    for el in pidpath:
        if el.length() == 0:
            continue
        # offsetting back to 0 (X0) position and invert Y axis (x0, y0 is topleft in svg)
        el = el * f"translate({-xOffset}, {-yOffset})" * "scale(1, -1)"
        length = math.ceil(el.length()*100)
        # pixels is in centimeters, (150 = 150cm), multiply with 100 to change to 0.01 cm resolution (oversampling)
        for i in range(length+1):
            pos = el.point(i/length)
            writer.writerow([
                pos.x,
                pos.y,
                i/length
            ])

    f.close()

    print(f"{PREFIX}Downsampling raw x and y coordinates...")

    cleanXY = dict()


    with open(os.path.join(filePath, "output_raw.csv"), 'r', newline='') as csvfile:
        # skip first line( contains headers)
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)

        for x, y, t in reader:
            # x is in cm,mm. go to millimeters
            cleanXY[int(round(float(x)*10, 0))] = int(round(float(y)*10, 0))

    print(f"{PREFIX}Downsampled raw x and y coordinates, validating...")

    lastRead = next(iter(cleanXY))
    for x in cleanXY:
        # first item, skip
        if x == lastRead:
            continue
        # check if we have a sequential run from the start to end (no missing x values)
        if x != lastRead+1:
            print(f"{x} is not 1 more than previous {lastRead}! Missing X coordinate!")
            exit()
        lastRead = x

    print(f"{PREFIX}Saving downsampled coordinates")
    cleanFilePath = os.path.join(filePath, "output_clean.csv")
    f2 = open(cleanFilePath, 'w')
    cleanwriter = csv.writer(f2)
    cleanwriter.writerow(['x', 'y'])
    for x in cleanXY:
        cleanwriter.writerow([
            x,
            cleanXY[x]
        ])
    f2.close()

    print(f"{PREFIX}Saved downsampled coordinates to {cleanFilePath}")