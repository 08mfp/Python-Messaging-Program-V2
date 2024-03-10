#########################################################################################
# MOHAMED FARID PATEL
#########################################################################################
""" 
To run the server, use the following command:
>>>> python3 myserver.py <IP> <Port> e.g. python3 myserver.py localhost 7090.

To run the client (in a new/seperate terminal), use the following command: 
>>>> python3 myclient.py <IP> <Port> e.g. python3 myclient.py localhost 7090 (The IP and Port should be the same as the server).

Typical usage:
1 - Once the client is running, you will be asked to enter a username. (if you enter a username that is already in use, you will be asked to enter a different username).
2 - Once you have entered a username, you can start sending messages to the server.
3 - Your available commands are:
    /DISCONNECT - to disconnect from the server.
    /HELP - to get a list of commands that you can use.
    /USERS - to get a list of users that are currently connected to the server.
    /PM - to send a private message to a specific user.
    /GROUPMESSAGE - to send a message to a group of users.
    /SENDALL - to send a message to all users (and the server).
    /CHANGEUSERNAME - to change your username.
4 - You can connect multiple clients to the server by running myclient.py in new/seperate terminals.
5 - To disconnect from the server, type "/DISCONNECT" and press enter. Once you have disconnected, the client will exit.
6 - You can stop the server by pressing "Ctrl + C" twice in the terminal window where the server is running. Doing this will disconnect all connected clients.

Extra information:
- You must enter a / before each command.
- the commands are not case sensitive (e.g. you can enter /sendall or /SENDALL).
- The server will display all messages and commands that the client enters.
- Once you select the /PM command, you will be asked to enter the username of the recipent, then you will be asked to enter the message. (if you enter an invalid username, you will be asked to try again).
- Once you select the /GROUPMESSAGE command, you will be asked to enter the usernames of the recipents, then you will be asked to enter the message. (if you enter no valid usernames, you will be asked to try again).
- Once you select the /SENDALL command, you will be asked to enter the message.
- Once you select the /CHANGEUSERNAME command, you will be asked to enter the new username. (if you enter a username that is already in use, you will be asked try again).

In order to test the code:
1 - Run the server on a new terminal.
2 - Run the client on a new terminal.
3 - Enter a username e.g. username1.
4 - On a separate terminal, Run another client & enter a different username e.g. username2.
5 - Send messages between the two clients using the available commands. (/PM or /SENDALL etc.)
6 - Connect a third client (in a new terminal) & register a unique username e.g. username3. 
7 - Connect a fourth client (in a new terminal) & register a unique username e.g. username4.
8 - You can now test group messaging by entering /GROUPMESSAGE in the first terminal. When asked to enter the usernames of the recipents, enter "username2, username4". The message will be sent to username2 and username4.
9 - In any of the clients, you can enter /USERS to see a list of all the users that are currently connected to the server.
10 - In any of the clients, you can enter /CHANGEUSERNAME to change your username.
11 - In any of the clients, you can enter /HELP to see a list of available commands.
12 - In any of the clients, you can enter /SENDALL to send a message to all users (and the server).
13 - Disconnect from all servers one by one using the /DISCONNECT command.
14 - Once all clients have disconnected, Stop the server by pressing "Ctrl + C" twice in the terminal window where the server is running.
"""
#########################################################################################

import sys
from ex2utils import Client
import time

class ChatBotProgram(Client):
    def __init__(self):
        super().__init__()
        self.readyformessaging = False

    def setupuser(self, username):
        self.interractwithserver(username)
        self.readyformessaging = True

    def interractwithserver(self, message):
        self.send(message.encode('utf-8'))

    def onMessage(self, socket, message):
        print("{}".format(message))
        if "Enter your username:" in message or "Username is already in use." in message:
            self.readyformessaging = False
        return True

    def usercommands(self):
        while not self.readyformessaging:
            username = input(">>> ")
            self.setupuser(username)
        while True:
            message = input(">>> ")
            if message.upper() == "/DISCONNECT": # The server will handle the disconnection, this loop is just used to terminate the client.
                self.interractwithserver("/DISCONNECT")
                print("The server has processeed your request to disconnect.")
                print("Exiting...")
                time.sleep(1)
                break
            print("Sending to server...")
            time.sleep(1) # simulate delay and allow server to proces message and asign state
            
            self.interractwithserver(message)

def main(ip, port):
    client = ChatBotProgram()
    client.start(ip, port)
    client.usercommands()
    client.stop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("python3 myserver.py localhost portnumber")
        sys.exit(1)
    ip = sys.argv[1]
    port = int(sys.argv[2])
    main(ip, port)
