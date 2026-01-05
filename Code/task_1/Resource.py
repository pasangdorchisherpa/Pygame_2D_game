from AI import AI
import pygame
from random import randint


class Resource(AI):
    # Resource entity: a collectible that does not move but has an image/rect
    def __init__(self, screen, size=20, image=None):
        color = (0,0,255) if image is None else (0,0,0)  # fallback color if no image
        position = [randint(0, screen.get_width()-size),
                    randint(0, screen.get_height()-size)]
        super().__init__(screen, color, size, position, speed=0, image=image)


    def update_position(self):
        # Resource doesn’t move, position for collisions
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def reset_position(self):
        # Place resource at a new random location and update rect accordingly
        self.position[0] = randint(0, self.screen.get_width()-self.size)
        self.position[1] = randint(0, self.screen.get_height()-self.size)
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
