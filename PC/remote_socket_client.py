import socket
import keyboard
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('192.168.117.1', 8483))
except:
    print("no connection")

connection = s.makefile('wb')

keyboard.on_press_key("w", lambda _:s.sendall(b'FW'))
keyboard.on_release(lambda e: s.sendall(b'FW'+ bytes(e.name, encoding='utf-8')))
keyboard.on_press_key("a", lambda _:print("L"))
#keyboard.on_release("wa", lambda _:print("stop L"))
keyboard.on_press_key("s", lambda _:print("BW"))
#keyboard.on_release("s", lambda _:print("stop BW"))
keyboard.on_press_key("d", lambda _:print("R"))
#keyboard.on_release("d", lambda _:print("stop R"))
keyboard.on_press_key("ü", lambda _:print("STOP"))

while True:
    time.sleep(100)