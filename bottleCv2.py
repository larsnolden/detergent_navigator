import cv2
import numpy as np
import os

# Load image
cap = cv2.VideoCapture(0)

while True:   

    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)
    # Apply Gaussian Blur
    frame = cv2.GaussianBlur(frame, kernel_size, 0)
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green = (43,21,81)
    upper_green = (81, 255, 255)

    # Define range of red color in HSV
    lower_red = (27, 0, 0)
    upper_red = (133, 182, 255)

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
        found_bottle = False
        for red_cnt in red_contours:
            x2, y2, w2, h2 = cv2.boundingRect(red_cnt)
            if x2 > x and x2 + w2 < x + w and y2 < y and y-0.3*h < y2:
                cv2.rectangle(res, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)
                found_bottle = True
                hits.append((h, x + w / 2))
                break

        if found_bottle:
            cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)

    for cnt in green_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    with open("hits.temp", 'w') as file:
        for hit in hits:
            file.write(f"{hit}\n")
            
    os.system("mv hits.temp hits.text")
    
    cv2.imshow("image", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
