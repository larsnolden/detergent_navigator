# PIDPATH

This is a package for TCS M8C Track 5, RTOS
This package takes an svg element with a bezier curve and converts that into a csv file to generate a set of XY coordinates for it. It is able to add an offset to the start of the bezier curve to change the origin.

## Installing
You should be able to install this package from git through pip [See here how](https://adamj.eu/tech/2019/03/11/pip-install-from-a-git-repository/)

## Example code:
```py
from PIDPATH.generator import generateFile
from PIDPATH.main import PIDCoords

# generates a csv file with raw and cleaned coordinates inside /pidpathData by default
generateFile('./mySVG.svg')

# resolutions (mm(default), cm, m), has the optional paramters xOffset and yOffset and filename for cleaned svg
pid = PIDCoords(resolution='mm')

# get limits on x axis
pid.getMaxX()
pid.getMinX()

# get y coordinate of a given x
# format of x depends on setup of pid, (mm = 1, cm = 5.4, m = 2.034)
# keep the number of decimals as above!
pid.getY(myX)

```

