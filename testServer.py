import cv2
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',1234))
s.listen(1)
c, addr = s.accept()

def webcam():
    while True:
        
