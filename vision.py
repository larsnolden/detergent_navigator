import cv2

print("Opening the camera...")
imcap = cv2.VideoCapture(0)

imcap.set(3, 640)
imcap.set(4, 480)

print("Loading the clasifier...")
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

print("Starting loop")
try:
	while True:
		success, img = imcap.read()
	
		imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = faceCascade.detectMultiScale(imgGray, 1.3, 5)
		img = cv2.rectangle(img, (0,0), (10,10), (0,255,0), 3)
		for (x, y, w, h) in faces:
			img =cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 3)
	
		cv2.imshow('face_detect', img)
		cv2.waitKey(10)
except:
	pass

print("Writing last image...")
cv2.imwrite("last_image.png", img)

print("Closing program")
imcap.release()
cv2.destroyWindow('face_detect')