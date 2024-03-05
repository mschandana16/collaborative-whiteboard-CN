import socket
import threading
import ssl
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
import tkinter as tk
import os
import sys

HOST = 'localhost'
PORT = 5050

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('certificate.crt') 
context.check_hostname = False

try:
    client = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=HOST)
    client.connect((HOST, PORT))
except ConnectionRefusedError:
    print("Server is not active. Cannot Connect.")
    sys.exit(1)

root = Tk()
root.title("Collaborative Whiteboard")
root.geometry("810x530+150+50")
root.configure(bg="#f2f3f5")
root.resizable(False, False)
start_x = None
start_y = None
color = 'black'
lines = []
removed_lines = []
brush_thickness = 2

def send_coords(event):
    try:
        global start_x, start_y, color, brush_thickness
        x, y = event.x, event.y
        if start_x is not None and start_y is not None:
            coords_color_thickness = f'{start_x},{start_y},{x},{y},{color},{brush_thickness}'
            message = f"{len(coords_color_thickness):<1024}" + coords_color_thickness
            client.sendall(message.encode())
            start_x, start_y = x, y
            lines.append(canvas.create_line(start_x, start_y, x, y, width=brush_thickness, fill=color,capstyle=ROUND,smooth=TRUE))
    except ConnectionResetError as e:
        print(f"Connection reset by server: {e}")
    except Exception as e:
        print(f"Error sending coordinates: {e}")

def receive_messages():
    while True:
        try:
            length_prefix = client.recv(1024).decode().strip()
            if length_prefix == 'CLEAR' or length_prefix == 'UNDO' or length_prefix == 'REDO':
                handle_special_command(length_prefix)
            else:
                message_length = int(length_prefix)
                data = client.recv(message_length).decode()
                handle_drawing_command(data)
        except Exception as e:
            print("Server is not active. Exiting client.")
            os._exit(1)

def handle_drawing_command(data):
    try:
        coords_color_thickness = data.split(',')
        x1, y1, x2, y2 = map(int, coords_color_thickness[:4])
        received_color = coords_color_thickness[4]
        received_thickness = int(coords_color_thickness[5])
        line_id = canvas.create_line(x1, y1, x2, y2, width=received_thickness, fill=received_color, capstyle=ROUND, smooth=TRUE)
        lines.append(line_id)
    except Exception as e:
        print(f"Error handling drawing command: {e}")

def handle_special_command(command):
    try:
        if command == 'CLEAR':
            canvas.delete('all')
            lines.clear()
            display_palette()
        elif command == 'UNDO':
            if lines:
                last_item = lines.pop()
                line_coords = canvas.coords(last_item)  # Get coordinates of the line
                line_color = canvas.itemcget(last_item, "fill")  # Get color of the line
                line_thickness = canvas.itemcget(last_item, "width")  # Get thickness of the line
                removed_lines.append((last_item, line_coords, line_color, line_thickness))
                canvas.delete(last_item)       
        elif command == 'REDO':
            if removed_lines:
                line_to_restore = removed_lines.pop()  # Get the properties of the line
                new_line_id = canvas.create_line(line_to_restore[1], width=line_to_restore[3], fill=line_to_restore[2], capstyle=ROUND)
                lines.append(new_line_id)
        
    except Exception as e:
        print(f"Error handling special command: {e}")

def start_draw(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def stop_draw(event):
    global start_x, start_y
    start_x, start_y = None, None

def show_color(new_color):
    global color
    color = new_color

def clear_canvas():
    canvas.delete('all')
    lines.clear()
    display_palette()
    client.sendall(b'CLEAR')

def undo():
    if lines:
        last_item = lines.pop()  # Remove the last drawn line
        line_coords = canvas.coords(last_item)  # Get coordinates of the line
        line_color = canvas.itemcget(last_item, "fill")  # Get color of the line
        line_thickness = canvas.itemcget(last_item, "width")  # Get thickness of the line
        removed_lines.append((last_item, line_coords, line_color, line_thickness))  # Store line properties
        canvas.delete(last_item)
        client.sendall(b'UNDO')

def redo():
    if removed_lines:
        line_to_restore = removed_lines.pop()  # Get the properties of the line
        new_line_id = canvas.create_line(line_to_restore[1], width=line_to_restore[3], fill=line_to_restore[2], capstyle=ROUND)
        lines.append(new_line_id)
        client.sendall(b'REDO')
        
def open_color_picker():
    global color
    new_color = askcolor()[1]
    if new_color:
        color = new_color
        
colors=Canvas(root, bg="#ffffff", width=40, height=340, bd=0)
colors.place(x=30, y=10)

def display_palette():
    colors_list = ['black', 'grey', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink','white']
    for i, color in enumerate(colors_list):
        id = colors.create_rectangle((12, 10 + i * 30, 32, 30 + i * 30), fill=color)
        colors.tag_bind(id, '<Button-1>', lambda x, color=color: show_color(color))

def get_current_value():
    return '{: .2f}'.format(current_value.get())

def update_brush_thickness(value):
    global brush_thickness
    brush_thickness = round(float(value))

Button(root, text="Choose Color", bg="#f2f3f5", command=open_color_picker).place(x=10, y=360)
Button(root, text="Undo", bg="#f2f3f5", command=undo).place(x=5, y=400)
Button(root, text="Redo", bg="#f2f3f5", command=redo).place(x=55, y=400)
Button(root, text="Clear", bg="#f2f3f5", command=clear_canvas).place(x=30, y=440)

canvas = Canvas(root, width=700, height=510, background="white", cursor="cross")
canvas.place(x=100, y=10)
canvas.bind('<Button-1>', start_draw)
canvas.bind('<B1-Motion>', send_coords)
canvas.bind('<ButtonRelease-1>', stop_draw)
display_palette()
current_value=tk.DoubleVar()
slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', variable=current_value, command=update_brush_thickness)
slider.place(x=1, y=480)
value_label = ttk.Label(root, text=get_current_value())
value_label.place(x=15, y=500)

def on_closing():
    root.destroy()  
    print("Client disconnecting.")
    client.close() 
    os._exit(0) #send msg to server when client is closed

root.protocol("WM_DELETE_WINDOW", on_closing) 

receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start() #recieves data from other clientc

root.mainloop()