import cv2
import numpy as np

# Load image
cap = cv2.VideoCapture(0)
# Define kernel size
kernel_size = (5,5)

colors = []
n_color_samples = 200

# for i in range(n_color_samples):
#         ret, frame = cap.read()
#         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#         x=0
#         y=0
#         w=10
#         h=10
#         cv2.rectangle(hsv, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         if(i > 100):
#             print("recording")
#             colors.append(hsv[5, 5])
#         cv2.imshow("preview", hsv)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

while True:   
    # color_min = min(colors, key=lambda num_ar: num_ar[0] + num_ar[1] + num_ar[2])
    # color_max = max(colors, key=lambda num_ar: num_ar[0] + num_ar[1] + num_ar[2])
    # actual_hsv_min = [color_min[0]*2, color_min[1]/255*100, color_min[2]/255*100]
    # actual_hsv_max = [color_max[0]*2, color_max[1]/255*100, color_color_maxmin[2]/255*100]
    # print("found color range: ", color_mactual_hsv_minin, " - ", actual_hsv_max)

    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)
    # Apply Gaussian Blur
    frame = cv2.GaussianBlur(frame, kernel_size, 0)
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green = (23,54,60)
    upper_green = (77, 137, 202)

    # Define range of red color in HSV
    lower_red = (0, 158, 97)
    upper_red = (9, 249, 194)

    # Create masks for green and red colors
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    # Use bitwise_and to mask the green bottle with red cap
    # res = cv2.bitwise_and(green_mask, red_mask)
    # Display the result
    # cv2.imshow("image", frame)

    # Find contours of the object
    # contours, _ = cv2.findContours(green_mask + red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find bounding box around the object

    # res = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_or(green_mask, red_mask))

    # for green_cnt in green_contours:
    #     x, y, w, h = cv2.boundingRect(green_cnt)
    #     found_bottle = False
    #     for red_cnt in red_contours:
    #         x2, y2, w2, h2 = cv2.boundingRect(red_cnt)
    #         if x2 > x and x2 + w2 < x + w and y2 < y and y-0.3*h < y2:
    #             cv2.rectangle(res, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)
    #             found_bottle = True
    #             # break

    #     if found_bottle:
    #         cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #         # if x2 > x and x2 < x + w and y2 > y and y2 < y + h:
    #     # cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)

    for cnt in green_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    

    cv2.imshow("image", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()