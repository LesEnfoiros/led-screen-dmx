from PIL import Image as Img
from .screen import path
import time

class Image:
    # Initialize the GIF.
    def __init__(self, asset):
        self.path = asset

    # Load the gif.
    def load(self, screen):
        image = Img.open(path("assets/" + self.path))
        image.thumbnail((screen.matrix.width, screen.matrix.height), Img.ANTIALIAS)

        screen.matrix.SetImage(image.convert('RGB'))

    # Render the GIF.
    def render(self, screen):
        time.sleep(100)
