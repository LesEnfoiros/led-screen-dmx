from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import sys

# GLOBAL VARIABLES.
MATRIX_SIZE = 64
FONT_ASSET = "assets/font-32x64.bdf"


class Screen:
    def __init__(self):
        self._load_matrix()
        self._load_font()

    # Load the matrix properties.        
    def _load_matrix(self):
        # Configurations for the matrix.
        options = RGBMatrixOptions()
        options.rows = MATRIX_SIZE
        options.cols = MATRIX_SIZE
        options.chain_length = 2
        options.parallel = 1
        options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

        # Init the internal variables.
        self.matrix = RGBMatrix(options = options)
        self.canvas = self.matrix.CreateFrameCanvas()

    # Load the font to be used in the screen.
    def _load_font(self):
        # Load the font family.
        self.font = graphics.Font()
        self.font.LoadFont(FONT_ASSET)

        # Initialise the font color.
        self.text_color = graphics.Color(255, 255, 0)

    # Go to next frame.
    def next(self):
        self.matrix.SwapOnVSync(self.canvas)
        self.canvas.clear()

    # Draw a text in the screen.
    def drawText(self, text, x, y):
        graphics.DrawText(self.canvas, self.font, x, y, self.text_color, str(text))




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