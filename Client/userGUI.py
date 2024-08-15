import tkinter as tk
from tkinter import scrolledtext, messagebox
from client import main
import sys

class ChatBotGUI:
    def __init__(self, master, ip, port):
        self.master = master
        self.master.title("ChatBot Client")
        self.master.geometry("800x1000")
        self.master.resizable(False, False)

        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, font=("Helvetica", 14))
        self.text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.text_area.config(state=tk.DISABLED)


        input_frame = tk.Frame(self.master)
        input_frame.pack(padx=10, pady=10, fill=tk.X)


        self.entry_field = tk.Entry(input_frame, font=("Helvetica", 12))
        self.entry_field.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self.entry_field.bind("<Return>", self.on_enter_pressed)


        self.enter_button = tk.Button(input_frame, text="Enter", font=("Helvetica", 12), command=self.on_enter_pressed)
        self.enter_button.pack(side=tk.RIGHT)


        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(padx=10, pady=10, fill=tk.X)

        self.create_command_buttons()

        self.client = main(ip, port, self)  
        self.ready_for_messaging = False
        self.current_command = None
        self.ask_username()

    def create_command_buttons(self):
        """Create larger, user-friendly buttons for each command."""
        button_font = ("Helvetica", 12)

        self.disconnect_button = tk.Button(self.button_frame, text="Disconnect", font=button_font, command=self.disconnect, height=2)
        self.disconnect_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.help_button = tk.Button(self.button_frame, text="Help", font=button_font, command=self.send_help_command, height=2)
        self.help_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.users_button = tk.Button(self.button_frame, text="Users", font=button_font, command=self.send_users_command, height=2)
        self.users_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.pm_button = tk.Button(self.button_frame, text="Private Message", font=button_font, command=self.pm_command, height=2)
        self.pm_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.group_message_button = tk.Button(self.button_frame, text="Group Message", font=button_font, command=self.group_message_command, height=2)
        self.group_message_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.sendall_button = tk.Button(self.button_frame, text="Send to All", font=button_font, command=self.send_sendall_command, height=2)
        self.sendall_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.change_username_button = tk.Button(self.button_frame, text="Change Username", font=button_font, command=self.change_username, height=2)
        self.change_username_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

    def ask_username(self):
        """Ask for the username within the same GUI window."""
        self.display_message("Please enter your username:")
        self.show_entry_widgets()
        self.ready_for_messaging = False 

    def on_enter_pressed(self, event=None):
        """Handle Enter button press or Return key press."""
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)

        if not self.ready_for_messaging: 
            self.client.setupuser(message)
            self.ready_for_messaging = True
        # elif self.current_command == "/PM":
        #     self.handle_private_message(message)
        # elif self.current_command == "/GROUPMESSAGE":
        #     self.handle_group_message(message)
        else:
            self.send_message(str(message))

    def send_message(self, message):
        if message:
            self.display_message(f"You: {message}")
            self.client.interractwithserver(message)

    def display_message(self, message):
        """Display messages in the text area."""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.yview(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def show_entry_widgets(self):
        """Show the entry field and Enter button."""
        self.entry_field.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self.enter_button.pack(side=tk.RIGHT)

    def hide_entry_widgets(self):
        """Hide the entry field and Enter button."""
        self.entry_field.pack_forget()
        self.enter_button.pack_forget()

    def send_help_command(self):
        self.current_command = None
        self.send_message("/HELP")

    def send_users_command(self):
        self.current_command = None
        self.send_message("/USERS")

    def pm_command(self):
        self.current_command = None
        self.send_message("/PM")
        # self.display_message("Enter the username of the recipient and then the message.")

    def handle_private_message(self, message):
        """Handles private messaging logic."""
        self.current_command = None
        self.send_message("/PM")
        # if "@" not in message:
        #     self.display_message("Please use the format @username message to send a private message.")
        #     return
        # recipient, msg = message.split("@", 1)[1].strip().split(" ", 1)
        # self.send_message(f"/PM {recipient} {msg}")
        # self.current_command = None  # Reset the command state

    def group_message_command(self):
        self.current_command = None
        self.send_message("/GROUPMESSAGE")
        # self.current_command = "/GROUPMESSAGE"
        # self.display_message("Enter the usernames of the recipients (comma-separated) followed by the message.")

    # def handle_group_message(self, message):
    #     """Handles group messaging logic."""
    #     if ":" not in message:
    #         self.display_message("Please use the format username1, username2: message to send a group message.")
    #         return
    #     recipients, msg = message.split(":", 1)
    #     self.send_message(f"/GROUPMESSAGE {recipients.strip()} {msg.strip()}")
    #     self.current_command = None  # Reset the command state

    def send_sendall_command(self):
        self.current_command = None
        self.send_message("/SENDALL")

    def change_username(self):
        self.current_command = "/CHANGEUSERNAME"
        self.display_message("Enter your new username.")

    def disconnect(self):
        self.send_message("/DISCONNECT")
        self.master.quit()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.ready_for_messaging:
                self.send_message("/DISCONNECT")
            self.client.stop()
            self.master.destroy()

def run_gui(ip, port):
    root = tk.Tk()
    chat_gui = ChatBotGUI(root, ip, port)
    root.protocol("WM_DELETE_WINDOW", chat_gui.on_closing)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 chatbot_gui.py <IP> <Port>")
        sys.exit(1)
    ip = sys.argv[1]
    port = int(sys.argv[2])
    run_gui(ip, port)
