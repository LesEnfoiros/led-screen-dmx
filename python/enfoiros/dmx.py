import wiringpi as wp
from .gif import Gif
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

# Manage the orders coming from the DMX regarding
# where the ascenseur should go.
def _manage_order(ascenseur, order: int):
    # Upper stairs.
    if order >= 0 and order < 10:
        ascenseur.goToStair(5)
    elif order >= 10 and order < 20:
        ascenseur.goToStair(4)
    elif order >= 20 and order < 30:
        ascenseur.goToStair(3)
    elif order >= 30 and order < 40:
        ascenseur.goToStair(2)
    elif order >= 40 and order < 50:
        ascenseur.goToStair(1)
    elif order >= 50 and order < 60:
        ascenseur.goToStair(0)
    
    # Lower stairs.
    elif order >= 60 and order < 70:
        ascenseur.goToStair(-1)
    elif order >= 70 and order < 80:
        ascenseur.goToStair(-2)
    elif order >= 80 and order < 90:
        ascenseur.goToStair(-3)
    elif order >= 90 and order < 100:
        ascenseur.goToStair(-4)
    elif order >= 100 and order < 110:
        ascenseur.goToStair(-5)
    
    # HS animation.
    elif order >= 110 and order < 120:
        ascenseur.is_hors_service = True
        ascenseur.current_stair = ascenseur.target_stair


def _manage_bullshit(screen, ascenseur, order: int):
    print("bullshit")
    new_gif = None

    # Upper stairs.
    if order >= 10 and order < 20:
        print("GYROPHARE")
        new_gif = Gif.build(screen, "assets/gif/gyrophare.gif", 10)
    elif order >= 20 and order < 30:
        print("OSS117")
        new_gif = Gif.build(screen, "assets/gif/oss117.gif", 5)

    if new_gif is not None and (screen.bullshit is None or (new_gif.path != screen.bullshit.path)): 
        print("JE REMPLACE")
        screen.bullshit = new_gif


def manage(screen, ascenseur):
    # Update the global color.
    #screen.text_color.red = get(DMX_CHANNEL_COLOR_R)
    #screen.text_color.green = get(DMX_CHANNEL_COLOR_G)
    #screen.text_color.blue = get(DMX_CHANNEL_COLOR_B)

    # Manage the orders for the ascenseur.
    order = get(DMX_CHANNEL_ORDER)
    print(order)
    if order > 0:
        #screen.bullshit = None
        _manage_bullshit(screen, ascenseur, order)
        #_manage_order(ascenseur, order)

        return

    # Display the bullshit if needed.
    bullshit = get(DMX_CHANNEL_BULLSHIT)
    if order > 0:
        _manage_bullshit(screen, ascenseur, order)

        return
