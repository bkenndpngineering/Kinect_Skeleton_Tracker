# testing openni2 and nite2 python bindings

import numpy as np
import cv2
from primesense import openni2

openni2.initialize("/usr/lib/")     # can also accept the path of the OpenNI redistribution

dev = openni2.Device.open_any()

depth_stream = dev.create_depth_stream()
depth_stream.start()

while(True):

    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()

    img = np.frombuffer(frame_data, dtype=np.uint16)
    img.shape = (1, 480, 640)
    img = np.concatenate((img, img, img), axis=0)
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 0, 1)

    cv2.imshow("image", img)
    cv2.waitKey(34)


depth_stream.stop()
openni2.unload()