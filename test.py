import socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('ec2-100-26-161-44.compute-1.amazonaws.com', 1234))
