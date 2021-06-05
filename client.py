import socket
import threading
import turtle
import pickle
import time
from tkinter import *
import tkinter.messagebox
import sys

list_of_coordinates = []
no_of_players = 2
players_remaining = no_of_players
my_id = 0
host = '192.168.0.101'
port = 10000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
print("Connected to Game")
print("")
direc = [""]*no_of_players
counter = 0
while True:
        if counter < 1:
                i_msg = sock.recv(1024)
                i_msg = pickle.loads(i_msg)
                # print(i_msg)
                # print("")
                my_id = i_msg
                counter += 1
        else:
                break
print("your id is: ", my_id)
while True:
        if len(list_of_coordinates) < no_of_players:
                incoming_message = sock.recv(1024)
                incoming_message = pickle.loads(incoming_message)
                list_of_coordinates.append(incoming_message)
                # print(incoming_message)
                # print("")
        else:
                break
# for i in range(no_of_players):
#         print(list_of_coordinates[i])

window = turtle.Screen()
window.bgcolor("green")
window.setup(width=600, height=600)
window.tracer(0)

def go_up():
        global direc
        list_of_coordinates2 = []
        temp = direc[my_id - 1] = "up"
        list_of_coordinates2.append(my_id)
        list_of_coordinates2.append(temp)
        list_of_coordinates2.append("Playing")
        msg = pickle.dumps(list_of_coordinates2)
        sock.sendall(msg)


def go_down():
        global direc
        list_of_coordinates2 = []
        temp = direc[my_id-1] = "down"
        list_of_coordinates2.append(my_id)
        list_of_coordinates2.append(temp)
        list_of_coordinates2.append("Playing")
        msg = pickle.dumps(list_of_coordinates2)
        sock.sendall(msg)


def go_right():
        global direc
        list_of_coordinates2 = []
        temp =  direc[my_id - 1] = "right"
        list_of_coordinates2.append(my_id)
        list_of_coordinates2.append(temp)
        list_of_coordinates2.append("Playing")
        msg = pickle.dumps(list_of_coordinates2)
        sock.sendall(msg)


def go_left():
        global direc
        list_of_coordinates2 = []
        temp = direc[my_id - 1] = "left"
        list_of_coordinates2.append(my_id)
        list_of_coordinates2.append(temp)
        list_of_coordinates2.append("Playing")
        msg = pickle.dumps(list_of_coordinates2)
        sock.sendall(msg)


def move(id):
        global direc
        if direc[id] == "up":
                y = dict1[id+1].ycor()
                dict1[id+1].sety(y+20)
        if direc[id] == "down":
                y = dict1[id+1].ycor()
                dict1[id+1].sety(y-20)
        if direc[id] == "left":
                x = dict1[id+1].xcor()
                dict1[id+1].setx(x-20)
        if direc[id] == "right":
                x = dict1[id+1].xcor()
                dict1[id+1].setx(x+20)


turtle_ids = []
u = 1
for i in range(no_of_players):
        turtle_ids.append(u)
        u += 1
dict1 = {}
segments = []

for turtle_id in turtle_ids:
        x = list_of_coordinates[turtle_id-1][0]
        y = list_of_coordinates[turtle_id-1][1]
        dict1[turtle_id] = turtle.Turtle()
        dict1[turtle_id].speed(0)
        dict1[turtle_id].shape("square")
        dict1[turtle_id].color("black")
        dict1[turtle_id].penup()
        dict1[turtle_id].goto(x, y)

for i in range(no_of_players):
        segments.append([])
        for j in range(2):
                new_segment = turtle.Turtle()
                new_segment.speed(0)
                new_segment.shape("square")
                new_segment.color("grey")
                new_segment.penup()
                new_segment.goto(dict1[i+1].xcor(), dict1[i+1].ycor())
                segments[i].append(new_segment)

list_of_players = ["Playing"]*no_of_players
def recvMsg():
    while True:
            global direc
            message1 = sock.recv(1024)
            message1 = pickle.loads(message1)
            sender_id = message1[0]
            dir = message1[1]
            p_or_not = message1[2]
            direc[sender_id - 1] = dir
            print(sender_id, dir, p_or_not)
            # if p_or_not == "Playing":
            #         direc[sender_id - 1] = dir
            #         print(sender_id, dir, p_or_not)
            # elif p_or_not == "Winner":
            #         direc[sender_id - 1] = dir
            #         tkinter.messagebox.showinfo("Congratulations, You won")
                    # sock.close()
                    # sys.exit()

t2 = threading.Thread(target=recvMsg)
t2.daemon = True
t2.start()

window.listen()
window.onkeypress(go_up, "Up")
window.onkeypress(go_down, "Down")
window.onkeypress(go_left, "Left")
window.onkeypress(go_right, "Right")

while True:
        window.update()
        for i in range(len(dict1)):
                if list_of_players[i] == "Playing":
                        for index in range(len(segments[i]) - 1, 0, -1):
                                x = segments[i][index-1].xcor()
                                y = segments[i][index-1].ycor()
                                segments[i][index].goto(x, y)
                        if len(segments[i]) > 0:
                                x = dict1[i+1].xcor()
                                y = dict1[i+1].ycor()
                                segments[i][0].goto(x, y)
                        if dict1[i + 1].xcor() > 290 or dict1[i + 1].xcor() < -290 or dict1[i + 1].ycor() > 290 or dict1[i + 1].ycor() < -290:
                                list_of_players[i] = "Lost"
                                direc[i] = ""
                                players_remaining -= 1
                                dict1[i+1].reset()
                                for s in segments[i]:
                                        s.goto(1000, 1000)
                                segments[i].clear()
                                if i+1 == my_id:
                                        print('You are eliminated because you touched the boundary')
                                        mess = []
                                        mess.append(my_id)
                                        mess.append("")
                                        mess.append("Eliminated")
                                        messi = pickle.dumps(mess)
                                        sock.sendall(messi)
                                        sock.close()
                                        sys.exit()
                        else:
                                move(i)
        time.sleep(0.2)

window.mainloop()