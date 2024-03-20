import wiringpi as wp
from .gif import Gif
import threading
import time

# GLOBAL DMX VARIABLES.
DMX_I2C_ID            = 0x08
DMX_CHANNEL_INTENSITY = 0
DMX_CHANNEL_COLOR_R   = 1
DMX_CHANNEL_COLOR_G   = 2
DMX_CHANNEL_COLOR_B   = 3
DMX_CHANNEL_ORDER     = 4
DMX_CHANNEL_BULLSHIT  = 5

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
def start(screen, ascenseur):
    thread = threading.Thread(target=_thread, args=(screen, ascenseur))
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
def _thread(screen, ascenseur):
    # Lire des données depuis le périphérique I2C
    while(_thread_should_run):
        _update_channel_value_from_i2c(DMX_CHANNEL_INTENSITY)
        _update_channel_value_from_i2c(DMX_CHANNEL_COLOR_R)
        _update_channel_value_from_i2c(DMX_CHANNEL_COLOR_G)
        _update_channel_value_from_i2c(DMX_CHANNEL_COLOR_B)
        _update_channel_value_from_i2c(DMX_CHANNEL_BULLSHIT)
        _update_channel_value_from_i2c(DMX_CHANNEL_ORDER)

        # Manage the brightness.
        screen.setBrightness(100.0 * get(DMX_CHANNEL_INTENSITY) / 255.0)

        # Then, wait for the next loop.
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
    elif order >= 220 and order < 230:
        ascenseur.is_hors_service = True
        ascenseur.target_stair = ascenseur.current_stair

    # If the order said to go to a specific stair.
    if new_stair is not None:
        ascenseur.goToStair(new_stair)
        screen.bullshit = None
        

# Manage the bullshit channel.
def _manage_bullshit(screen, order: int):
    current_path = screen.bullshit.path if screen.bullshit is not None else ""

    # Logo des restos.
    if order >= 10 and order < 20 and current_path != "restos.gif":
        screen.bullshit = Gif.build(screen, "restos.gif", 20)

    # Coluche.
    if order >= 20 and order < 30 and current_path != "coluche.gif":
        screen.bullshit = Gif.build(screen, "coluche.gif", 20)

    # Render gifs.
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
    elif order >= 100 and order < 110 and current_path != "sam-cool-cool.gif":
        screen.bullshit = Gif.build(screen, "sam-cool-cool.gif", 5)
    elif order >= 110 and order < 120 and current_path != "gyrophare.gif" :
        screen.bullshit = Gif.build(screen, "gyrophare.gif", 10)
    elif order >= 120 and order < 130 and current_path != "raquet.gif" :
        screen.bullshit = Gif.build(screen, "raquet.gif", 10)
    elif order >= 130 and order < 140 and current_path != "jyf.gif" :
        screen.bullshit = Gif.build(screen, "jyf.gif", 10)
    elif order >= 140 and order < 150 and current_path != "glissade.gif" :
        screen.bullshit = Gif.build(screen, "glissade.gif", 10)
    elif order >= 150 and order < 160 and current_path != "sens-interdit.gif" :
        screen.bullshit = Gif.build(screen, "sens-interdit.gif", 10)

    elif order >= 170 and order < 180 and current_path != "hide.gif" :
        screen.bullshit = Gif.build(screen, "hide.gif", 10)
    elif order >= 180 and order < 190 and current_path != "insa.gif" :
        screen.bullshit = Gif.build(screen, "insa.gif", 10)
    elif order >= 190 and order < 200 and current_path != "enfoiros.gif" :
        screen.bullshit = Gif.build(screen, "enfoiros.gif", 10)

    elif order >= 200 and order < 210 and current_path != "oss117.gif":
        screen.bullshit = Gif.build(screen, "oss117.gif", 5)


# Get the color from the DMX signal.
def _get_color(channel: int):
    value = get(channel)

    return value if value >= 0 else 0


# This function manages the colors.
COLOR_BUFFER_R = -1
COLOR_BUFFER_G = -1
COLOR_BUFFER_B = -1
def _manage_color(screen, new_r, new_g, new_b):
    global COLOR_BUFFER_R, COLOR_BUFFER_G, COLOR_BUFFER_B

    # Keep the current values easily accessible.
    current_r = screen.text_color.red
    current_g = screen.text_color.green
    current_b = screen.text_color.blue

    # Set the color buffers if not yet initialized.
    COLOR_BUFFER_R = COLOR_BUFFER_R if COLOR_BUFFER_R >= 0 else current_r
    COLOR_BUFFER_G = COLOR_BUFFER_G if COLOR_BUFFER_G >= 0 else current_g
    COLOR_BUFFER_B = COLOR_BUFFER_B if COLOR_BUFFER_B >= 0 else current_b

    # Initialize some variables determining whether it is all dark.
    current_is_fully_dark = (current_r == 0 and current_g == 0 and current_b == 0) or (get(DMX_CHANNEL_INTENSITY) == 0)
    buffer_is_fully_dark = COLOR_BUFFER_R == 0 and COLOR_BUFFER_G == 0 and COLOR_BUFFER_B == 0
    new_is_fully_dark = new_r == 0 and new_g == 0 and new_b == 0

    # If we detect an anomaly in the color received.
    if current_is_fully_dark and not new_is_fully_dark:
        if buffer_is_fully_dark:
            COLOR_BUFFER_R = new_r
            COLOR_BUFFER_G = new_g
            COLOR_BUFFER_B = new_b

            return (current_r, current_g, current_b)
        else:
            return (new_r, new_g, new_b)

    COLOR_BUFFER_R = new_r
    COLOR_BUFFER_G = new_g
    COLOR_BUFFER_B = new_b

    return (new_r, new_g, new_b)


# Globally manage the DMX signals.
def manage(screen, ascenseur):
    # Manage the colors.
    red, green, blue = _manage_color(screen=screen, 
        new_r=_get_color(DMX_CHANNEL_COLOR_R),
        new_g=_get_color(DMX_CHANNEL_COLOR_G),
        new_b=_get_color(DMX_CHANNEL_COLOR_B),
    )
    screen.text_color.red = red
    screen.text_color.green = green
    screen.text_color.blue = blue

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
