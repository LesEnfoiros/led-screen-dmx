from enfoiros import Ascenseur, Screen, Gif
import sys

# Create and instanciate the matrix.
screen = Screen()
ascenseur = Ascenseur()

gif = Gif("assets/gif/oss117.gif")
gif.load()

try:
    # Start loop
    print("Press CTRL-C to stop sample")

    while True:
        screen.clear()

        # Render the components.
        #ascenseur.render(screen=screen)
        gif.render()

        screen.swap()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)