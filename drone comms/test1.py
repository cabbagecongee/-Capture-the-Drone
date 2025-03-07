from djitellopy import tello #type: ignore
import time
import keystrokes as kp
import cv2
import mediapipe as mp #type: ignore

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

kp.init()  # Initialize keyboard input

# Connect to drone
drone = tello.Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")
drone.streamon()  # Start camera stream

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed
    if kp.getKey("UP"): fb = moveSpeed
    elif kp.getKey("DOWN"): fb = -moveSpeed
    if kp.getKey("w"): ud = liftSpeed
    elif kp.getKey("s"): ud = -liftSpeed
    if kp.getKey("d"): yv = rotationSpeed
    elif kp.getKey("a"): yv = -rotationSpeed
    if kp.getKey("q"): drone.land()
    elif kp.getKey("e"): drone.takeoff()
    return [lr, fb, ud, yv]

def is_peace_sign(landmarks):
    """Detects if the hand is making a peace sign"""
    fingers = []
    tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

    # Check if fingers are extended (tip is higher than PIP joint)
    for i in range(1, 5):  # Ignore thumb for peace sign
        if landmarks[tip_ids[i]].y < landmarks[tip_ids[i] - 2].y:
            fingers.append(1)  # Extended
        else:
            fingers.append(0)  # Folded

    return fingers == [1, 1, 0, 0]  # Peace sign pattern (Index & Middle up, others down)

while True:
    keyValues = getKeyboardInput()
    drone.send_rc_control(*keyValues)

    # Get frame and convert to RGB
    frame = drone.get_frame_read().frame
    frame = cv2.resize(frame, (640, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Hand detection
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        print("Hand detected!")  # Debugging output
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check for peace sign
            if is_peace_sign(hand_landmarks.landmark):
                print("✌️ Peace sign detected! Taking picture.")
                # cv2.imwrite(f"tellopy/Resources/Images/{time.time()}.jpg", frame)
                cv2.imwrite(f"/Users/tuyennguyen/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Academics/Caltech/2425/CS12/Peace Signs?/{time.time()}.jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Change the path accordingly

                time.sleep(1)  # Avoid multiple triggers

    else:
        print("No hands detected.")  # Debugging output

    cv2.imshow("Hand Gesture Detection", frame)
    if kp.getKey("x"): break
    cv2.waitKey(1)

cv2.destroyAllWindows()
