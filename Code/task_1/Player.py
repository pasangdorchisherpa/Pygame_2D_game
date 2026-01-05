import pygame
from Square import Square
from Enemy import Enemy

# PLAYER CLASS WITH DEATH EVENT
class Player(Square):
    def __init__(self, screen, colour, size, position=(0, 0), speed=5, image=None):
        super().__init__(screen, colour, size, position, speed, image=image)
        
    def set_death_event(self, event):
        self.DEATH = event

    def check_collision(self, obj):
        if super().check_collision(obj):
            if isinstance(obj, Enemy):
                pygame.event.post(pygame.event.Event(self.DEATH))