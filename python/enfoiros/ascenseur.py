
# GLOBAL VARIABLES.
SECONDS_BETWEEN_FRAME = 1

class Ascenseur:
    # Instanciate the ascenseur class.
    def __init__(self):
        # Static initialisation variables.
        self.current_stair = 0
        self.target_stair = 0 

    # Render the ascenseur. This method is not
    # always called.
    def render(self, screen):
        screen.drawText(text=self.current_stair, x=36, y=48)
    
        if self.current_stair != self.target_stair:
            self.current_stair += -1 if self.current_stair > self.target_stair else 1

        screen.sleep(SECONDS_BETWEEN_FRAME)

    # Tell the ascenseur to go to the given stair.
    def goToStair(self, stair):
        self.target_stair = stair