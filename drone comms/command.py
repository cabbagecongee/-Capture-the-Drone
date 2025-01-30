## this is the file for the code to send commands to the drone

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ("192.168.10.1", 8889)
sock.bind(tello_address)

while True: 
    try: 
        msg = input(" ")
        if not msg:
            break
        if 'end' in msg:
            sock.close()
            break
        msg = msg.encode()
        sent = sock.sendto(msg, tello_address)
    except Exception as err:
        print(err)
        sock.close()
    break

## PLS CHANGE 