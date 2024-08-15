import tkinter as tk
from tkinter import messagebox
import sys

try:
    import customtkinter as ctk
    use_ctk = True
except ImportError:
    ctk = tk  # fallback to standard tkinter
    use_ctk = False

from client import main

class ChatBotGUI:
    def __init__(self, master, ip, port):
        self.master = master
        self.master.title("Messaging Program")
        self.master.geometry("500x1000")
        self.master.resizable(True, True)

        self.top_button_frame = ctk.Frame(self.master) if not use_ctk else ctk.CTkFrame(self.master)
        self.top_button_frame.pack(padx=10, pady=(10, 0), fill="x")

        self.create_top_buttons()

        self.text_area_frame = ctk.Frame(self.master, borderwidth=2, relief="solid") if not use_ctk else ctk.CTkFrame(self.master, border_width=2, border_color="white")
        self.text_area_frame.pack(padx=10, pady=10, expand=True, fill="both")

        self.text_area = tk.Text(self.text_area_frame, wrap="word", font=("Helvetica", 18), height=20) if not use_ctk else ctk.CTkTextbox(self.text_area_frame, wrap="word", font=("Helvetica", 18), height=20)
        self.text_area.pack(padx=2, pady=2, expand=True, fill="both")
        self.text_area.configure(state="disabled")

        input_frame = ctk.Frame(self.master) if not use_ctk else ctk.CTkFrame(self.master)
        input_frame.pack(padx=10, pady=10, fill="x")

        self.entry_field = tk.Entry(
            input_frame,
            font=("Helvetica", 14),
            relief="solid",
            fg="black",
            bg="white",
            width=40
        ) if not use_ctk else ctk.CTkEntry(
            input_frame,
            font=("Helvetica", 14),
            border_width=3,
            fg_color="white",
            border_color="#0066CC",
            text_color="black",
            height=40
        )
        self.entry_field.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.entry_field.bind("<Return>", self.on_enter_pressed)

        self.enter_button = tk.Button(
            input_frame,
            text="Enter",
            font=("Helvetica", 14, "bold"),
            command=self.on_enter_pressed,
            height=2
        ) if not use_ctk else ctk.CTkButton(
            input_frame,
            text="Enter",
            font=("Helvetica", 14, "bold"),
            command=self.on_enter_pressed,
            height=40
        )
        self.enter_button.pack(side="right")

        self.bottom_button_frame_top = ctk.Frame(self.master) if not use_ctk else ctk.CTkFrame(self.master)
        self.bottom_button_frame_top.pack(padx=10, pady=(10, 0), anchor="s", fill="x")

        self.bottom_button_frame_bottom = ctk.Frame(self.master) if not use_ctk else ctk.CTkFrame(self.master)
        self.bottom_button_frame_bottom.pack(padx=10, pady=(10, 20), anchor="s", fill="x")

        self.create_command_buttons()

        self.client = main(ip, port, self)
        self.ready_for_messaging = False
        self.current_command = None
        self.ask_username()

    def create_top_buttons(self):
        """Create Disconnect and Help buttons for the top of the GUI."""
        button_font = ("Helvetica", 16, "bold")

        button_params = {
            "font": button_font,
            "height": 50,
        }

        self.disconnect_button = tk.Button(self.top_button_frame, text="Disconnect", bg="red", **button_params, command=self.disconnect) if not use_ctk else ctk.CTkButton(self.top_button_frame, text="Disconnect", fg_color="red", **button_params, command=self.disconnect)
        self.disconnect_button.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        self.help_button = tk.Button(self.top_button_frame, text="Help", bg="green", **button_params, command=self.send_help_command) if not use_ctk else ctk.CTkButton(self.top_button_frame, text="Help", fg_color="green", **button_params, command=self.send_help_command)
        self.help_button.pack(side="right", padx=5, pady=5, expand=True, fill="x")

    def create_command_buttons(self):
        """Create Private Message, Group Message, Send to All, Change Username buttons."""
        button_font = ("Helvetica", 16, "bold")

        button_params = {
            "font": button_font,
            "height": 50,
        }

        self.pm_button = tk.Button(self.bottom_button_frame_top, text="Private Message", bg="#3399FF", **button_params, command=self.pm_command) if not use_ctk else ctk.CTkButton(self.bottom_button_frame_top, text="Private Message", fg_color="#3399FF", **button_params, command=self.pm_command)
        self.pm_button.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        self.group_message_button = tk.Button(self.bottom_button_frame_top, text="Group Message", bg="#3399FF", **button_params, command=self.group_message_command) if not use_ctk else ctk.CTkButton(self.bottom_button_frame_top, text="Group Message", fg_color="#3399FF", **button_params, command=self.group_message_command)
        self.group_message_button.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        self.sendall_button = tk.Button(self.bottom_button_frame_top, text="Send to All", bg="#3399FF", **button_params, command=self.send_sendall_command) if not use_ctk else ctk.CTkButton(self.bottom_button_frame_top, text="Send to All", fg_color="#3399FF", **button_params, command=self.send_sendall_command)
        self.sendall_button.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        self.users_button = tk.Button(self.bottom_button_frame_bottom, text="Users", bg="orange", **button_params, command=self.send_users_command) if not use_ctk else ctk.CTkButton(self.bottom_button_frame_bottom, text="Users", fg_color="orange", **button_params, command=self.send_users_command)
        self.users_button.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        self.change_username_button = tk.Button(self.bottom_button_frame_bottom, text="Change Username", bg="orange", **button_params, command=self.change_username) if not use_ctk else ctk.CTkButton(self.bottom_button_frame_bottom, text="Change Username", fg_color="orange", **button_params, command=self.change_username)
        self.change_username_button.pack(side="left", padx=5, pady=5, expand=True, fill="x")

    def ask_username(self):
        """Ask for the username within the same GUI window."""
        self.show_entry_widgets()
        self.ready_for_messaging = False

    def on_enter_pressed(self, event=None):
        """Handle Enter button press or Return key press."""
        message = self.entry_field.get()
        self.entry_field.delete(0, "end")

        if not self.ready_for_messaging:
            self.client.setupuser(message)
            self.ready_for_messaging = True
        else:
            self.send_message(str(message))

    def send_message(self, message):
        if message:
            self.display_message(f"You: {message}")
            self.client.interractwithserver(message)

    def display_message(self, message):
        """Display messages in the text area."""
        self.text_area.configure(state="normal")
        self.text_area.insert("end", message + "\n")
        self.text_area.yview("end")
        self.text_area.configure(state="disabled")

    def show_entry_widgets(self):
        """Show the entry field and Enter button."""
        self.entry_field.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.enter_button.pack(side="right")

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

    def group_message_command(self):
        self.current_command = None
        self.send_message("/GROUPMESSAGE")

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
    try:
        if use_ctk:
            ctk.set_appearance_mode("Dark")
            ctk.set_default_color_theme("dark-blue")
    except AttributeError:
        pass

    root = ctk.CTk() if use_ctk else tk.Tk()
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
