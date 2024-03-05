import socket
import threading
import time
import ssl

HOST = 'localhost'
PORT = 5050
INACTIVITY_TIMEOUT = 30

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('certificate.crt', 'privateKey.key')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server_active = True

clients = []
clients_lock = threading.Lock()

def handle_client(client, address): #broadcast messages if client is there
    global server_active
    while server_active:
        try:
            data = client.recv(1024).decode()
            if not data:
                break
            with clients_lock:
                for c in clients:
                    c.sendall(data.encode())
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Error handling client {address}: {e}")
            break

    with clients_lock:
        if client in clients:
            clients.remove(client)
    print(f"Client {address} disconnected.")
    client.close()

def start_server(): #start server, create threads for individual clients
    global server_active
    server.listen()
    print(f'Server is listening on {HOST}:{PORT}')

    while server_active: 
        try:
            server.settimeout(1) 
            client, address = server.accept()
            server.settimeout(None)  
            print(f'Connection established with {address}')
            ssl_client = context.wrap_socket(client, server_side=True)
            with clients_lock:
                clients.append(ssl_client)
            thread = threading.Thread(target=handle_client, args=(ssl_client, address), daemon=True)
            thread.start()
        except socket.timeout:
            pass  
        except Exception as e:
            if server_active:
                print(f"Error accepting connection: {e}")
            break
    server.close()

def monitor_activity(): #check for clients, or close server
    global server_active
    global clients
    while server_active:
        time.sleep(INACTIVITY_TIMEOUT)
        with clients_lock:
            if not clients:
                print(f"No clients connected for {INACTIVITY_TIMEOUT} seconds. Shutting down server.")
                server_active = False
                exit()

server_thread = threading.Thread(target=start_server, daemon=True) #starts threading of server
activity_thread = threading.Thread(target=monitor_activity, daemon=True) #checks for clients, otherwise shuts it

server_thread.start()
activity_thread.start()

server_thread.join()
activity_thread.join()