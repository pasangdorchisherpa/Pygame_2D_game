from AI import AI

class Enemy(AI):
    def __init__(self, screen, colour, size, position=(0,0), speed=1, image=None):
        super().__init__(screen, colour, size, position, speed, image=image)
