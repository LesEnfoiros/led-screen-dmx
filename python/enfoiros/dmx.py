import wiringpi as wp
import threading
import time

# GLOBAL DMX VARIABLES.
DMX_I2C_ID           = 0x08
DMX_NUMBER_CHANNELS  = 3
DMX_CHANNEL_COLOR_R  = 0
DMX_CHANNEL_COLOR_G  = 1
DMX_CHANNEL_COLOR_B  = 2
DMX_CHANNEL_ONOFF    = 3
DMX_CHANNEL_BULLSHIT = 4
DMX_CHANNEL_ORDER    = 5

# Variables.
dmx_values = {}
i2c_fd = None

def dmx_connect():
    global i2c_fd

    # Initialiser WiringPi
    wp.wiringPiSetup()

    # Ouvrir une connexion I2C
    i2c_fd = wp.wiringPiI2CSetup(DMX_I2C_ID)

    if i2c_fd == -1:
        print("Erreur lors de l'ouverture de la connexion I2C")
        exit()


def dmx_start():
    thread = threading.Thread(target=_dmx_thread)
    thread.start()


def _dmx_thread():
    dmx_connect()

    # Lire des données depuis le périphérique I2C
    while(True):
        wp.wiringPiI2CWrite(i2c_fd, DMX_CHANNEL_ORDER)
        value = wp.wiringPiI2CRead(i2c_fd)
        print("Value = %d", value)
        time.sleep(0.2)

def dmx_read(channel: int):
    return dmx_values[channel]