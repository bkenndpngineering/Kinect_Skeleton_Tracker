from tracker import Tracker
import cv2

t = Tracker()
t.run()
f = t.getFrame()
while f is None:
    f = t.getFrame()

while 1:
    f = t.getFrame()
    print(t.calculate_angle("RIGHT_HAND", "LEFT_HAND"))
    print("Frame gotten!")
    cv2.imshow("img", f)
    print("Frame shown!")
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

t.stop()
cv2.destroyAllWindows()