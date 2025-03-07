from djitellopy import tello #type: ignore
import time
import keystrokes as kp
import cv2
import mediapipe as mp #type: ignore

#initalize everything
global img
#face
faceXML = "drone comms/data/haarcascades/haarcascade_frontalface_default.xml"
smileXML = "drone comms/data/haarcascades/haarcascade_smile.xml"
faceDetector = cv2.CascadeClassifier(faceXML)
smileDetector = cv2.CascadeClassifier(smileXML) 

#pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

kp.init() #initialize keyboard input

drone = tello.Tello() #connect to drone
drone.connect()
print(f"Battery: {drone.get_battery()}%")
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

def detect_smile(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceDetector.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (30,30), flags = cv2.CASCADE_SCALE_IMAGE)

    picture_taken = False
    
    for (x, y, w, h) in faces: 
        cv2.rectangle(frame, (x, y), (x+w-1, y+h-1), (0, 255, 0), 3)

        smiles = smileDetector.detectMultiScale(gray[y:y + h, x:x + w] , 1.8, 20) 

        if len(faces) > 0 and len(smiles) > 0 and picture_taken == False:
            time.sleep(0.5)
            cv2.imwrite(f"drone comms/data/smile/{time.time()}.jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            time.sleep(0.3)
            picture_taken = True
  
        for (sx, sy, sw, sh) in smiles: 
            cv2.rectangle(frame[y:y + h, x:x + w], (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)

def is_peace_sign(landmarks):
    fingers = []
    tip_ids = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky

    # check if fingers are extended (tip is higher than PIP joint)
    for i in range(1, 5):  # ignore thumb for peace sign
        if landmarks[tip_ids[i]].y < landmarks[tip_ids[i] - 2].y:
            fingers.append(1)  # extended
        else:
            fingers.append(0)  # folded

    return fingers == [1, 1, 0, 0]  # peace sign pattern (index & middle up, others down)

def detect_peace(frame):
    frame = cv2.resize(frame, (640, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        print("Hand detected!")  # debugging output
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check for peace sign
            if is_peace_sign(hand_landmarks.landmark):
                print("✌️ Peace sign detected! Taking picture.")
                cv2.imwrite(f"drone comms/data/pose/{time.time()}.jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                time.sleep(1)  # Avoid multiple triggers

    else:
        print("No hands detected.")  # Debugging outpute

while True:
    print(f"Battery: {drone.get_battery()}%")
    keyValues = getKeyboardInput() 
    drone.send_rc_control(keyValues[0],keyValues[1],keyValues[2],keyValues[3]) #control the drone
    frame = drone.get_frame_read().frame

    detect_smile(frame)
    detect_peace(frame)
    
    if kp.getKey("x"): break
    cv2.imshow("DroneCapture", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cv2.waitKey(1)

cv2.destroyAllWindows
