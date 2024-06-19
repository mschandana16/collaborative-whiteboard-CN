# Collaborative Whiteboard

This project consists of a client-server architecture enabling multiple clients to collaborate on a shared whiteboard in real time using Python's sockets and SSL/TLS encryption. The server manages client connections, handles client activity, and broadcasts drawing commands to all connected clients. The client-side provides a graphical user interface (GUI) built with Tkinter, allowing users to draw, select colours, adjust brush thickness, and perform undo and redo actions.

## Features

- **Secure Communication:** SSL/TLS encryption ensures secure communication between the server and clients, protecting data integrity and confidentiality.
- **Real-time Collaboration:** Clients can draw simultaneously on a shared whiteboard, with changes/edits instantly propagated to all connected clients.
- **Clear/Undo/Redo Functionality:** Users can easily erase the entire canvas or undo/redo individual drawing actions to correct mistakes or revert changes.
- **Color Selection and Brush Thickness:** Interactive colour pickers and adjustable brush thickness enhance drawing capabilities and user experience.
- **Client Disconnect Handling:** The server gracefully handles client disconnections and removes inactive clients from the active client list.

## Commands to be run

1. ### Start the Server
Open a terminal and run the following command to start the server:

`python server.py`

2. ### Start the Client(s)
Open another terminal (multiple such client terminals may be opened) and run the following command to start a client:

`python client.py`

## Usage

1. **Start the Server:** Run the server script to initialize the server and start listening for client connections.
2. **Start the Client(s):** Run the client script on multiple terminals or machines to connect to the server and collaborate on the shared whiteboard.
3. **Draw and Collaborate:** Use the drawing tools provided in the client GUI to draw, select colours, adjust brush thickness, and perform undo/redo actions in real time with other connected clients.

