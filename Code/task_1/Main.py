# File: Main.py
# Author: Pasang Dorchi Sherpa
# Date: 2025-11-25
# Project : 2

###################
# T E M P L A T E #
###################

import pygame
from Square import Square
from AI import AI
from Enemy import Enemy
from Player import Player
from EntityFramework import EntityFramework
from Resource import Resource
import time
from pygame.locals import *
from random import choice
import json
import os

# WINDOW SETUP
def setup(window_name, width=800, height=800):
    pygame.init() # initialize pygame internals
    screen = pygame.display.set_mode((width, height)) # create game window
    pygame.display.set_caption(window_name) # set window title
    return screen

# JUST THERE TO END THE GAME
def quit_game():
    pygame.quit() # shut down pygame
    exit() # terminate the program


# EVENT PROCESSING
def process_event(screen, event, ef):
    if event.type == QUIT:
        quit_game()

    # Keyboard handling: movement, pause, and game controls
    elif event.type == KEYDOWN:
        # Toggle pause with ESC
        if event.key == K_ESCAPE:
            ef.paused = not getattr(ef, 'paused', False)
            return

        # Movement/input ignored while paused
        if getattr(ef, 'paused', False):
            return

        if event.key == K_LEFT:
            ef.player.move_left()   # move player left
        elif event.key == K_RIGHT:
            ef.player.move_right()  # move player right
        elif event.key == K_UP:
            ef.player.move_up()     # move player up
        elif event.key == K_DOWN:
            ef.player.move_down()   # move player down
        elif event.key == K_q: 
            game_over(screen, ef)    # immediate game over / show score screen

    elif event.type == KEYUP:
        # if key released stop player movement (no inertia)
        # Only allow stop when not paused
        if not getattr(ef, 'paused', False):
            ef.player.stop()  # stop player's motion

    # Player died
    elif event.type == ef.DEATH:
        game_over(screen, ef)



def show_score(screen, ef):
    font = pygame.font.SysFont('arial', 24) # HUD font
    yellow = pygame.Color(255,255,0) # score colour
    surf = font.render(f"Score: {ef.score}", True, yellow) # render score text
    screen.blit(surf, (screen.get_width()-120, 10)) # draw score top-right



# GAME OVER SCREEN
def game_over(screen, ef):
    screen.fill((0,0,0))  # clear screen to black
    font = pygame.font.SysFont('times new roman', 50) # large font for game over
    red = pygame.Color(255, 0, 0)

    text = font.render(f"GAME OVER: {ef.score}", True, red) # render final score
    rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//3))

    small_font = pygame.font.SysFont('arial', 24) # prompt font
    prompt = small_font.render("Press Q to quit", True, pygame.Color(200, 200, 200))
    prompt_rect = prompt.get_rect(center=(screen.get_width()//2, screen.get_height()//2))

    screen.blit(text, rect) # draw game over text
    screen.blit(prompt, prompt_rect) # draw quit prompt
    pygame.display.flip() # update display once

    # --- WAIT FOR Q PRESS ---
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# HELLO SCREEN
def start_game(screen):
    font_title = pygame.font.SysFont('Comic Sans', 60)
    font_prompt = pygame.font.SysFont('Comic Sans', 30)

    blue = pygame.Color(0, 150, 255)
    white = pygame.Color(255, 255, 255)

    title_surface = font_title.render("Toothbrush Tango", True, blue)
    prompt_surface = font_prompt.render("Press ENTER to start", True, white)

    title_rect = title_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//3))
    prompt_rect = prompt_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))

    waiting = True

    while waiting:
        # Clearing the screen for new stuff to come else everything will be displayed 60 times a sec :OO
        screen.fill((0, 0, 0))   # clear to black for title screen
        screen.blit(title_surface, title_rect)
        screen.blit(prompt_surface, prompt_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER
                    waiting = False


# MAIN LOOP
if __name__ == "__main__":

    # Create, set and track our game window, fps, time
    screen = setup("Plaque Blast")
    CLOCK = pygame.time.Clock()
    fps = 60

    # load assets from JSON
    def load_assets(json_path):
        with open(json_path, 'r') as f:
            cfg = json.load(f)

        def load_img(entry):
            path = os.path.normpath(entry['path'])
            if path.lower().endswith('.png'):
                img = pygame.image.load(path).convert_alpha()
            else:
                img = pygame.image.load(path).convert()
            if 'scale' in entry:
                img = pygame.transform.scale(img, tuple(entry['scale']))
            return img

        assets = {}
        assets['player'] = load_img(cfg['player'])
        assets['enemies'] = [load_img(e) for e in cfg.get('enemies', [])]
        assets['resources'] = [load_img(r) for r in cfg.get('resources', [])]
        assets['background'] = load_img(cfg['background'])
        return assets

    assets = load_assets('task_1/assets.json')

    main_char = assets['player']
    enemy01 = assets['enemies'][0] if assets['enemies'] else None
    resourcedrops = assets['resources']
    background = assets['background']

    # Show start text
    start_game(screen)

    ef = EntityFramework(screen)
    ef.spawn_player(image=main_char) # toothbrush
    ef.spawn_enemy(image=enemy01) # germ
    # provide the resource images so EntityFramework can rechoose on each respawn
    ef.spawn_resource(images=resourcedrops)
    ef.paused = False
    ef.draw()

    while True:
        for event in pygame.event.get():
            process_event(screen, event, ef)

        screen.blit(background, (0, 0))
        # When paused, skip game updates and collisions but still render
        if not getattr(ef, 'paused', False):
            ef.update_positions()
            ef.check_collisions()
        ef.draw()
        show_score(screen, ef)

        if getattr(ef, 'paused', False):
            # semi-transparent overlay
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            pause_font = pygame.font.SysFont('arial', 48)
            pause_surf = pause_font.render('PAUSED - Press ESC to resume', True, pygame.Color(255,255,255))
            pause_rect = pause_surf.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            screen.blit(pause_surf, pause_rect)

        pygame.display.update()
        CLOCK.tick(fps)

