"""
client.py

Receives and displays a video stream from the server.py
This implementation is based on the implementation found in this stack overflow thread
https://stackoverflow.com/questions/49084143/opencv-live-stream-video-over-socket-in-python-3
"""

import socket, cv2, pickle, struct

#create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.20' #Replace with correct IP or run subscript to find the correct IP
port = 9999
client_socket.connect((host_ip, port)) #tuple

data = b""

payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) #4k
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data= data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("RECEIVED VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

client_socket.close()

                      


