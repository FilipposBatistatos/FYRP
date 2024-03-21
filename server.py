"""
Server.py

the server creates a socket which then displays the image received from the clients
This implementation is based on the implementation found in this stack overflow thread
https://stackoverflow.com/questions/49084143/opencv-live-stream-video-over-socket-in-python-3
"""

import socket, cv2, pickle, struct

#Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #potentially change this as it used TCP
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print("HOST IP:", host_ip) #debbuging

port = 9999
socket_address = (host_ip, port)

#bind the socket
server_socket.bind(socket_address)

#Liste to the socket
server_socket.listen(5)
print("LISTENING AT: ", socket_address)

#Accept the socket stream
while True:
    client_socket,addr = server_socket.accept()
    print("SUCCESSFUL CONNECTION WITH ADDRESS: ", addr)
    if client_socket:
        vid = cv2.VideoCapture(0)

        while(vid.isOpened()):
            img, frame = vid.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a))+a
            client_socket.sendall(message)

            #Debugging to know what the camera can see
            cv2.imshow("TRANSMITTING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF
            if key ==ord('q'):
                client_socket.close()