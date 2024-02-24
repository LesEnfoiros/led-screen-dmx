from enfoiros import screen as screen_lib
from enfoiros import ascenseur as ascenseur_lib
import time
import sys

# Create and instanciate the matrix.
screen = screen_lib.Screen()
ascenseur = ascenseur_lib.Ascenseur()

i = 0

try:
    # Start loop
    print("Press CTRL-C to stop sample")

    while True:
        screen.clear()
        ascenseur.render(screen=screen)

        if i == 3:
            ascenseur.goToStair(9)
        else:
            i += 1

        screen.swap()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)