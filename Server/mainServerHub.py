import sys
import os
import tkinter as tk
from tkinter import scrolledtext
import threading

try:
    import customtkinter as ctk
except ImportError:
    ctk = tk

ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Server.serverInit import Server

class MyServer(Server):
    def __init__(self, gui=None):
        """ Initialize the server. """
        super().__init__()
        self.totalconnectedusers = 0
        self.trackedsockets = []
        self.socketusernames = {}
        self.currentuserstatus = {}
        self.notregistered = set()
        self.gui = gui

    def onStart(self):
        """ Called when the server starts. Prints message to server console and GUI """
        message = "SERVER STARTED AND RUNNING."
        self.log_message(message)

    def log_message(self, message):
        """ Log a message to the console and the GUI (if available) """
        print(message)
        if self.gui:
            self.gui.write_message(message)

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
        self.log_message(message)

    def onMessage(self, socket, message):
        """ Handle incoming messages from clients. """
        if socket in self.notregistered:
            usernameinput = message.strip()
            if usernameinput in self.socketusernames.values():
                self.send(socket, "Username is already in use. Pick another: ")
            else:
                self.socketusernames[socket] = usernameinput
                self.notregistered.remove(socket)
                self.totalconnectedusers += 1
                self.send(socket, "Welcome {}. Total users: {} ".format(usernameinput, len(self.trackedsockets)))
                # self.send(socket, "Available commands: /DISCONNECT, /USERS, /SENDALL, /PM, /GROUPMESSAGE, /CHANGEUSERNAME, /HELP\n")
                self.send(socket, "You can now start chatting: ")
                self.sendall("{} joined the chat. Total users: {}".format(usernameinput, len(self.trackedsockets)), exclude=socket)
        elif socket in self.currentuserstatus and self.currentuserstatus[socket] == "enterreceiver":
            receiver = message.strip()
            if receiver in self.socketusernames.values():
                self.currentuserstatus[socket] = ("entermessage", receiver)
                self.send(socket, "Enter The message you want to send:")
            else:
                self.send(socket, "You can only message connected users:")
                self.send(socket, "Connected users: " + ', '.join(self.socketusernames.values()))
                self.send(socket, "Enter the username of the receiver:")
        elif socket in self.currentuserstatus and self.currentuserstatus[socket][0] == "entermessage":
            usernameofreceiver = self.currentuserstatus[socket][1]
            socketofreceiver = None
            for receiversocket, receiverusername in self.socketusernames.items():
                if receiverusername == usernameofreceiver:
                    socketofreceiver = receiversocket
                    break
            self.send(socketofreceiver, "Private Message From {}: {}".format(self.socketusernames[socket], message))
            self.log_message("{} sent a private message to {}, message: {}".format(self.socketusernames[socket], usernameofreceiver, message))
            del self.currentuserstatus[socket]
        elif socket in self.currentuserstatus and self.currentuserstatus[socket][0] == "sendtoall":
            self.sendall("{}: {}".format(self.socketusernames[socket], message), exclude=socket)
            self.send(socket, "Message sent to all users.")
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
                self.log_message("{} sent a group message to {}, message: {}".format(self.socketusernames[socket], self.socketusernames[socketofreceiver], message))
            self.send(socket, "Message sent to users.")
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
        command = words[0].upper()  
        self.send(socket, "Server has received your request: " + message.strip())  
        if command == "/DISCONNECT" or command == "/DISCONNECT/":
            self.log_message(f" User {self.socketusernames[socket]} entered /DISCONNECT")
            self.onDisconnect(socket)
        elif command == "/USERS" or command == "/USERS/":
            self.log_message(f" User {self.socketusernames[socket]} entered /USERS")
            self.send(socket, "Connected users: " + ', '.join(self.socketusernames.values()))
        elif command == "/SENDALL" or command == "/SENDALL/":
            self.log_message(f" User {self.socketusernames[socket]} entered /SENDALL")
            self.currentuserstatus[socket] = ("sendtoall", None)
            self.send(socket, "Enter your message to broadcast:")
        elif command == "/PM" or command == "/PM/":
            self.log_message(f" User {self.socketusernames[socket]} entered /PM")
            self.currentuserstatus[socket] = "enterreceiver"
            self.send(socket, "Enter the username of the receiver:")
        elif command == "/GROUPMESSAGE" or command == "/GROUPMESSAGE/":
            self.log_message(f" User {self.socketusernames[socket]} entered /GROUPMESSAGE")
            self.currentuserstatus[socket] = ("selectmembers", None)
            self.send(socket, "Enter the usernames of the recipients separated by commas (,):")
        elif command == "/CHANGEUSERNAME" or command == "/CHANGEUSERNAME/":
            self.log_message(f" User {self.socketusernames[socket]} entered /CHANGEUSERNAME")
            self.currentuserstatus[socket] = "updateusername"
            self.send(socket, "Enter your new username:")
        elif command == "/HELP" or command == "/HELP/":
            self.log_message(f" User {self.socketusernames[socket]} entered /HELP")
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
            self.log_message(f" User {self.socketusernames[socket]} entered [invalid] command: {message}")
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
            self.sendall(f"{username} has disconnected. Total users: {len(self.trackedsockets)}", exclude=socket)
            return False
        else:
            self.log_message("A connection has been closed.")
            return False

class ServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Server Command Viewer")

        # Set the background color to black
        self.master.configure(bg="#404040")  # Black background

        # Create a frame with a green border around the main area
        self.frame = ctk.CTkFrame(self.master, fg_color="#404040", border_width=2, border_color="green")
        self.frame.pack(padx=10, pady=10, expand=True, fill="both")

        # Create a modern and stylish text area with larger bold green text
        self.text_area = ctk.CTkTextbox(
            self.frame,
            wrap="word",
            font=("Helvetica", 16, "bold"),  # Larger and bold text
            text_color="green",  # Green text color
            fg_color="#000000",  # Dark gray background color for the text area
            width=400,
            height=800
        )
        self.text_area.pack(padx=10, pady=10, expand=True, fill="both")
        self.text_area.configure(state="disabled")

    def write_message(self, message):
        """Display messages in the text area."""
        self.text_area.configure(state="normal")
        self.text_area.insert("end", message + "\n")
        self.text_area.yview("end")
        self.text_area.configure(state="disabled")

def start_server_gui(host, port):
    root = ctk.CTk()  # Use customtkinter's CTk or fallback to Tk
    gui = ServerGUI(root)

    server = MyServer(gui)  # Pass the GUI instance to the server

    # Start the server in a separate thread
    server_thread = threading.Thread(target=server.start, args=(host, port), daemon=True)
    server_thread.start()

    # Run the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 myserver.py <IP> <Port>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    start_server_gui(host, port)