import socket
import threading
import random
import pickle

connections = []
addresses = []
list_of_coordinates = []
no_of_connections = 0
no_of_players = 2
player_id = 0
players_kicked_out = 0
for c in connections:
    c.close() #close previous connections
del connections[:] #delete previous connections from list and their addresses
del addresses[:]
host = '192.168.0.101'
port = 10000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(0)
counter = 0
def work(c,):
    global connections
    global players_kicked_out
    while True:
        incoming_message = c.recv(1024)
        incoming_message = pickle.loads(incoming_message)
        print(incoming_message)
        # if players_kicked_out != no_of_players-1:
        if incoming_message[2] == "Eliminated":
            # players_kicked_out += 1
            for conn in connections:
                if conn != c:
                    out_message = pickle.dumps(incoming_message)
                    conn.sendall(out_message)
            c.close()
            connections.remove(c)
            break
        else:
            outgoing_message = pickle.dumps(incoming_message)
            for conn in connections:
                if conn != c:
                    conn.sendall(outgoing_message)
        # else:
        #     incoming_message[2] = "Winner"
        #     out = pickle.dumps(incoming_message)
        #     c.sendall(out)
        #     c.close()
        #     connections.remove(c)
        #     break

while True:
    if no_of_connections < no_of_players:
        no_of_connections += 1
        player_id += 1
        print("Waiting for connection for player ", player_id)
        c, a = sock.accept()
        sock.setblocking(True)  # prevents timeout from happening if i do nothing with the server
        connections.append(c)
        addresses.append(a)
        msg = pickle.dumps(player_id)
        c.sendall(msg)
        print("Player ", player_id, "Connected")
        print("")
        while len(list_of_coordinates) != no_of_connections:
            x = random.randint(-27, 27)
            x = x*10
            y = random.randint(-27, 27)
            y = y*10
            list_of_coordinates.append([])
            list_of_coordinates[no_of_connections-1].append(x)
            list_of_coordinates[no_of_connections-1].append(y)
            list_of_coordinates[no_of_connections-1].append(player_id)
    if no_of_connections == no_of_players:
        no_of_connections += 1
        player_id = 0
        for i in range(no_of_players):
            print(list_of_coordinates[i])
        for c in connections:
            player_id += 1
            for j in range(len(list_of_coordinates)):
                message = pickle.dumps(list_of_coordinates[j])
                c.sendall(message)
            t = threading.Thread(target=work, args=(c, ))
            t.daemon = True
            t.start()


