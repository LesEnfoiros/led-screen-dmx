
# GLOBAL VARIABLES.
SECONDS_BETWEEN_FRAME = 1

class Ascenseur:
    # Instanciate the ascenseur class.
    def __init__(self):
        # Static initialisation variables.
        self.current_stair = 0
        self.target_stair = 0 

    # Draw the minux sign in the screen.
    def _drawMinus(self, screen):
        # The minus sign appears from:
        # x=20 to x=34
        # y=28 to y=30
        for i in range(14):
            screen.drawPixel(i + 20, 28)
            screen.drawPixel(i + 20, 29)
            screen.drawPixel(i + 20, 30)

    # Render the ascenseur. This method is not
    # always called.
    def render(self, screen):
        is_negative = self.current_stair < 0
        level = - self.current_stair if is_negative else self.current_stair

        # Draw the ciffer.
        screen.drawText(text=level, x=36, y=screen.font_baseline)

        # Draw the minus if the stair is negative.
        if is_negative:
            self._drawMinus(screen)

        # Move to the next stair if needed.
        if self.current_stair != self.target_stair:
            self.current_stair += -1 if self.current_stair > self.target_stair else 1

        screen.sleep(SECONDS_BETWEEN_FRAME)

    # Tell the ascenseur to go to the given stair.
    def goToStair(self, stair):
        self.target_stair = stair