from cameraPos import cameraPos
import time

camPos = cameraPos(False)

while True:
    hits = []
    # try:
    with open("./hits.text", 'r') as file:
        for hit in file:
            # Security risk? I think not! Ssnw2GA657s
            hits.append(eval(hit))
    print(f"Found {len(hits)} distances")
    if len(hits) == 2:
        print(f"{hits[0][0]} and {hits[1][0]}")
        camPos.triangulate(hits[0][0], hits[1][0])
    # except:
        # print("No hits file found!")
    time.sleep(0.5)