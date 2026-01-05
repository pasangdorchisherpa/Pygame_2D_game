import pygame
from random import randrange, choice
from Player import Player
from Enemy import Enemy
from Resource import Resource

# ENTITY FRAMEWORK
class EntityFramework:
    ## Manages game entities and overall game state
    def __init__(self, screen, game_objects={}):
        self.screen = screen # game display surface
        self.game_objects = {} # dict of active entities
        self.score = 0 # player's score counter
        self.DEATH = None # custom pygame event for death

    def spawn_player(self, image=None):
        yellow = (255, 255, 0)
        player = Player(self.screen, yellow, 20, (0, 0), 5, image=image) # create player entity
        self.game_objects['player'] = player
        self.player = player
        self.DEATH = pygame.USEREVENT + 1
        self.player.set_death_event(self.DEATH)

    def spawn_enemy(self, image=None):
        width = self.screen.get_width()
        height = self.screen.get_height()
        purple = (128, 0, 128)

        safe_distance = 100
        while True:
            spawn_coord = [randrange(width - 20), randrange(height - 20)]
            # Avoid spawning too close to player
            if hasattr(self, 'player'):
                dx = abs(spawn_coord[0] - self.player.position[0])
                dy = abs(spawn_coord[1] - self.player.position[1])
                if dx > safe_distance or dy > safe_distance:
                    break
            else:
                break

        enemy = Enemy(self.screen, purple, 20, spawn_coord, 5, image=image) # create enemy entity
        self.game_objects['enemy'] = enemy
        # enemy patrol will be set during updates

    def spawn_resource(self, image=None, images=None):
        # images: optional list of resource image surfaces to choose from
        if images:
            chosen = choice(images)
            # store list so we can rechoose on respawn
            self.resource_images = images
        else:
            chosen = image
            self.resource_images = None

        r = Resource(self.screen, size=30, image=chosen)
        self.resource = r
        self.game_objects["resource"] = r


    def update_positions(self):
        for obj in self.game_objects.values():
            obj.update_position()

    def check_collisions(self):
        # Player hits resource -> increment score, respawn resource, change enemy behaviour
        if self.player.rect.colliderect(self.resource.rect):
            self.score += 1  # update score
            self.resource.reset_position()  # move resource to new location

            # choose a new resource image if available and update rect
            if getattr(self, 'resource_images', None):
                new_img = choice(self.resource_images) # pick random image
                self.resource.image = new_img
                self.resource.rect = new_img.get_rect(topleft=(self.resource.position[0], self.resource.position[1]))

            self.increase_enemy_speed() # speed up enemies each collection

            # Change direction of all enemies to make game dynamic
            for obj in self.game_objects.values():
                if isinstance(obj, Enemy):
                    obj.patrol()

        # Player collides with any enemy -> post DEATH event
        for obj in self.game_objects.values():
            if isinstance(obj, Enemy) and self.player.rect.colliderect(obj.rect):
                pygame.event.post(pygame.event.Event(self.DEATH))
    
    
    def increase_enemy_speed(self):
        #Increase speed for all enemies by 10%"""
        for name,obj in self.game_objects.items():
            if isinstance(obj, Enemy):
                obj.speed *= 1.10
                # Maintain direction
                obj.speedx = obj.speedx/abs(obj.speedx) * obj.speed if obj.speedx else 0
                obj.speedy = obj.speedy/abs(obj.speedy) * obj.speed if obj.speedy else 0

    def draw(self):
        for obj in self.game_objects.values():
            obj.draw()