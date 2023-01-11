import cv2

# Load image
cap = cv2.VideoCapture(0)
# Define kernel size
kernel_size = (5,5)

while True:
    ret, frame = cap.read()
    # Apply Gaussian Blur
    frame = cv2.GaussianBlur(frame, kernel_size, 0)
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green = (36, 25, 25)
    upper_green = (86, 255, 255)

    # Define range of red color in HSV
    lower_red = (0, 64, 94)
    upper_red = (10, 255, 255)

    # Create masks for green and red colors
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    # Use bitwise_and to mask the green bottle with red cap
    # res = cv2.bitwise_and(green_mask, red_mask)
    # Display the result
    # cv2.imshow("image", frame)

    # Find contours of the object
    contours, _ = cv2.findContours(green_mask + red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find bounding box around the object
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    res = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_or(green_mask, red_mask))
    cv2.imshow("image", res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()