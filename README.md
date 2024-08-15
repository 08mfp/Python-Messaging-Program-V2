# Python Messaging Program

This Python Messaging Program allows multiple clients to connect to a central server and exchange messages using a set of predefined commands. The program is built using Python and features a graphical user interface (GUI) created with `customtkinter`.

## Table of Contents

- [File Structure](#file-structure)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
  - [Step 1: Navigate to the Root Directory](#step-1-navigate-to-the-root-directory)
  - [Step 2: Create a Virtual Environment](#step-2-create-a-virtual-environment)
    - [On macOS](#on-macos)
    - [On Windows](#on-windows)
  - [Step 3: Install `customtkinter`](#step-3-install-customtkinter)
- [Running the Program](#running-the-program)
  - [To Run the Server and the First Messaging Client](#to-run-the-server-and-the-first-messaging-client)
  - [To Run Additional Clients](#to-run-additional-clients)
- [Features](#features)
  - [Server](#server)
  - [Client](#client)
- [Available Commands](#available-commands)

## File Structure

```
.
├── Client
│   ├── client.py
│   └── userGUI.py
├── Server
│   ├── baseServer.py
│   ├── mainServerHub.py
│   ├── serverGUI.py
│   ├── serverInit.py
│   └── extraClients.py
├── README.md
└── runServer.py
```

## Requirements

- Python 3.x
- `customtkinter` library

## Setup Instructions

### Step 1: Navigate to the Root Directory

Open your terminal and navigate to the root directory of the project.

### Step 2: Create a Virtual Environment

#### On macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install `customtkinter`

With your virtual environment activated, install the required library:

```bash
pip install customtkinter
```

## Running the Program

### To Run the Server and the First Messaging Client

1. **Ensure your virtual environment is activated** (refer to Step 2).
2. Run the following command to start the server and the first client:

   ```bash
   python3 runServer.py
   ```

### To Run Additional Clients

1. **Ensure your virtual environment is activated** (refer to Step 2).
2. Open a new terminal window in the root directory.
3. Run the following command to start an additional client:

   ```bash
   python3 extraClients.py
   ```

## Features

### Server
- Listens for client connections and handles messages.
- Provides hooks for handling events such as connection, disconnection, and message reception.
- Supports multiple clients simultaneously.

### Client
- Connects to the server and communicates using a set of predefined commands.
- Allows private messaging, group messaging, and broadcasting messages to all connected clients.
- Supports changing the username and retrieving the list of connected users.

## Available Commands

Clients can use the following commands to interact with the server and other users:

- **/DISCONNECT**: Disconnect from the server.
- **/HELP**: Display a list of available commands.
- **/USERS**: List all currently connected users.
- **/PM <username>**: Send a private message to a specific user.
- **/GROUPMESSAGE <username1, username2, ...>**: Send a message to a group of users.
- **/SENDALL**: Send a message to all users (including the server).
- **/CHANGEUSERNAME <new_username>**: Change your username.
