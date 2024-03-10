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
