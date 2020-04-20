import socket
import json
import random
import base64
import keyboard
import os
import time
import threading


def dodraw():
    data["serverpos"] = draw(_map, data["items"]["guns"], data["items"]["health"], data["serverpos"], data["clientpos"])


def donetworking(c, something_weird_that_i_need_to_make_bcuz_frickin_threading_doesnt_work):
    try:
        data["clientpos"] = json.loads(base64.decodebytes(c.recv(1024)).decode("utf-8"))
    except json.decoder.JSONDecodeError:
        os.system("cls")
        c.close()
        print("ERROR: CANNOT CONNECT TO THE ENEMY'S SOCKET \nREASON: The enemy might be afk or crashed")
        exit(1)

    c.sendall(base64.encodebytes(json.dumps(data["serverpos"]).encode("utf-8")))


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
    if keyboard.is_pressed("a") and d[1] != 0:
        try:
            if mp[d[0]][d[1] - 1] != "#":
                d[1] -= 1
        except IndexError:
            pass
    if keyboard.is_pressed("d") and d[1] != 119:
        try:
            if mp[d[0]][d[1] + 1] != "#":
                d[1] += 1
        except IndexError:
            pass
    return d


def waitdata(c):
    while True:
        try:
            return c.recv(512)
        except Exception as e:
            print(e)


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
            unit += view[y][x]
        print(unit)
        unit = ""

    return p


fps = int()
first = float()
port = 2362
st = float()
nd = float()
data = {"map": [[]],
        "serverpos": [0, 0, 0, 0],  # Y X Yold Xold
        "clientpos": [0, 0, 0, 0],  # Y X Yold Xold
        "items": {
            "guns": [],
            "health": []
            }
        }
map_ = []
_map = []

s = socket.socket()
s.bind(('', port))
print("Created server on " + socket.gethostbyname(socket.gethostname()))
print("Waiting for any clients to connect")

s.listen(5)
while True:
    # Establish connection with client.
    c, addr = s.accept()
    print("Connected by " + addr[0])
    print("Generating map...")

    unit = list()
    for y in range(0, 25):
        for x in range(0, 120):
            if random.randint(0, 6) == 0:
                unit.append("#")
            else:
                unit.append(" ")
        map_.append(unit)
        unit = []
    data["map"] = map_

    print("Generating items...")
    for a in range(0, random.randint(4, 7)):
        data["items"]["guns"].append([random.randint(2, 23), random.randint(3, 117)])
        #  = "¬"

    for a in range(0, random.randint(7, 13)):
        data["items"]["health"].append([random.randint(5, 20), random.randint(10, 100)])
        #  = "+"

    print("Generating random locations to spawn....")
    data["clientpos"] = [random.randint(1, 23), random.randint(1, 44)]
    data["clientpos"] += data["clientpos"]

    data["serverpos"] = [random.randint(1, 23), random.randint(74, 120)]
    data["serverpos"] += data["serverpos"]
    print(data)
    print("Done\n")

    print("Sending data to client..")
    c.sendall(base64.encodebytes(json.dumps(data).encode("utf-8")))
    print("Done")
    _map = data["map"]
    data.pop("map")

    first = time.time()

    # Start game
    while True:
        st = time.time()
        threadnet = threading.Thread(target=donetworking, args=(c, 0))
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

        data["serverpos"] = detectkey(data["serverpos"], _map)
        os.system("cls")
        nd = time.time()
    c.close()
