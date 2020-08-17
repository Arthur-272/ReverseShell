import socket
import pyaudio

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',1234))

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

while True:
    data = stream.read(chunk)
    s.send(data)
