import subprocess
import os
CLIENT_GUI_SCRIPT = os.path.join('Client', 'userGUI.py')

def start_client_gui(ip, port):
    """Start the client GUI as a subprocess."""
    subprocess.Popen(['python3', CLIENT_GUI_SCRIPT, ip, str(port)])

def main():
    ip = 'localhost'
    port = input("What port is the server running on? ")
    try:
        port = int(port)
        if port <= 0 or port > 65535:
            raise ValueError("Invalid port number.")
    except ValueError as e:
        print(f"Error: {e}")
        return
    print(f"Starting the client GUI on port {port}...")
    start_client_gui(ip, port)

if __name__ == "__main__":
    main()
