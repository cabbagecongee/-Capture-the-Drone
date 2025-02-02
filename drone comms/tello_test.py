#testing drone

from djitellopy import Tello
import time
import cv2


# image size
WIDTH = 320
HEIGHT = 240
# startCounter = 1 #0 for flight 1 for testing
me = Tello()

#connect to tello
me.connect()

print("Battery:", me.get_battery())
me.streamoff()
me.streamon()
me.takeoff()
time.sleep(2)

while True:
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.cvtColor(cv2.resize(myFrame, (WIDTH, HEIGHT)), cv2.COLOR_BGR2RGB)

    # display image
    cv2.imshow('Live Feed', img)
    me.send_rc_control(0, 0, 0, 0)
    time.sleep(5)
    me.flip_right()
    me.flip_left()
    me.flip_forward()
    me.flip_back()
    #get image from tello and resize to specifications above

    #wait for the 'q' button to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break

me.end()
cv2.destroyAllWindows()


