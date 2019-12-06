from tracker import Tracker
import cv2

t = Tracker()
t.run()

while 1:
    f = t.getFrame()
    print(t.calculate_angle("RIGHT_HAND", "LEFT_HAND"))
    print("Frame gotten!")
    if f is not None:
        cv2.imshow("img", f)
    print("Frame shown!")


t.stop()
