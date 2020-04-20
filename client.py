import socket
import json
import keyboard
import os
import base64
import time
import threading


def dodraw():
    data["clientpos"] = draw(_map, data["items"]["guns"], data["items"]["health"], data["clientpos"], data["serverpos"])


def donetworking(c):
    s.sendall(base64.encodebytes(json.dumps(data["clientpos"]).encode("utf-8")))
    try:
        data["serverpos"] = json.loads(base64.decodebytes(s.recv(1024)).decode("utf-8"))
    except ConnectionResetError:
        os.system("cls")
        s.close()
        print("ERROR: CANNOT CONNECT TO THE ENEMY'S SOCKET \nREASON: The Enemy Might be AFK or Crashed")
        exit(1)
    except ConnectionAbortedError:
        os.system("cls")
        s.close()
        print("ERROR: CANNOT CONNECT TO THE ENEMY'S SOCKET \nREASON: The Enemy Might be AFK or Crashed")
        exit(1)


def detectkey(d, mp):
    if keyboard.is_pressed("w") and d[0] != 0:
        try:
            if mp[d[0] - 1][d[1]] != "#":
                d[0] -= 1
        except IndexError:
            pass
    if keyboard.is_pressed("s") and d[0] != 24:
        try:
            if mp[d[0] + 1][d[1]] != "#":
                d[0] += 1
        except IndexError:
            pass
    if keyboard.is_pressed("a") and d[1] != 199:
        try:
            if mp[d[0]][d[1] + 1] != "#":
                d[1] += 1
        except IndexError:
            pass
    if keyboard.is_pressed("d") and d[1] != 0:
        try:
            if mp[d[0]][d[1] - 1] != "#":
                d[1] -= 1
        except IndexError:
            pass
    return d


def waitdata(c):
    while True:
        try:
            a = c.recv(512)
            return a
        except ConnectionAbortedError:
            os.system("cls")
            c.close()
            print("ERROR: CANNOT CONNECT TO THE ENEMY'S SOCKET \n REASON: The Enemy Might be AFK or Crashed")
            exit(1)


def draw(view, guns, health, p, pe):
    for g in guns:
        view[g[0]][g[1]] = "¬"

    for h in health:
        view[h[0]][h[1]] = "+"

    view1 = view
    print(view1)

    view[pe[2]][pe[3]] = " "
    view[pe[0]][pe[1]] = "E"

    view[p[2]][p[3]] = " "
    view[p[0]][p[1]] = "@"
    p[2] = p[0]
    p[3] = p[1]

    unit = ""
    for y in range(0, 25):
        for x in range(0, 120):
            unit += view1[y][x]
        print(unit)
        unit = ""


port = 2362
fps = 0
data = {}
_map = []
st = float()
nd = float()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((input("Connect to IP: "), port))

print("Successfully connected to socket " + s.getsockname()[0])
print("Waiting for server to generate some data....")
# Wait the server until sended the data
data = s.recv(32768)
print(data.decode("utf-8"))
data = json.loads(base64.decodebytes(data).decode("utf-8"))
_map = data["map"]
data.pop("map")

first = time.time()

# Start game
while True:
    st = time.time()
    threadnet = threading.Thread(target=donetworking, args=[s])
    threaddraw = threading.Thread(target=dodraw)

    threadnet.start()

    if time.time() - first >= 1:
        first = time.time()
        fps = 1
    else:
        fps += 1
    print("\n")
    print("Multiplayer Shooter v1".center(120) + "\n\t" + str(fps) + " FPS" + "\n" + "_" * 120)
    threaddraw.start()
    threaddraw.join()
    print(nd - st)

    data["clientpos"] = detectkey(data["clientpos"], _map)

    os.system("cls")
    nd = time.time()
s.close()
