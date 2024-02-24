from PIL import Image
import sys

class Gif:
    # Initialize the GIF.
    def __init__(self, path, rate):
        self.path = path
        self.rate = rate
        self.canvases = []
        self.current_frame = 0

    def build(screen, file_name, rate):
        gif = Gif(file_name, rate)
        gif.load(screen)

        return gif

    # Load the gif.
    def load(self, screen):
        gif = Image.open(self.path)

        try:
            self.num_frames = gif.n_frames
        except Exception:
            sys.exit("provided image is not a gif")

        for frame_index in range(0, self.num_frames):
            gif.seek(frame_index)
            # must copy the frame out of the gif, since thumbnail() modifies the image in-place
            frame = gif.copy()
            frame.thumbnail((screen.matrix.width, screen.matrix.height), Image.ANTIALIAS)
            canvas = screen.matrix.CreateFrameCanvas()
            canvas.SetImage(frame.convert("RGB"))

            self.canvases.append(canvas)

        # Close the gif file to save memory now that we have copied out all of the frames
        gif.close()

    # Render the GIF.
    def render(self, screen):
        screen.matrix.SwapOnVSync(self.canvases[self.current_frame], framerate_fraction=self.rate)

        if self.current_frame == self.num_frames - 1:
            self.current_frame = 0
        else:
            self.current_frame += 1
