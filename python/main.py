from enfoiros import ascenseur as ascenseur_lib
from enfoiros import screen as screen_lib
import sys

# Create and instanciate the matrix.
screen = screen_lib.Screen()
ascenseur = ascenseur_lib.Ascenseur()

try:
    # Start loop
    print("Press CTRL-C to stop sample")

    while True:
        screen.clear()

        # Render the components.
        ascenseur.render(screen=screen)

        screen.swap()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)