import os
import csv

PREFIX = '[PIDPATH] '

class PIDCoords:
    XYCoords = dict()
    minX = 0
    maxX = 0

    def __init__(self, cleanedCSV='./pidpathData/output_clean.csv', resolution='mm'):
        self.svgFile = cleanedCSV
        if not os.path.exists(cleanedCSV):
            raise ValueError(f'{PREFIX}Cleaned csv file does not exist')

        if resolution not in ['mm', 'm', 'cm']:
            raise ValueError(f"{PREFIX}Unsupported resolution! (choose m, cm or mm)")

        # setting the conversions for mm to other format (source is in mm)
        if resolution == 'mm':
            conversion = self.keep_mm
            stepSize = 1
        elif resolution == 'cm':
            conversion = self.convert_mm_cm
            stepSize = 1/10
        else:
            conversion = self.convert_mm_m
            stepSize = 1/1000

        with open(os.path.join(cleanedCSV), 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # skip first line( contains headers)
            next(reader)

            for x, y in reader:
                self.XYCoords[conversion(x)] = conversion(y)

        print(f"{PREFIX}Loaded xy coordinates, validating...")

        # nr. of decimals we can round the validation to (to prevent float math errors (4.199 != 4.2))
        decimalsForResolution = dict({'mm': 0, 'cm': 1, 'm': 3})
        lastRead = next(iter(self.XYCoords))
        for i, x in enumerate(self.XYCoords):
            # first item, skip
            if i == 0:
                self.minX = x
                continue
            # check if we have a sequential run from the start to end (no missing x values)
            if x != round(lastRead + stepSize, decimalsForResolution[resolution]):
                raise ValueError(f"{PREFIX}{x} is not {stepSize} more than previous {lastRead}! Missing X coordinate!")
            lastRead = x

            if i == (len(self.XYCoords) - 1):
                self.maxX = x

        print(f"{PREFIX}Loaded and validated PIDPATH!")


    def getMaxX(self):
        return self.maxX

    def getMinX(self):
        return self.minX

    def getY(self, x):
        try:
            return self.XYCoords[x]
        except:
            raise ValueError(f"{PREFIX}Y not Found for {x} (limits: X={self.minX} and X={self.maxX})")

    # conversion functions used in setup
    def convert_mm_m(self, input):
        return round((int(input)/1000), 3)

    def convert_mm_cm(self, input):
        return round((int(input)/10), 1)

    def keep_mm(self, input):
        return int(input)

