# collaborative-whiteboard

This project consists of a client-server architecture enabling multiple clients to collaborate on a shared whiteboard in real time using Python's sockets and SSL/TLS encryption. The server-side manages client connections, handles client activity, and broadcasts drawing commands to all connected clients. The client-side provides a graphical user interface (GUI) built with Tkinter, allowing users to draw, select colours, adjust brush thickness, and perform undo and redo actions.

### Features
1. Secure Communication: SSL/TLS encryption ensures secure communication between the server and clients, protecting data integrity and confidentiality.
2. Real-time Collaboration: Clients can draw simultaneously on a shared whiteboard, with changes/edits instantly propagated to all connected clients.
3. Clear/Undo/Redo Functionality: Users can easily erase the entire canvas or undo/redo individual drawing actions to correct mistakes or revert changes.
4. Color Selection and Brush Thickness: Interactive color pickers and adjustable brush thickness enhance drawing capabilities and user experience.
5. Client Disconnect Handling: The server gracefully handles client disconnections and removes inactive clients from the active client list.

### Commands to be run:
In one terminal: `python ssl_server.py`
In another terminal (multiple such client terminals can be made use of): `python ssl_client.py`
