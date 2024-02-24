from enfoiros import Ascenseur, Screen, Gif
from enfoiros.dmx import dmx_start
import sys

# Create and instanciate the matrix.
screen = Screen()
ascenseur = Ascenseur()

dmx_start()

#gif = Gif("assets/gif/ah.gif")
#gif.load(screen)
while(True):
    continue

try:
    # Start loop
    print("Press CTRL-C to stop sample")

    while True:
        #screen.clear()

        # Render the components.
        #ascenseur.render(screen=screen)
        gif.render(screen)

        #screen.swap()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)