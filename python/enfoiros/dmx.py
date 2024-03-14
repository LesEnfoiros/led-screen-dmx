import wiringpi as wp
from .gif import Gif
from .image import Image
import threading
import time

# GLOBAL DMX VARIABLES.
DMX_I2C_ID           = 0x08
DMX_CHANNEL_COLOR_R  = 0
DMX_CHANNEL_COLOR_G  = 1
DMX_CHANNEL_COLOR_B  = 2
#DMX_CHANNEL_ONOFF    = 3
DMX_CHANNEL_ORDER    = 3
DMX_CHANNEL_BULLSHIT = 4

# Variables.
dmx_fd = None
dmx_values = {}
dmx_static_values = {} # Used to manually set values to the DMX fields.
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


# Get the value from the registries.
def get(channel: int):
    if channel in dmx_static_values and dmx_static_values[channel] is not None:
        return dmx_static_values[channel]
    
    return 0 if not channel in dmx_values else dmx_values[channel]


# Set a static value to the DMX channel to interact
# with the ascenseur from the command line.
def set_static_value(channel: int, value = None):
    dmx_static_values[channel] = value


# Read a value from the i2c.
def _update_channel_value_from_i2c(channel: int):
    global dmx_values

    # Send the order to the I2C client to 
    # prepare the value of the given channel.
    wp.wiringPiI2CWrite(dmx_fd, channel)

    # Put the value in a buffer.
    dmx_values[channel] = wp.wiringPiI2CRead(dmx_fd)

    # We reset the static values if a real value was
    # received from DMX.
    if dmx_values[channel] > 0 and channel in dmx_static_values and dmx_static_values[channel] is not None:
        dmx_static_values[channel] = None


# Thread internal function.
def _thread():
    # Lire des données depuis le périphérique I2C
    while(_thread_should_run):
        _update_channel_value_from_i2c(DMX_CHANNEL_COLOR_R)
        _update_channel_value_from_i2c(DMX_CHANNEL_COLOR_G)
        _update_channel_value_from_i2c(DMX_CHANNEL_COLOR_B)
        #_update_channel_value_from_i2c(DMX_CHANNEL_ONOFF)
        _update_channel_value_from_i2c(DMX_CHANNEL_BULLSHIT)
        _update_channel_value_from_i2c(DMX_CHANNEL_ORDER)

        time.sleep(0.2)

    print("[STOP] DMX thread stopped")

# Manage the orders coming from the DMX regarding
# where the ascenseur should go.
def _manage_order(ascenseur, screen, order: int):
    new_stair = None

    # If the ascenseur should be hidden, then
    # do nothing more than setting the value.
    # to the hide parameter.
    if order >= 0 and order < 10:
        ascenseur.hide = True
        return

    # If not, then the ascenseur should not hide.
    ascenseur.hide = False

    # Upper stairs.
    if order >= 10 and order < 20:
        new_stair = 9
    elif order >= 20 and order < 30:
        new_stair = 8
    elif order >= 30 and order < 40:
        new_stair = 7
    elif order >= 40 and order < 50:
        new_stair = 6
    elif order >= 50 and order < 60:
        new_stair = 5
    elif order >= 60 and order < 70:
        new_stair = 4
    elif order >= 70 and order < 80:
        new_stair = 3
    elif order >= 80 and order < 90:
        new_stair = 2
    elif order >= 90 and order < 100:
        new_stair = 1
    elif order >= 100 and order < 110:
        new_stair = 0

    # Lower stairs.
    elif order >= 110 and order < 120:
        new_stair = -1
    elif order >= 120 and order < 130:
        new_stair = -2
    elif order >= 130 and order < 140:
        new_stair = -3
    elif order >= 140 and order < 150:
        new_stair = -4
    elif order >= 150 and order < 160:
        new_stair = -5
    elif order >= 160 and order < 170:
        new_stair = -6
    elif order >= 170 and order < 180:
        new_stair = -7
    elif order >= 180 and order < 190:
        new_stair = -8
    elif order >= 190 and order < 200:
        new_stair = -9
    
    # HS animation.
    elif order >= 200:
        ascenseur.is_hors_service = True
        ascenseur.target_stair = ascenseur.current_stair

    # If the order said to go to a specific stair.
    if new_stair is not None:
        ascenseur.goToStair(new_stair)
        screen.bullshit = None
        

# Manage the bullshit channel.
def _manage_bullshit(screen, order: int):
    current_path = screen.bullshit.path if screen.bullshit is not None else ""

    # Render gifs.
    if order >= 10 and order < 20 and current_path != "gyrophare.gif":
        screen.bullshit = Gif.build(screen, "gyrophare.gif", 10)
    elif order >= 20 and order < 30 and current_path != "oss117.gif":
        screen.bullshit = Gif.build(screen, "oss117.gif", 5)
    elif order >= 30 and order < 40 and current_path != "ah.gif":
        screen.bullshit = Gif.build(screen, "ah.gif", 10)
    elif order >= 40 and order < 50 and current_path != "marc.gif":
        screen.bullshit = Gif.build(screen, "marc.gif", 10)
    elif order >= 50 and order < 60 and current_path != "fire.gif":
        screen.bullshit = Gif.build(screen, "fire.gif", 10)
    elif order >= 60 and order < 70 and current_path != "loading.gif":
        screen.bullshit = Gif.build(screen, "loading.gif", 10)
    elif order >= 70 and order < 80 and current_path != "notre-projet.gif":
        screen.bullshit = Gif.build(screen, "notre-projet.gif", 10)
    elif order >= 80 and order < 90 and current_path != "zzz.gif":
        screen.bullshit = Gif.build(screen, "zzz.gif", 10)
    elif order >= 90 and order < 100 and current_path != "eyes.gif":
        screen.bullshit = Gif.build(screen, "eyes.gif", 2)

    # Logo des restos.
    elif order >= 200 and order < 220 and current_path != "restos.png" :
        screen.bullshit = Gif.build(screen, "restos.gif", 1000)
        #screen.bullshit = Image("restos.png")
        #screen.bullshit.load(screen)


# Get the color from the DMX signal.
def _get_color(channel: int):
    value = get(channel)

    return value if value >= 0 else 0


# Globally manage the DMX signals.
def manage(screen, ascenseur):
    # Update the global color.
    screen.text_color.red = _get_color(DMX_CHANNEL_COLOR_R)
    screen.text_color.green = _get_color(DMX_CHANNEL_COLOR_G)
    screen.text_color.blue = _get_color(DMX_CHANNEL_COLOR_B)

    # Manage the orders for the ascenseur.
    order = get(DMX_CHANNEL_ORDER)
    if order >= 0:
        _manage_order(ascenseur, screen, order)

    # Display the bullshit if needed.
    bullshit = get(DMX_CHANNEL_BULLSHIT)
    if order < 10 and bullshit >= 10:
        _manage_bullshit(screen, bullshit)
    else:
        # We reset the bullshit, so that we can remove the 
        # Gif from the screen.
        screen.bullshit = None
