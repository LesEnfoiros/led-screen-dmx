from enfoiros import screen as screen_lib
from enfoiros import ascenseur as ascenseur_lib
import time
import sys

# Create and instanciate the matrix.
screen = screen_lib.Screen()
ascenseur = ascenseur_lib.Ascenseur()

try:
    # Start loop
    print("Press CTRL-C to stop sample")

    while True:
        screen.clear()
        ascenseur.render(screen)

        time.sleep(1)
        screen.swap()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)


try:
    # Start loop
    print("Press CTRL-C to stop sample")
    
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("assets/font-32x64.bdf")
    textColor = graphics.Color(255, 255, 0)
    pos = offscreen_canvas.width
    my_text = 1

    while True:
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, 0, 64, textColor, my_text)

        time.sleep(1)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)