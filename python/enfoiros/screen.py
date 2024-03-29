from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import os

BASE_PYTHON_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../")

# Get the absolute path of the given asset.
def path(asset):
    return os.path.join(BASE_PYTHON_FOLDER, asset)


# GLOBAL VARIABLES.
MATRIX_SIZE = 64
FONT_ASSET = path("assets/font-32x64.bdf")


# This class interacts with the screen.
class Screen:
    def __init__(self):
        self.bullshit = None
        self.brightness = 100 # Default brightness of the screen
        self._load_matrix()
        self._load_font()

    # Load the matrix properties.        
    def _load_matrix(self):
        # Configurations for the matrix.
        options = RGBMatrixOptions()
        options.rows = MATRIX_SIZE
        options.cols = MATRIX_SIZE
        options.chain_length = 1
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
        self.text_color = graphics.Color(255, 255, 255)
        self.font_baseline = 52

    # Go to next frame.
    def clear(self):
        self.canvas.Clear()

    # Set the screen brightness.
    # Value between 1 and 100.
    def setBrightness(self, value: int):
        self.brightness = value
        self.matrix.brightness = value

    # Swap the screen for the next frame.
    def swap(self):
        self.canvas = self.matrix.SwapOnVSync(self.canvas)
        self.canvas.brightness = self.brightness

    # Draw a text in the screen.
    def drawText(self, text, x, y):
        graphics.DrawText(self.canvas, self.font, x, y, self.text_color, str(text))

    # Draw a pixel at the given coordinates.
    def drawPixel(self, x, y):
        self.canvas.SetPixel(x, y, self.text_color.red, self.text_color.green, self.text_color.blue)

    # Make the program stop for a given number of seconds.
    def sleep(self, nbr_seconds):
        time.sleep(nbr_seconds)