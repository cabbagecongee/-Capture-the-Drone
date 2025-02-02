from djitellopy import tello
import time
import keystrokes as kp
import cv2

global img

#Initialize Keyboard Input
kp.init()

#Start Connection With Drone
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
#Start Camera Display Stream
drone.streamon()

def getKeyboardInput():
    #LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
    lr, fb, ud, yv = 0,0,0,0
    speed = 50
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100

    if kp.getKey("LEFT"): lr = -speed #Controlling The Left And Right Movement
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = moveSpeed #Controlling The Front And Back Movement
    elif kp.getKey("DOWN"): fb = -moveSpeed

    if kp.getKey("w"): ud = liftSpeed #Controlling The Up And Down Movemnt:
    elif kp.getKey("s"): ud = -liftSpeed 

    if kp.getKey("d"): yv = rotationSpeed #Controlling the Rotation:
    elif kp.getKey("a"): yv = -rotationSpeed 

    if kp.getKey("q"): drone.land(); #Landing The Drone
    elif kp.getKey("e"): drone.takeoff() #Take Off The Drone

    if kp.getKey("z"): #Screen Shot Image From The Camera Display
        cv2.imwrite(f"tellopy/Resources/Images/{time.time()}.jpg", img)
        time.sleep(0.3)

    return [lr, fb, ud, yv] #Return The Given Value

while True:
    keyValues = getKeyboardInput() 
    drone.send_rc_control(keyValues[0],keyValues[1],keyValues[2],keyValues[3]) #control the drone
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (1080,720))
    cv2.imshow("DroneCapture", img)
    cv2.waitKey(1)
    drone.sleep(0.05)