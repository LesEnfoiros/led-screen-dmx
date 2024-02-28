from .screen import BASE_PYTHON_FOLDER
import threading
import socket
import time
import os

# Constants.
BASE_PATH = os.path.join(BASE_PYTHON_FOLDER, "../service")

# Variables.
THREAD = None
PORT = None
SOCK = None


# Get the path of the file identifying the
# port number for the current script.
def _get_file_name():
    return os.path.join(BASE_PATH, str(PORT) + ".socket")


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

    print("end of thread")

def manage_order(screen, ascenseur, order: str):
    print("Order : %s" % order)

    if order.startswith('gif'):
        id = int(order.replace('gif', '').strip(' '))

        print("id: %d" % id)

    return "superbe command : " + str(order)
