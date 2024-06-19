# Collaborative Whiteboard

This project consists of a client-server architecture enabling multiple clients to collaborate on a shared whiteboard in real time using Python's sockets and SSL/TLS encryption. The server-side manages client connections, handles client activity, and broadcasts drawing commands to all connected clients. The client-side provides a graphical user interface (GUI) built with Tkinter, allowing users to draw, select colours, adjust brush thickness, and perform undo and redo actions.

## Features

- **Secure Communication:** SSL/TLS encryption ensures secure communication between the server and clients, protecting data integrity and confidentiality.
- **Real-time Collaboration:** Clients can draw simultaneously on a shared whiteboard, with changes/edits instantly propagated to all connected clients.
- **Clear/Undo/Redo Functionality:** Users can easily erase the entire canvas or undo/redo individual drawing actions to correct mistakes or revert changes.
- **Color Selection and Brush Thickness:** Interactive colour pickers and adjustable brush thickness enhance drawing capabilities and user experience.
- **Client Disconnect Handling:** The server gracefully handles client disconnections and removes inactive clients from the active client list.

## Commands to Run

### Start the Server

Open a terminal and run the following command to start the server:

```bash
python ssl_server.py
