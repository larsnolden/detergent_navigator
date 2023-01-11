import cv2
import numpy as np

imcap = cv2.VideoCapture(0)

mid = np.array([105+10, 202+10, 130+10])
e = np.array([80, 35, 40])
low = np.array([36, 25, 25])
high = np.array([86, 255, 255])

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

bs = [None]

while True:
    ok, img = imcap.read()
    img = cv2.GaussianBlur(img, (5, 5), 0)
    if not ok:
        break
    
    height, width, depth = img.shape

    
    img = cv2.circle(img, (mouse_x, mouse_y), 10, (10,10,255))
    
    clr = img[mouse_y][mouse_x]
    if bs and clicked:
        if bs[-1] == None:
            bs[-1] = (clr, clr)
        else:
            max, min = bs[-1]
            max = np.maximum(max, clr)
            min = np.minimum(min, clr)
            bs[-1] = (max, min)
        clicked = False

    masks = []
    for b in bs:
        if b == None:
            continue
        masks.append(cv2.bitwise_not(cv2.inRange(img, b[1], b[0])))
    for mask in masks:
        img = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("capture", img)
    key = cv2.waitKey(1)
    print(bs)
    if key == ord('q'):
        break
    if key == ord('n'):
        bs.append(None)
    if key == ord('z'):
        del bs[-1]

imcap.release()
cv2.destroyAllWindows()
