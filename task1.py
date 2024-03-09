from ex2utils import Server
import sys

class MyServer(Server):
    def __init__(self):
        super().__init__()
        self.active_clients = 0
        self.clients = []

    def onStart(self):
        print("Server has started.")

    def onConnect(self, socket):
        self.active_clients += 1
        self.clients.append(socket)
        print(f"A client has connected. Total clients: {self.active_clients}")
        self.broadcast("A new client has connected.")

    def onMessage(self, socket, message):
        print(f"Message received: {message}")

    def onDisconnect(self, socket):
        self.active_clients -= 1
        if socket in self.clients:
            self.clients.remove(socket)
        print(f"A client has disconnected. Total clients: {self.active_clients}")
        self.broadcast("A client has disconnected.")

    def broadcast(self, message):
        for client_socket in self.clients:
            self.sendMessage(client_socket, message)

    def sendMessage(self, client_socket, message):
        try:
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python myserver.py [host] [port]")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    server = MyServer()
    server.start(host, port)

#7070 being used
#7071
    
