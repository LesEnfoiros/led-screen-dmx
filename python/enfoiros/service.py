from . import dmx as DMX
import threading
import socket
import time
import os

# Variables.
THREAD = None
PORT = None
SOCK = None

# Get the path of the file identifying the
# port number for the current script.
def _get_file_name():
    return "/tmp/" + str(PORT) + ".socket"


# Start the thread listening the DMX values.
def start(screen, ascenseur):
    global THREAD

    _create_socket()
    THREAD = threading.Thread(target=_thread, args=(screen, ascenseur))
    THREAD.start()


# Stop the thread.
def stop():
    # This will stop the thread.
    SOCK.shutdown(2)

    # If there is no port, then stop here.
    if PORT is None:
        return

    # To clean up the code, we remove the previous socket file.
    file_path = _get_file_name()
    if os.path.isfile(file_path):
        os.remove(file_path)


# Create the socket instance.
def _create_socket():
    global PORT, SOCK

    # Build the socket.
    SOCK = socket.socket()

    # Bind it to port 0, so that it takes a random port number.
    SOCK.bind(('', 0))

    # Get the port number.
    PORT = SOCK.getsockname()[1]

    # Then, create a file in the service folder to
    # be able to communicate with the python script.
    open(_get_file_name(), 'a').close()
    
    # Display the listening port.
    print("Start listening on port %d" % PORT)


# Main thread function.
def _thread(screen, ascenseur):
    global SOCK
    SOCK.listen(1)

    # We do this as long as the service is running.
    while True:
        try:
            conn, addr = SOCK.accept()
        except OSError:
            break
        
        data = conn.recv(1024)

        # If there is no data, close the connection.
        if not data: 
            continue

        order = data.decode('utf-8').replace("\n", "").strip(' ')

        response = manage_order(screen, ascenseur, order)
        conn.sendall(str(response + "\n").encode())
        time.sleep(1)
        conn.close()

    print("[END] End of service thread")


# Clean the input received from the command line.
def _clean_order(type, order: str):
    return int(order.replace(type, '').strip(' '))
    

# Manage the order coming from the command line.
def manage_order(screen, ascenseur, order: str):
    # If we received a GIF order.
    if order.startswith('bullshit'):
        DMX.set_static_value(DMX.DMX_CHANNEL_BULLSHIT, _clean_order('bullshit', order))

    # If the received an order to go to a specific stair.
    elif order.startswith('order'):
        DMX.set_static_value(DMX.DMX_CHANNEL_ORDER, _clean_order('order', order))
        DMX.set_static_value(DMX.DMX_CHANNEL_COLOR_R, 255)
        DMX.set_static_value(DMX.DMX_CHANNEL_COLOR_G, 255)
        DMX.set_static_value(DMX.DMX_CHANNEL_COLOR_B, 255)

    return "Executed command: " + str(order)
