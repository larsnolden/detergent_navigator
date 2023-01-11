import cv2
import numpy as np
import tensorflow as tf
#import pprint

# Load the TFLite model and allocate tensors.
print("Loading model...")
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Use the camera to make a picture
print("Loading Camera...")
imcap = cv2.VideoCapture(0)
imcap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
imcap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

try:
    while True:
        print("Taking picture... (Smile)")
        _, img = imcap.read()
        oimg = img
        print("Converting image...")
        img = tf.convert_to_tensor(img, dtype=tf.uint8)
        img = tf.image.resize(img, [320, 320])
        img = img[tf.newaxis, :]
        img = tf.cast(img, dtype=tf.uint8)

        #pprint.pprint(input_details)
        #pprint.pprint(output_details)

        # Test the model on random input data.
        #input_shape = input_details[0]['shape']
        #input_data = np.array(np.random.random_sample(input_shape), dtype=np.uint8)
        print("Interpreting image...")
        interpreter.set_tensor(input_details[0]['index'], img)
        interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        confs = interpreter.get_tensor(output_details[0]['index'])
        boxes = interpreter.get_tensor(output_details[1]['index'])
        box = boxes[0][0]
        print(box)
        xmin, xmax, ymin, ymax = box
        xmin = int(640*xmin)
        xmax = int(640*xmax)
        ymin = int(480*ymin)
        ymax = int(480*ymax)
        print("Showing image...")
        img = cv2.rectangle(oimg, (xmin, ymin) , (xmax, ymax), (255,0,0), 2)
        cv2.imshow("capture", img)
        cv2.waitKey(1)
except Exception as e:
    print(e)
    pass
except:
    print("Interupted")

print("Closing...")
cv2.destroyAllWindows()
imcap.release()
