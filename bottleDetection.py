import cv2
import numpy as np
import os
import math

# Load image
cap = cv2.VideoCapture(0)
kernel_size = (5,5)

print(cap.get(3), ", ", cap.get(4))

while True:   

    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)
    # Apply Gaussian Blur
    frame = cv2.GaussianBlur(frame, kernel_size, 0)
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # good calibrated values!
    # Define range of green color in HSV
    # lower_green = (42,17,85)
    # upper_green = (77, 255, 255)

    # # Define range of green color in HSV
    lower_green = (43,21,81)
    upper_green = (81, 255, 255)

    # Define range of red color in HSV
    lower_red = (27, 0, 0)
    upper_red = (133, 182, 255)

    # # designlab calibrated
    # # Define range of green color in HSV
    # lower_green = (81, 82, 113)
    # upper_green = (102, 255, 255)

    # # Define range of red color in HSV
    # lower_red = (69, 61, 0)
    # upper_red = (96, 157, 255)
    
    # Create masks for green and red colors
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    red_mask = cv2.inRange(cv2.bitwise_not(hsv), lower_red, upper_red)

    # Find contours of the object
    # contours, _ = cv2.findContours(green_mask + red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find bounding box around the object

    hits = []
    
    for green_cnt in green_contours:
        x, y, w, h = cv2.boundingRect(green_cnt)
        # found_bottle = False
        lX, lY, lW, lH, = (0, 0, 0, 0)
        for red_cnt in red_contours:
            x2, y2, w2, h2 = cv2.boundingRect(red_cnt)
            if x2 > x and x2 + w2 < x + w and y2 < y and y-0.3*h < y2:
                # check for the largest blue square
                if(w2 * h2 > lH * lW):
                    lX = x2
                    lY = y2
                    lW = w2
                    lH = h2
        if lX != 0:                    
            cv2.rectangle(frame, (lX, lY), (lX + lW, lY + lH), (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # found_bottle = True
            distance = 823.055764 * math.exp(-0.033767 * h) + 148.197165 * math.exp(-0.004140 * h)
            centerPos = lX + lW/2
            # y = -4E-06x2 - 0.105x + 34.131
            angle = -0.000004 * (centerPos**2) - 0.105 * centerPos + 34.131
            angle = angle * -1
            hits.append((distance, angle))
            print(f"Found bottle with distance: {distance} and angle: {angle}")

        # if found_bottle:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # for cnt in green_contours:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    hits.sort()
    with open("hits.temp", 'w') as file:
        for hit in hits:
            file.write(f"{hit}\n")
            
    os.system("mv hits.temp hits.text")
    
    cv2.imshow("image", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()