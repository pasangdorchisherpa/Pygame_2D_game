from random import randrange, randint
from Square import Square

# AI CLASS (RANDOM)
class AI(Square):
    # Basic auto behavior used by enemies (random patrol + bounce)
    def __init__(self, screen, colour, size, position=(0, 0), speed=1, image=None):
        super().__init__(screen, colour, size, position, speed, image=image)

    def patrol(self):
        ##Choose a random direction
        x_dir = randint(-1, 1)  # -1, 0 or 1 for horizontal
        y_dir = randint(-1, 1)  # -1, 0 or 1 for vertical

        # If both are zero, force movement along x to avoid static enemies
        if x_dir == 0 and y_dir == 0:
            x_dir = 1 
            # this avoids completely stationary enemies

        self.speedx = self.speed * x_dir  # horizontal velocity
        self.speedy = self.speed * y_dir  # vertical velocity

    def update_position(self):
        # Move and bounce off walls using parent logic then adjust direction
        super().update_position()

        width = self.screen.get_width()
        height = self.screen.get_height()

        # Bounce when hitting horizontal bounds
        if self.position[0] <= 0 or self.position[0] >= width - self.size:
            self.speedx *= -1
        # Bounce when hitting vertical bounds
        if self.position[1] <= 0 or self.position[1] >= height - self.size:
            self.speedy *= -1