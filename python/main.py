from enfoiros import Ascenseur, Screen
import enfoiros.dmx as DMX 
import enfoiros.service as Service
import sys

# Initialize the DMX before initiating the
# screen that changes the rights.
DMX.connect()

# Create and instanciate the matrix.
screen = Screen()
ascenseur = Ascenseur()

# Then, start the DMX thread to dynamically
# get the values from the Arduino.
DMX.start(screen, ascenseur)

# Start the service, so that we can communicate
# with him when the ascenseur is running.
Service.start(screen, ascenseur)

try:
    # Start loop
    print("Press CTRL-C to stop sample")

    i = 0
    while True:
        if screen.bullshit is None:
            screen.clear()
            ascenseur.render(screen=screen, frame=i)
            screen.swap()

            i += 1
        else: 
            screen.bullshit.render(screen)

        DMX.manage(screen, ascenseur)
except KeyboardInterrupt:
    print("Exiting\n")
    DMX.stop()
    Service.stop()
    sys.exit(0)