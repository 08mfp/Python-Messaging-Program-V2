from ex2utils import Server
import sys

class MyServer(Server):
    def onStart(self):
        print("Server has started.")

    def onConnect(self, socket):
        print("Client has connected.")

    def onMessage(self, socket, message):
        print(f"Message received: {message}")
        return True

    def onDisconnect(self, socket):

        print("Client has disconnected.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python myserver.py [host] [port]")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])
    server = MyServer()
    server.start(host, port)

#7070 being used
#7071
    