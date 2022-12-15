import numpy as np
import tensorflow as tf
import cv2

print("Loading model...")
# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="model.tflite")

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

interpreter.allocate_tensors()

print("Capturing image...")
# Use the camera:
#imcap = cv2.VideoCapture(0)
#imcap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
#imcap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
#success, img = imcap.read()

# Example images:
#img = cv2.imread('./sharp1/sharp1/pos/7b5000b6cfac4e5895277f7c35c3437f.png')
#img = cv2.imread('./sharp1/sharp1/pos/9b0ad3ac816247b3b1d59072d71b4858.png')
img = cv2.imread('./sharp1/sharp1/pos/ac64d6f639494240bea6c800d3fc84e8.png')


print("Converting image...")
img = tf.convert_to_tensor(img, dtype=tf.uint8)
o_img = img
img = tf.image.resize(img, [320, 320])
img = img[tf.newaxis, :]
img = tf.cast(img, dtype=tf.uint8)

print("Processing image...")
output_data = (interpreter.get_signature_runner())(images=img)
output = output_data
#print(output_data)


count = int(np.squeeze(output['output_0']))
scores = np.squeeze(output['output_1'])
classes = np.squeeze(output['output_2'])
boxes = np.squeeze(output['output_3'])

print(scores)
print(boxes)

img = o_img.numpy().astype(np.uint8)
y1, x1, y2, x2 = boxes[0]
x1 = int(x1 * img.shape[1])
x2 = int(x2 * img.shape[1])
y1 = int(y1 * img.shape[0])
y2 = int(y2 * img.shape[0])

img = cv2.rectangle(img, (x1, y1), (x2, y2),(255,0,0), 4)

cv2.imshow("test", img)

imcap.release()
