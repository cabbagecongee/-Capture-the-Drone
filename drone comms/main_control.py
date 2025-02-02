from djitellopy import tello
import time
import keystrokes as kp
import cv2

global img

kp.init() #initialize keyboard input


drone = tello.Tello() #connect to drone
drone.connect()
print(drone.get_battery())
drone.streamon() #start camera stream

def getKeyboardInput():
    #LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
    lr, fb, ud, yv = 0,0,0,0
    speed = 50
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100

    if kp.getKey("LEFT"): lr = -speed #left right
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = moveSpeed #forward backward
    elif kp.getKey("DOWN"): fb = -moveSpeed

    if kp.getKey("w"): ud = liftSpeed #up down
    elif kp.getKey("s"): ud = -liftSpeed 

    if kp.getKey("d"): yv = rotationSpeed #left right rotation
    elif kp.getKey("a"): yv = -rotationSpeed 

    if kp.getKey("q"): drone.land(); 
    elif kp.getKey("e"): drone.takeoff() 

    if kp.getKey("z"): #take screenshot of video feed
        cv2.imwrite(f"tellopy/Resources/Images/{time.time()}.jpg", img)
        time.sleep(0.3)

    return [lr, fb, ud, yv] 

while True:
    keyValues = getKeyboardInput() 
    drone.send_rc_control(keyValues[0],keyValues[1],keyValues[2],keyValues[3]) #control the drone
    img = drone.get_frame_read().frame
    img = cv2.cvtColor(cv2.resize(img, (320,240)), cv2.COLOR_BGR2RGB)
    cv2.imshow("DroneCapture", img)
    cv2.waitKey(1)
