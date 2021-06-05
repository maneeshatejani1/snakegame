# snakegame
multiplayer snake game that can be played by players in real time. Inspired by the popular Nokia's snake game
# Pre-Requisites 
python3
# Dependencies
socket,threading,pickle,turtle,tkinter
# Instructions
first, change the value of 'host' in server.py to your server's ip adsress. You can also set the number of players by changing the corresponding variable name in both the server and client files.
To run the server, run command 'python3 servery.py'

You can run multiple instances of clients in one machine as well but for better experience, run the client code in different machines to test the game. To run client, you need to change the 'host' value in client.py file as well and change it to your server's ip adress where the server code is running
