
class Ascenseur:
    # Instanciate the ascenseur class.
    def __init__(self, screen):
        self.screen = screen

        # Static initialisation variables.
        self.current_stair = 0
        self.target_stair = 0 

    def render(self):
        self.screen.drawText(1, 0, 64)