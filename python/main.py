from enfoiros import Ascenseur, Screen, Gif
import enfoiros.dmx as DMX 
import sys

# Initialize the DMX before initiating the
# screen that changes the rights.
DMX.connect()

# Create and instanciate the matrix.
screen = Screen()
ascenseur = Ascenseur()

# Then, start the DMX thread to dynamically
# get the values from the Arduino.
DMX.start()
DMX.manage(screen, ascenseur)

try:
    # Start loop
    print("Press CTRL-C to stop sample")

    while True:
        if screen.bullshit is None:
            screen.clear()
            print("Order: " + str(DMX.get(DMX.DMX_CHANNEL_ORDER)))
            ascenseur.render(screen=screen)
            screen.swap()
        else:
            screen.bullshit.render(screen)

        DMX.manage(screen, ascenseur)
except KeyboardInterrupt:
    print("Exiting\n")
    DMX.stop()
    sys.exit(0)