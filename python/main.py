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

#gif = Gif("assets/gif/gyrophare.gif")
#gif.load(screen)

try:
    # Start loop
    print("Press CTRL-C to stop sample")

    while True:
        screen.clear()

        # Render the components.
        ascenseur.render(screen=screen)
        print("Order: " + str(DMX.get(DMX.DMX_CHANNEL_ORDER)))
        DMX.manage()
        #gif.render(screen)

        screen.swap()
except KeyboardInterrupt:
    print("Exiting\n")
    DMX.stop()
    sys.exit(0)