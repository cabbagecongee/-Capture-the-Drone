from djitellopy import tello #type: ignore
import time
import keystrokes as kp
import cv2

global img
faceXML = ".mypy_cache/data/haarcascades/haarcascade_frontalface_default.xml"
smileXML = ".mypy_cache/data/haarcascades/haarcascade_smile.xml"
faceDetector = cv2.CascadeClassifier(faceXML)
smileDetector = cv2.CascadeClassifier(smileXML) 

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
        cv2.imwrite(f"tellopy/Resources/Images/{time.time()}.jpg", img) #need to fix doesn't work
        time.sleep(0.3)

    return [lr, fb, ud, yv] 

while True:
    keyValues = getKeyboardInput() 
    drone.send_rc_control(keyValues[0],keyValues[1],keyValues[2],keyValues[3]) #control the drone
    frame = drone.get_frame_read().frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceDetector.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (30,30), flags = cv2.CASCADE_SCALE_IMAGE)

    picture_taken = False
    
    for (x, y, w, h) in faces: 
        cv2.rectangle(frame, (x, y), (x+w-1, y+h-1), (0, 255, 0), 3)

        smiles = smileDetector.detectMultiScale(gray[y:y + h, x:x + w] , 1.8, 20) 

        if len(faces) > 0 and len(smiles) > 0 and picture_taken == False:
            time.sleep(0.5)
            cv2.imwrite(f"tellopy/Resources/Images/{time.time()}.jpg", frame)
            time.sleep(0.3)
            picture_taken = True
  
        for (sx, sy, sw, sh) in smiles: 
            cv2.rectangle(frame[y:y + h, x:x + w], (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)

    if kp.getKey("x"): break
    cv2.imshow("DroneCapture", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cv2.waitKey(1)

cv2.destroyAllWindows
