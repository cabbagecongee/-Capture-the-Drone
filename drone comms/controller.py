import serial

ser = serial.Serial('COM5', 9600, timeout=1)

# serial connection to arduino
def readserial(ser):
    # print(str(ser))
    # data = ser.readline().decode().strip().split(', ')
    # while True:
    if ser.in_waiting>0:
        #data = ser.read()
        d = ser.readline()
        data = d.decode('utf-8', 'ignore').strip().split(', ')
        return data
    else:
        return None

def getControllerInput(x, y, button1, z, rotation, button2):
    #LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
    lr, fb, ud, yv = 0,0,0,0
    speed = 50
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100

    if x < 500: 
        lr = -speed #left right
        print(f"go left: {str(lr)}")
    elif x > 530: 
        lr = speed
        print(f"go right: {str(lr)}")

    if y > 530: 
        fb = moveSpeed #forward backward
        print(f"go forwards: {str(fb)}")
    elif y < 500: 
        fb = -moveSpeed
        print(f"go backwards: {str(fb)}")

    if z > 530: 
        ud = liftSpeed #up down
        print(f"go up: {str(ud)}")
    elif z < 500: 
        ud = -liftSpeed 
        print(f"go down: {str(ud)}")

    if rotation < 480: 
        yv = rotationSpeed
        print(f"rotate left: {str(yv)}") #left right rotation
    elif rotation > 510: 
        yv = -rotationSpeed 
        print(f"rotate right: {str(yv)}")

    if button1 == 0: print("LAND")#drone.land(); 
    elif button2 == 0: print("TAKEOFF")#drone.takeoff() 

    return [lr, fb, ud, yv] 

while True:
    # if ser.in_waiting > 0:
    #     line = ser.readline().decode('utf-8', 'ignore').strip()
    #     print(f"Received: {line}")
    controller_data = readserial(ser)
    if controller_data is not None:
        x, y, button1, z, rotation, button2 = controller_data
        
        # keyValues = getKeyboardInput() 
        keyValues = getControllerInput(int(x), int(y), int(button1), int(z), int(rotation), int(button2)) 
        # print(keyValues)
import serial

ser = serial.Serial('COM5', 9600, timeout=1)

# serial connection to arduino
def readserial(ser):
    # print(str(ser))
    # data = ser.readline().decode().strip().split(', ')
    # while True:
    if ser.in_waiting>0:
        #data = ser.read()
        d = ser.readline()
        data = d.decode('utf-8', 'ignore').strip().split(', ')
        return data
    else:
        return None

def getControllerInput(x, y, button1, z, rotation, button2):
    #LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
    lr, fb, ud, yv = 0,0,0,0
    speed = 50
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100

    if x < 500: 
        lr = -speed #left right
        print(f"go left: {str(lr)}")
    elif x > 530: 
        lr = speed
        print(f"go right: {str(lr)}")

    if y > 530: 
        fb = moveSpeed #forward backward
        print(f"go forwards: {str(fb)}")
    elif y < 500: 
        fb = -moveSpeed
        print(f"go backwards: {str(fb)}")

    if z > 530: 
        ud = liftSpeed #up down
        print(f"go up: {str(ud)}")
    elif z < 500: 
        ud = -liftSpeed 
        print(f"go down: {str(ud)}")

    if rotation < 480: 
        yv = rotationSpeed
        print(f"rotate left: {str(yv)}") #left right rotation
    elif rotation > 510: 
        yv = -rotationSpeed 
        print(f"rotate right: {str(yv)}")

    if button1 == 0: print("LAND")#drone.land(); 
    elif button2 == 0: print("TAKEOFF")#drone.takeoff() 

    return [lr, fb, ud, yv] 

while True:
    # if ser.in_waiting > 0:
    #     line = ser.readline().decode('utf-8', 'ignore').strip()
    #     print(f"Received: {line}")
    controller_data = readserial(ser)
    if controller_data is not None:
        x, y, button1, z, rotation, button2 = controller_data
        
        # keyValues = getKeyboardInput() 
        keyValues = getControllerInput(int(x), int(y), int(button1), int(z), int(rotation), int(button2)) 
        # print(keyValues)
