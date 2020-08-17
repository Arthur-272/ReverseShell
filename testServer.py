import pyaudio
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',1234))
s.listen(1)
c, addr = s.accept()

def audio(c):
    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    record_seconds = 5
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    try:
        try:
            while True:
                data = c.recv(1024)
                stream.write(data)
        except KeyboardInterrupt:
            pass
    except:
        print("Error")
try:
    audio(c)
except KeyboardInterrupt:
    pass
