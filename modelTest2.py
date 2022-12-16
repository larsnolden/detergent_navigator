import cv2
import numpy as np
import tensorflow as tf
import pprint

# Use the camera to make a picture
print("Making a picture...")
imcap = cv2.VideoCapture(0)
imcap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
imcap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
_, img = imcap.read()
imcap.release()

print("Converting image...")
img = tf.convert_to_tensor(img, dtype=tf.uint8)
img = tf.image.resize(img, [320, 320])
img = img[tf.newaxis, :]
img = tf.cast(img, dtype=tf.uint8)

# Load the TFLite model and allocate tensors.
print("Loading model...")
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#pprint.pprint(input_details)
#pprint.pprint(output_details)

# Test the model on random input data.
input_shape = input_details[0]['shape']
input_data = np.array(np.random.random_sample(input_shape), dtype=np.uint8)
interpreter.set_tensor(input_details[0]['index'], img)

interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
confs = interpreter.get_tensor(output_details[0]['index'])
boxes = interpreter.get_tensor(output_details[1]['index'])
print(confs)
print(boxes)

