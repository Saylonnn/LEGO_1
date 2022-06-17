import socket
import keyboard
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('192.168.117.1', 8484))
except:
    print("no connection")

connection = s.makefile('wb')

keyboard.on_press_key("w", lambda _:s.sendall(b'FW'))

keyboard.on_press_key("s", lambda _:s.sendall(b'BW'))
#keyboard.on_release("wa", lambda _:print("stop L"))
keyboard.on_press_key("h", lambda _:s.sendall(b'hold'))
#keyboard.on_release("s", lambda _:print("stop BWah

keyboard.on_press_key("a", lambda _:s.sendall(b'angel 50'))
#keyboard.on_release("d", lambda _:print("stop R"))
keyboard.on_press_key("q", lambda _:s.sendall(b'speed 50'))
keyboard.on_press_key("e", lambda _:s.sendall(b'exit'))

while True:
    time.sleep(100)