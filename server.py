import socket
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
import tkinter as tk
import threading

# Define the host and port
HOST = '192.168.0.175'
PORT = 5050

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Create Tkinter root window
root = Tk()
root.title("Collaborative Whiteboard")
root.geometry("810x530+150+50")
root.configure(bg="#f2f3f5")
root.resizable(False, False)
start_x = None
start_y = None
color = 'black'
lines = []
brush_thickness = 2

def send_coords(event):
    try:
        global start_x, start_y, color, brush_thickness
        x, y = event.x, event.y
        if start_x is not None and start_y is not None:
            coords_color_thickness = f'{start_x},{start_y},{x},{y},{color},{brush_thickness}'
            # Prefix the message with its length
            message = f"{len(coords_color_thickness):<10}" + coords_color_thickness
            client.sendall(message.encode())
            start_x, start_y = x, y
            lines.append(canvas.create_line(start_x, start_y, x, y, width=brush_thickness, fill=color,capstyle=ROUND,smooth=TRUE))
    except ConnectionResetError as e:
        print(f"Connection reset by server: {e}")
    except Exception as e:
        print(f"Error sending coordinates: {e}")

# Function to receive drawing coordinates, color, and brush thickness from the server and draw on the canvas
# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            # Receive the length-prefixed message
            length_prefix = client.recv(10).decode().strip()
            if length_prefix:
                # Check if the message is a special command
                if length_prefix == 'CLEAR' or length_prefix == 'UNDO':
                    handle_special_command(length_prefix)
                else:
                    message_length = int(length_prefix)
                    data = client.recv(message_length).decode()
                    handle_drawing_command(data)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Function to handle regular drawing commands
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

# Function to handle special commands like 'UNDO' and 'CLEAR'
def handle_special_command(command):
    try:
        if command == 'CLEAR':
            # Clear the canvas locally
            canvas.delete('all')
            lines.clear()
            display_palette()
        elif command == 'UNDO':
            # Perform undo action locally
            if lines:
                last_item = lines.pop()
                canvas.delete(last_item)
    except Exception as e:
        print(f"Error handling special command: {e}")

# Define callbacks for drawing and color selection
def start_draw(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def stop_draw(event):
    global start_x, start_y
    start_x, start_y = None, None

def show_color(new_color):
    global color
    color = new_color

# Function to clear the canvas
def clear_canvas():
    canvas.delete('all')
    lines.clear()
    display_palette()
    client.sendall(b'CLEAR')

def undo():
    if lines:
        last_item = lines.pop()  # Remove the last drawn line
        canvas.delete(last_item)
        client.sendall(b'UNDO')

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
   
# Function to update the brush thickness
def update_brush_thickness(value):
    global brush_thickness
    brush_thickness = round(float(value))


Button(root, text="Choose Color", bg="#f2f3f5", command=open_color_picker).place(x=10, y=360)
Button(root, text="Clear", bg="#f2f3f5", command=clear_canvas).place(x=30, y=400)
Button(root, text="Undo", bg="#f2f3f5", command=undo).place(x=30, y=440)

# Create the drawing canvas
canvas = Canvas(root, width=700, height=510, background="white", cursor="cross")
canvas.place(x=100, y=10)
canvas.bind('<Button-1>', start_draw)
canvas.bind('<B1-Motion>', send_coords)
canvas.bind('<ButtonRelease-1>', stop_draw)
display_palette()
current_value=tk.DoubleVar()
slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', variable=current_value, command=update_brush_thickness)
slider.place(x=1, y=480)

# Start a thread to receive drawing coordinates from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.mainloop()