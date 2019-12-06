from tracker import Tracker
import cv2

try:
    t = Tracker()
    t.run()
    while 1:
        print(t.calculate_angle("RIGHT_HAND", "LEFT_HAND"))
        f = t.getFrame()
        cv2.imshow("img", f)

except Exception as e:
    print(e)


t.stop()