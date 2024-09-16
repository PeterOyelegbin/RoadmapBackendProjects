# [Broadcast Server CLI](https://roadmap.sh/projects/broadcast-server).
You are required to create a simple broadcast server that will allow clients to connect to it, send messages that will be broadcasted to all connected clients. The goal of this project is to help you understand how to work with websockets and implement real-time communication between clients and servers. This will help you understand how the real-time features of applications like chat applications, live scoreboards, etc., work.


## Requirements
You are required to build a CLI based application that can be used to either start the server or connect to the server as a client. Here are the sample commands that you can use:
- broadcast-server start - This command will start the server.
- broadcast-server connect - This command will connect the client to the server.
When the server is started using the broadcast-server start command, it should listen for client connections on a specified port (you can configure that using command options or hardcode for simplicity). When a client connects and sends a message, the server should broadcast this message to all connected clients.

The server should be able to handle multiple clients connecting and disconnecting gracefully.

## Demo
[![Watch the video](https://img.youtube.com/vi/2wgb0G9moRE&list=PLTYOT9-XlEm4J6GfPJ_S-MKH4Pyq6Deir/maxresdefault.jpg)](https://www.youtube.com/watch?v=2wgb0G9moRE&list=PLTYOT9-XlEm4J6GfPJ_S-MKH4Pyq6Deir)


## Usage
### Install Dependencies
Open your teminal and enter the command below to install needed dependencies:
```bash
pip install websockets
```

### Start the Server
To start the broadcast server, use the command below:
```bash
python broadcast-server.py start
```

### Coonect to the Server
Open a new terminal and enter the command below to connect to the server already running as shown below:
```bash
python broadcast-server.py connect
```
