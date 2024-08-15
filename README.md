
# Network Server and Client

This project demonstrates a basic network server and client implementation in Python. The server listens on a specified IP address and TCP port, handling incoming messages from multiple clients. Clients can connect to the server, send messages, and interact with other connected clients using a variety of commands.

## Features

- **Server**:
  - Listens for client connections and handles messages.
  - Provides hooks for handling events such as connection, disconnection, and message reception.
  - Supports multiple clients simultaneously.

- **Client**:
  - Connects to the server and communicates with it using a set of predefined commands.
  - Allows private messaging, group messaging, and broadcasting messages to all connected clients.
  - Supports changing the username and retrieving the list of connected users.

## Usage

### Running the Server

To start the server, use the following command:

```bash
python3 myserver.py <IP> <Port>
```

For example:

```bash
python3 myserver.py localhost 7090
```

### Running the Client

To connect to the server using the client, run the following command in a new terminal:

```bash
python3 myclient.py <IP> <Port>
```

For example:

```bash
python3 myclient.py localhost 7090
```

### Typical Client Usage

1. **Username Setup**: When you start the client, you'll be prompted to enter a username. If the username is already in use, you'll need to choose a different one.
2. **Messaging**: Once your username is set, you can start sending messages using the following commands:

   - `/DISCONNECT` - Disconnect from the server.
   - `/HELP` - Display a list of available commands.
   - `/USERS` - List all currently connected users.
   - `/PM <username>` - Send a private message to a specific user.
   - `/GROUPMESSAGE <username1, username2, ...>` - Send a message to a group of users.
   - `/SENDALL` - Send a message to all users (including the server).
   - `/CHANGEUSERNAME <new_username>` - Change your username.

3. **Connecting Multiple Clients**: You can run multiple instances of the client in separate terminals, each connecting with a unique username.
4. **Disconnecting**: To disconnect, use the `/DISCONNECT` command. The client will then exit.

### Telnet Connection

You can also use `telnet` to connect to the server:

```bash
telnet localhost <Port>
```

For example:

```bash
telnet localhost 7090
```

### Additional Information

- Commands are not case-sensitive (`/sendall` or `/SENDALL` are both valid).
- The server displays all messages and commands entered by clients.
- **Note**: Pressing `Ctrl + ]` and `Ctrl + Z` in a telnet client suspends it without disconnecting from the server. Use the `/DISCONNECT` command to properly terminate the connection.

## Testing

To test the implementation:

1. Start the server in a terminal.
2. Connect multiple clients from separate terminals using different usernames.
3. Use the available commands to interact between clients and the server.
4. Test private messaging, group messaging, and broadcasting.
5. Verify that the `/USERS` command lists all connected clients.
6. Change usernames using `/CHANGEUSERNAME` and verify the changes.
7. Disconnect all clients using `/DISCONNECT`.
8. Stop the server by pressing `Ctrl + C` twice in the server terminal.
