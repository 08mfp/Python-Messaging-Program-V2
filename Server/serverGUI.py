# import tkinter as tk
# from tkinter import scrolledtext
# import sys
# import threading
# import os


# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from Server.serverInit import Server

# class ServerGUI:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Server Command Viewer")

#         self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, font=("Helvetica", 10))
#         self.text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
#         self.text_area.config(state=tk.DISABLED)

#         sys.stdout = self

#     def write(self, message):
#         """Display messages in the text area."""
#         self.text_area.config(state=tk.NORMAL)
#         self.text_area.insert(tk.END, message)
#         self.text_area.yview(tk.END)
#         self.text_area.config(state=tk.DISABLED)

#     def flush(self):
#         """Flush method needed to redirect stdout properly."""
#         pass

# class MyServer(Server):
#     def __init__(self, gui):
#         """ Initialize the server. """
#         super().__init__()
#         self.totalconnectedusers = 0
#         self.trackedsockets = []
#         self.socketusernames = {}
#         self.currentuserstatus = {}
#         self.notregistered = set()
#         self.gui = gui

#     def onStart(self):
#         """ Called when the server starts. Prints message to server console only """
#         print("SERVER STARTED AND RUNNING.")

#     def onConnect(self, socket):
#         """ Called when a new client connects to the server. """
#         self.trackedsockets.append(socket)
#         self.notregistered.add(socket)
#         self.send(socket, "Enter your username: ")

#     def send(self, client_socket, message):
#         """ Send a message to current client, or other connected clients"""
#         client_socket.send(message.encode('utf-8') + b'\n')

#     def sendall(self, message, exclude=None):
#         """ Send a message to all connected clients and server, except itself. """
#         for client_socket in self.trackedsockets:
#             if client_socket != exclude:
#                 self.send(client_socket, message)
#         print(message)

#     def onMessage(self, socket, message):
#         """ Main handling of message handling states and commands. """
#         print(f"Received message from {self.socketusernames.get(socket, 'Unknown User')}: {message.strip()}")
#         super().onMessage(socket, message)

#     def onDisconnect(self, socket):
#         """Handle cleanup when user/client disconnects"""
#         username = self.socketusernames.pop(socket, None)
#         if socket in self.trackedsockets:
#             self.trackedsockets.remove(socket)
#         self.currentuserstatus.pop(socket, None)
#         self.notregistered.discard(socket)
#         self.totalconnectedusers -= 1
#         if username:
#             goodbye_message = f"Goodbye {username}, sad to see you go"
#             self.send(socket, goodbye_message)
#             self.sendall(f"{username} has disconnected. Total users: {len(self.trackedsockets)}", exclude=socket)
#             print(f"{username} has disconnected.")
#             return False
#         else:
#             print("A connection has been closed.")
#             return False

# def start_server_gui(host, port):
#     root = tk.Tk()
#     gui = ServerGUI(root)
    
#     server = MyServer(gui)
#     server_thread = threading.Thread(target=server.start, args=(host, port), daemon=True)
#     server_thread.start()

#     root.mainloop()

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python3 server_gui.py <IP> <Port>")
#         sys.exit(1)

#     host, port = sys.argv[1], int(sys.argv[2])
#     start_server_gui(host, port)
