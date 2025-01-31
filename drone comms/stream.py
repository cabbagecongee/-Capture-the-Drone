# file to stream live video of drone

from djitellopy import Tello
import time
import cv2

# image size
WIDTH = 320
HEIGHT = 240
# startCounter = 1 #0 for flight 1 for testing

#connect to tello
me = Tello()
me.connect()

# #drone pre-settings
# me.for_back_velocity = 0
# me.for_left_velocity = 0
# me.up_down_veolocity = 0
# me.yaw_velocity = 0
# me.speed = 0

print("Battery:", me.get_battery())
me.streamoff()
me.streamon()

me.takeoff()
time.sleep(2)

while True:
    me.send_rc_control(0, 0, 0, 0)
    #get image from tello and resize to specifications above
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.cvtColor(cv2.resize(myFrame, (WIDTH, HEIGHT)), cv2.COLOR_BGR2RGB)

        
    # display image
    cv2.imshow('Live Feed', img)


    #wait for the 'q' button to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break

me.end()
cv2.destroyAllWindows()

    # if startCounter == 0:
    #     me.takeoff()
    #     time.sleep(8)
    #     # me.move_left(10) #define distance and angle, 20cm left, 90 degrees clockwise
    #     # me.rotate_clockwise(90)
    #     me.move_forward(100)
    #     me.land()
    #     startCounter = 1
    
    # # # send velocity values to tello
    # if me.send_rc_control:
    #     me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)




