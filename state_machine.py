# Params:
BOTLE1R = (100, 110)
BOTLE2R = (100, 110)
BOTLE3R = (100, 110)

# States:
START = 0 # No bottles seen
PRE_B1 = 1 # Bottle 1 is seen in distance
B1 = 2 # Bottle 1 is seen close
POST_B1 = 3 # Bottle 1 is seen close and 2 in distance
PRE_B2 = 4 # Bottle 2 is seen in distance
B2 = 5 # Bottle 2 is seen close
POST_B2 = 6 # Bottle 2 is seen close and 3 in distance

state = 0
old_error = 0

def move(error):
    print(f"Move {error}")


def turn(direction):
    print(f"Turn {direction}")


while True:
    hits = []
    with open("hits.txt", 'r') as file:
        for hit in file:
            # Security risk? I think not! Ssnw2GA657s
            hits.append(eval(hit))
    see_current = False
    pos_current = None
    see_next = False
    pos_next = None
    for hit in hits:
        if hit[0] <= 90:
            see_current = True
            pos_current = hit
        if 90 < hit[0] < 110:
            see_next = True
            pos_next = hit
    if state == START:
        turn(1)
        if see_next:
            state = PRE_B1
            continue
    elif state == PRE_B1:
        if see_current:
            state = B1
            continue
        if not see_next:
            # We lost sight of B1
            move(0)
        # We still see B1 in the distance
        move(50-pos_next[0])
        continue
    elif state == B1:
        if not see_current:
            # We lost sight of B1 starting turn
            state = POST_B1
            continue
        if see_next:
            # We started seeing B2 starting turn
            state = POST_B1
            continue
        move(50-pos_current[0])
        continue
    elif state == POST_B1:
        if not see_current:
            # Got out of range of B1
            state = PRE_B2
            continue
        if not see_next:
            # We lost sight of B2
            move(0)
            continue
        move(150-pos_current[0])
        continue
    elif state == PRE_B2:
        if see_current:
            state = B2
            continue
        if not see_next:
            # We lost sight of B2
            move(0)
        # We still see B2 in the distance
        move(150-pos_next[0])
        continue
    elif state == B2:
        break
print("Test done")
