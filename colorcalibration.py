# Guid:
# press (left mouse button) to add a pixel to the bound
# press (z) to remove the previously added pixel from the bound
# press (q) to quit

import cv2
import numpy as np

imcap = cv2.VideoCapture(0)

mouse_x = 0
mouse_y = 0

clicked = False

def onMouse(event, x, y, _flags, _param):
    global mouse_x, mouse_y, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_x = x
        mouse_y = y
        clicked = True

cv2.namedWindow("capture")
cv2.setMouseCallback("capture", onMouse)

hist = []
bound = None

while True:
    ok, img = imcap.read()
    if not ok:
        break
    height, width, depth = img.shape
    
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.circle(img, (mouse_x, mouse_y), 10, (10,10,255))
    
    clr = img[mouse_y][mouse_x]
    if clicked:
        if bound == None:
            bound = (clr, clr)
        else:
            hist.append(bound)
            max, min = bound
            max = np.maximum(max, clr)
            min = np.minimum(min, clr)
            bound = (max, min)
        clicked = False

    
    if bound != None:
        mask = cv2.bitwise_not(cv2.inRange(img, bound[1], bound[0]))
        img = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("capture", img)
    key = cv2.waitKey(1)
    if bound != None:
        print(f"({bound[1].tolist()}, {bound[0].tolist()})")
    if key == ord('q'):
        break
    if key == ord('z'):
        if hist:
            bound = hist.pop(-1)
        else:
            bound = None

imcap.release()
cv2.destroyAllWindows()
