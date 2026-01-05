import pygame

# SQUARE CLASS
class Square:
    def __init__(self, screen, colour=(255,255,255), size=20, position=(0,0), speed=1, image=None):
        self.screen = screen
        self.colour = colour if colour is not None else (255,255,255)  # default white
        self.size = size
        self.position = list(position) # x,y coordinates
        self.speed = speed
        self.speedx = 0 # initial horizontal speed
        self.speedy = 0 # initial vertical speed

        # if an image surface is provided use its rect,
        # otherwise fall back to a simple pygame.Rect for drawing/collision
        self.image = image
        if self.image:
            self.rect = self.image.get_rect(topleft=position)
        else:
            self.rect = pygame.Rect(position[0], position[1], size, size)

    def update_position(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
    
        x = self.position[0] + self.speedx
        y = self.position[1] + self.speedy
    
        # Keep the object inside screen bounds
        x = max(0, min(x, screen_width - self.size))
        y = max(0, min(y, screen_height - self.size))

        self.position = [x, y] # update stored position
        self.rect.x = x # sync rect for drawing/collisions
        self.rect.y = y


    def draw(self):
        # Draw image if provided, otherwise draw coloured rectangle
        if self.image:
            self.screen.blit(self.image, self.rect.topleft)
        else:
            if self.colour:  # only draw if colour is valid
                pygame.draw.rect(self.screen, self.colour,
                                 (self.position[0], self.position[1], self.size, self.size))

    # Motion logic within class
    def stop(self):
        # immediately stop movement
        self.speedx = 0
        self.speedy = 0

    def move_left(self):  self.speedx = -self.speed   # start moving left
    def move_right(self): self.speedx = self.speed   # start moving right
    def move_up(self):    self.speedy = -self.speed  # start moving up
    def move_down(self):  self.speedy = self.speed   # start moving down

    # Collision logic
    def check_collision(self, other):
        return self.rect.colliderect(other.rect)