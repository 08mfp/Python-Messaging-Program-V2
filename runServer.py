import subprocess
import time
import os


SERVER_SCRIPT = os.path.join('Server', 'mainServerHub.py')
CLIENT_GUI_SCRIPT = os.path.join('Client', 'userGUI.py')

def start_server(ip, port):
    """Start the server as a subprocess."""
    server_process = subprocess.Popen(['python3', SERVER_SCRIPT, ip, str(port)])
    return server_process

def start_client_gui(ip, port):
    """Start the client GUI as a subprocess."""
    subprocess.Popen(['python3', CLIENT_GUI_SCRIPT, ip, str(port)])

def main():
    ip = 'localhost'
    port = input("Please enter the port number to run the server and client on: ")
    try:
        port = int(port)
        if port <= 0 or port > 65535:
            raise ValueError("Invalid port number.")
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    print(f"Starting the server on port {port}...")
    server_process = start_server(ip, port)
    time.sleep(2)

    print(f"Starting the client GUI on port {port}...")
    start_client_gui(ip, port)

    try:
        server_process.wait()
    except KeyboardInterrupt:
        print("Shutting down the server...")
        server_process.terminate()

if __name__ == "__main__":
    main()
