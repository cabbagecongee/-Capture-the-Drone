# file to stream live video of drone

from djitellopy import Tello
import cv2

# image size
WIDTH = 320
HEIGHT = 240
startCounter = 1 #0 for flight 1 for testing

#connect to tello
me = Tello()
me.connect()

#drone pre-settings
me.for_back_velocity = 0
me.for_left_velocity = 0
me.up_down_veolocity = 0
me.yaw_velocity = 0
me.speed = 0

print(me.get_battery())
me.streamoff()
me.streamon()

while True:
    #get image from tello and resize to specifications above
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (WIDTH, HEIGHT))

    if startCounter == 0:
        me.takeoff()
        me.move_left(20) #define distance and angle, 20cm left, 90 degrees clockwise
        me.rotate_clockwise(90)
        startCounter = 1
    
    # display image
    cv2.imshow('Live Feed', img)

    #wait for the 'q' button to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break




