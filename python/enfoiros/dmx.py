import wiringpi as wp
import threading
import time

# GLOBAL DMX VARIABLES.
DMX_I2C_ID           = 0x08
DMX_CHANNEL_COLOR_R  = 0
DMX_CHANNEL_COLOR_G  = 1
DMX_CHANNEL_COLOR_B  = 2
DMX_CHANNEL_ONOFF    = 3
DMX_CHANNEL_BULLSHIT = 4
DMX_CHANNEL_ORDER    = 5

# Variables.
dmx_fd = None
dmx_values = {}
_thread_should_run = True

# Make a connection with the I2C client.
def connect():
    global dmx_fd

    # Initialiser WiringPi
    wp.wiringPiSetup()

    # Ouvrir une connexion I2C
    dmx_fd = wp.wiringPiI2CSetup(DMX_I2C_ID)

    if dmx_fd == -1:
        print("Erreur lors de l'ouverture de la connexion I2C")
        exit()

# Start the thread listening the DMX values.
def start():
    thread = threading.Thread(target=_thread)
    thread.start()

# Stop the thread.
def stop():
    global _thread_should_run
    _thread_should_run = False

# GEt the value from the registries.
def get(channel: int):
    return dmx_values[channel]

# Read a value from the i2c.
def _update_channel_value_from_i2c(channel: int):
    global dmx_values

    # Send the order to the I2C client to 
    # prepare the value of the given channel.
    wp.wiringPiI2CWrite(dmx_fd, channel)

    # Put the value in a buffer.
    dmx_values[channel] = wp.wiringPiI2CRead(dmx_fd)

# Thread internal function.
def _thread():
    # Lire des données depuis le périphérique I2C
    while(_thread_should_run):
        print("Iteration")
        _update_channel_value_from_i2c(DMX_CHANNEL_COLOR_R)
        _update_channel_value_from_i2c(DMX_CHANNEL_COLOR_G)
        _update_channel_value_from_i2c(DMX_CHANNEL_COLOR_B)
        _update_channel_value_from_i2c(DMX_CHANNEL_ONOFF)
        _update_channel_value_from_i2c(DMX_CHANNEL_BULLSHIT)
        _update_channel_value_from_i2c(DMX_CHANNEL_ORDER)

        time.sleep(0.5)

    # Close the I2C connection.
    wp.wiringPiI2CClose(dmx_fd)
    print("DMX thread stopped")
