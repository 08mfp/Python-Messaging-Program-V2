import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Server.serverInit import Client
import time

class ChatBotProgram(Client):
    def __init__(self, gui):
        super().__init__()
        self.readyformessaging = False
        self.gui = gui

    def setupuser(self, username):
        self.interractwithserver(username)
        self.readyformessaging = True

    def interractwithserver(self, message):
        self.send(message.encode('utf-8'))

    def onMessage(self, socket, message):
        self.gui.display_message(f"{message}")
        if "Enter your username:" in message or "Username is already in use." in message:
            self.readyformessaging = False
        return True

    def usercommands(self):
        while not self.readyformessaging:
            username = input(">>> ")
            self.setupuser(username)
        while True:
            message = input(">>> ")
            if message.upper() == "/DISCONNECT":
                self.interractwithserver("/DISCONNECT")
                print("The server has processed your request to disconnect.")
                print("Exiting...")
                time.sleep(1)
                break
            print("Sending to server...")
            time.sleep(1)
            
            self.interractwithserver(message)

def main(ip, port, gui):
    client = ChatBotProgram(gui)
    client.start(ip, port)
    return client

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("python3 myserver.py localhost portnumber")
        sys.exit(1)
    ip = sys.argv[1]
    port = int(sys.argv[2])
    main(ip, port)
