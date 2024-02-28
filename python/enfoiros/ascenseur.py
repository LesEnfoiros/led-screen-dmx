import random

# GLOBAL VARIABLES.
SECONDS_BETWEEN_FRAME = 1
ARROW_WIDTH = 30

class Ascenseur:
    # Instanciate the ascenseur class.
    def __init__(self):
        # Static initialisation variables.
        self.current_stair = 0
        self.target_stair = 0 
        self.is_hors_service = False
        self.hide = False


    # Draw the minux sign in the screen.
    def _drawMinus(self, screen):
        # The minus sign appears from:
        # x=21 to x=34
        # y=28 to y=30
        for i in range(14):
            screen.drawPixel(i + 21, 28)
            screen.drawPixel(i + 21, 29)
            screen.drawPixel(i + 21, 30)


    # This function draws an arrow in the screen if
    # the ascenseur is moving.
    def _drawArrow(self, screen):
        if self.current_stair == self.target_stair or self.is_hors_service:
            return

        top_to_down = self.target_stair < self.current_stair
        multiplier = 1 if top_to_down else -1
        head_orig_y = 0 if top_to_down else 64

        for y in range(ARROW_WIDTH):
            for x in range(ARROW_WIDTH - y):
                if x < y:
                    continue

                screen.drawPixel(x, head_orig_y + multiplier * 2 * y)
                screen.drawPixel(x, head_orig_y + multiplier * 2 * y + multiplier)


    # Render the ascenseur. This method is not
    # always called.
    def render(self, screen):
        # If the ascenseur should hide, then do nothing.
        if self.hide:
            screen.sleep(SECONDS_BETWEEN_FRAME)

        # If the ascenseur is out of service.
        elif self.is_hors_service:
            rand = random.randint(0, 10)

            # This is done to make the "HS" text "strobbing".""
            if rand == 7:
                screen.drawText("H", 0, screen.font_baseline)
            elif rand == 2:
                screen.drawText(" S", 0, screen.font_baseline)
            elif rand % 10 != 9:
                screen.drawText("HS", 0, screen.font_baseline)

        # Otherwise, render the ascenseur.
        else:
            is_negative = self.current_stair < 0
            level = - self.current_stair if is_negative else self.current_stair

            # Draw the ciffer.
            screen.drawText(text=level, x=36, y=screen.font_baseline)

            # Draw the minus if the stair is negative.
            if is_negative:
                self._drawMinus(screen)

            # Draw the arrow.
            self._drawArrow(screen)

            # Move to the next stair if needed.
            if self.current_stair != self.target_stair:
                self.current_stair += -1 if self.current_stair > self.target_stair else 1

            screen.sleep(SECONDS_BETWEEN_FRAME)


    # Tell the ascenseur to go to the given stair.
    def goToStair(self, stair):
        self.is_hors_service = False

        if self.current_stair == stair or self.target_stair == stair:
            return
            
        self.target_stair = stair