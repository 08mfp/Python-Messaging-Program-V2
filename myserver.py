from ex2utils import Server
import sys

class MyServer(Server):
    def __init__(self):
        """ Initialize the server. """
        super().__init__()
        self.totalconnectedusers = 0
        self.trackedsockets = []
        self.socketusernames = {}
        self.currentuserstatus = {}
        self.notregistered = set()

    def onStart(self):
        """ Called when the server starts. Prints message to server console only """
        print("SERVER STARTED AND RUNNING.")

    def onConnect(self, socket):
        """ Called when a new client connects to the server. """
        self.trackedsockets.append(socket)
        self.notregistered.add(socket)
        self.send(socket, "Enter your username: ")

    def send(self, client_socket, message):
        """ Send a message to current client, or other connected clients"""
        client_socket.send(message.encode('utf-8') + b'\n')

    def sendall(self, message, exclude=None):
        """ Send a message to all connected clients and server, except itself. """
        for client_socket in self.trackedsockets:
            if client_socket != exclude:
                self.send(client_socket, message)
        print(message)

    def onMessage(self, socket, message):
        """ Main handling of message handling states and commands. allfeatures() is called if no state is found. allfeatures() commands call onMessage() to set states."""
        if socket in self.notregistered:
            usernameinput = message.strip()
            if usernameinput in self.socketusernames.values():
                self.send(socket, "Username is already in use. Pick another: ")
            else:
                self.socketusernames[socket] = usernameinput
                self.notregistered.remove(socket)
                self.totalconnectedusers += 1
                self.send(socket, "Welcome {}. Total users: {} ".format(usernameinput, len(self.trackedsockets)))# I changed the totalconnectedusers to len(self.trackedsockets) 
                #to fix a bug when using myclient.py (so it is different to the PDF's protocol design).
                # self.send(socket, "Your socket: {}".format(socket)) 
                self.send(socket, "Available commands: /DISCONNECT, /USERS, /SENDALL, /PM, /GROUPMESSAGE, /CHANGEUSERNAME, /HELP\n")
                self.send(socket, "You can now start chatting: ")
                self.sendall("{} joined the chat. Total users: {}".format(usernameinput, len(self.trackedsockets)), exclude=socket) # I changed the totalconnectedusers to len(self.trackedsockets) 
                #to fix a bug when using myclient.py (so it is different to the PDF's protocol design).
        elif socket in self.currentuserstatus and self.currentuserstatus[socket] == "enterreceiver":
            receiver = message.strip()
            if receiver in self.socketusernames.values():
                self.currentuserstatus[socket] = ("entermessage", receiver)
                self.send(socket, "Enter The message you want to send:")
            else:
                self.send(socket, "You can only message connected users:")
                self.send(socket, "Connected users: " + ', '.join(self.socketusernames.values())) #! IF THERE IS ERROR REMOVE TJIS
                self.send(socket, "Enter the username of the receiver:")
        elif socket in self.currentuserstatus and self.currentuserstatus[socket][0] == "entermessage":
            usernameofreceiver = self.currentuserstatus[socket][1]
            socketofreceiver = None
            for receiversocket, receiverusername in self.socketusernames.items():
                if receiverusername == usernameofreceiver:
                    socketofreceiver = receiversocket
                    break
            self.send(socketofreceiver, "Private Message From {}: {}".format(self.socketusernames[socket], message))
            print("{} sent a private message to {}, message: {}".format(self.socketusernames[socket], usernameofreceiver, message))
            del self.currentuserstatus[socket]
        elif socket in self.currentuserstatus and self.currentuserstatus[socket][0] == "sendtoall":
            self.sendall("{}: {}".format(self.socketusernames[socket], message), exclude=socket)
            del self.currentuserstatus[socket]
        elif socket in self.currentuserstatus and self.currentuserstatus[socket][0] == "selectmembers":
            receivers = []
            splitmessage = message.split(',')
            for receiver in splitmessage:
                receivers.append(receiver.strip())
            activeusers = []
            for receiver in receivers:
                if receiver in self.socketusernames.values():
                    activeusers.append(receiver)
            if not activeusers:
                self.send(socket, "User/s does not exist. Try again:")
            else:
                self.currentuserstatus[socket] = ("entergroupmessage", activeusers)
                self.send(socket, "Enter your message to send:")
        elif socket in self.currentuserstatus and self.currentuserstatus[socket][0] == "entergroupmessage":
            for receiver in self.currentuserstatus[socket][1]:
                socketofreceiver = None
                for receiversocket, receiverusername in self.socketusernames.items():
                    if receiverusername == receiver:
                        socketofreceiver = receiversocket
                        break
                self.send(socketofreceiver, "Broadcast Message From {}: {}".format(self.socketusernames[socket], message))
                print("{} sent a group message to {}, message: {}".format(self.socketusernames[socket], socketofreceiver, message))
            del self.currentuserstatus[socket]
        elif socket in self.currentuserstatus and self.currentuserstatus[socket] == "updateusername":
            newusername = message.strip()
            if newusername in self.socketusernames.values():
                self.send(socket, "Username already in use, try another:")
            else:
                oldusername = self.socketusernames[socket]
                self.socketusernames[socket] = newusername
                self.sendall("{} changed their username to {}.".format(oldusername, newusername), exclude=socket)
                self.send(socket, "your new username is {}.".format(newusername))
                del self.currentuserstatus[socket]
        else:
            self.allfeatures(socket, message)
        return True

    def allfeatures(self, socket, message):
        """ All commands that connected clients are able to use. """
        words = message.strip().split(' ', 1)
        command = words[0].upper() # I use this to get the command from the user
        if command == "/DISCONNECT" or command == "/DISCONNECT/" :
            print(" User {} entered /DISCONNECT".format(self.socketusernames[socket]))
            self.onDisconnect(socket)
        elif command == "/USERS" or command == "/USERS/" :
            print(" User {} entered /USERS".format(self.socketusernames[socket]))
            self.send(socket, "Connected users: " + ', '.join(self.socketusernames.values()))
        elif command == "/SENDALL" or command == "/SENDALL/":
            print(" User {} entered /SENDALL".format(self.socketusernames[socket]))
            self.currentuserstatus[socket] = ("sendtoall", None) 
            self.send(socket, "Enter your message to broadcast:")
        elif command == "/PM" or command == "/PM/":
            print(" User {} entered /PM".format(self.socketusernames[socket]))
            self.currentuserstatus[socket] = "enterreceiver"
            self.send(socket, "Enter the username of the receiver:")
        elif command == "/GROUPMESSAGE" or command == "/GROUPMESSAGE/":
            print(" User {} entered /GROUPMESSAGE".format(self.socketusernames[socket]))
            self.currentuserstatus[socket] = ("selectmembers", None)
            self.send(socket, "Enter the usernames of the recipients separated by commas (,):")
        elif command == "/CHANGEUSERNAME" or command == "/CHANGEUSERNAME/":
            print(" User {} entered /CHANGEUSERNAME".format(self.socketusernames[socket]))
            self.currentuserstatus[socket] = "updateusername"
            self.send(socket, "Enter your new username:")
        elif command == "/HELP" or command == "/HELP/":
            print(" User {} entered /HELP".format(self.socketusernames[socket]))
            self.send(socket, "---------------------------------------------------------------")
            self.send(socket, "/DISCONNECT: Terminate connection to the server")
            self.send(socket, "/USERS: Display all the connected users")
            self.send(socket, "/SENDALL: Broadcast message to all connected users and server")
            self.send(socket, "/PM: Send private message")
            self.send(socket, "/GROUPMESSAGE: Send Group Message")
            self.send(socket, "/CHANGEUSERNAME: Change your username")
            self.send(socket, "/HELP: for more")
            self.send(socket, "---------------------------------------------------------------")
        else:
            print(" User {} entered [invalid] command: {} ".format(self.socketusernames[socket], message))
            self.send(socket, "You entered an invalid command (see /HELP)")

    def onDisconnect(self, socket):
        """Handle cleanup when user/client disconnects"""
        username = self.socketusernames.pop(socket, None)
        if socket in self.trackedsockets:
            self.trackedsockets.remove(socket)
        self.currentuserstatus.pop(socket, None)
        self.notregistered.discard(socket)
        self.totalconnectedusers -= 1
        if username:
            goodbye_message = f"Goodbye {username}, sad to see you go"
            self.send(socket, goodbye_message)
            self.sendall(f"{username} has disconnected. Total users: {len(self.trackedsockets)}", exclude=socket)# I changed the totalconnectedusers to len(self.trackedsockets) 
                #to fix a bug when using myclient.py (so it is different to the PDF's protocol design).
            return False
        else:
            print("A connection has been closed.")
            return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("python3 myserver.py localhost portnumber")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    server = MyServer()
    server.start(host, port)
