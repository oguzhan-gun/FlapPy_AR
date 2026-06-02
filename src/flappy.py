import asyncio
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from .entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from .utils import GameConfig, Images, Sounds, Window

import threading
from .entities.RealTimeControllerHands import HandTracker
import subprocess



class Flappy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        window = Window(288, 512)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )
        self.tracker = HandTracker()
        self.server_thread = threading.Thread(target=self.movement_check, daemon=True)
        self.server_thread.start()
        
        
        self.cmd = []
        
        
    async def start(self):
        while True:
            self.background = Background(self.config)
            self.floor = Floor(self.config)
            self.player = Player(self.config)
            self.welcome_message = WelcomeMessage(self.config)
            self.game_over_message = GameOver(self.config)
            self.pipes = Pipes(self.config)
            self.score = Score(self.config)
            await self.splash()
            await self.play()
            await self.game_over()

    async def splash(self):
        """Shows welcome splash screen animation of flappy bird"""

        self.player.set_mode(PlayerMode.SHM)

        while True:
            if self.cmd and self.cmd[-1] == 'Flap':
                self.cmd.clear()
                fake_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(0,0))
                pygame.event.post(fake_event)
            
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    return

            self.background.tick()
            self.floor.tick()
            self.player.tick()
            self.welcome_message.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()



    def movement_check(self):
                while True:
                    command = self.tracker.get_movement()
                    # print("Alınan veri:", command)
                    if command == 'Flap':
                        print("Flap tetiklendi")
                        self.cmd.clear()
                        self.cmd.append('Flap')
                        print(self.cmd)
                    else:
                        # Stop veya başka komut gelirse hiçbir 
                        self.cmd.clear()
                        self.cmd.append('Stop') 
                        print(self.cmd)
                        
    def check_quit_event(self, event):
        if event.type == QUIT or (
            event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    def is_tap_event(self, event):
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        mouse_button_down = event.type == pygame.MOUSEBUTTONDOWN
        return mouse_button_down or space_or_up or screen_tap

    async def play(self):
        self.score.reset()
        self.player.set_mode(PlayerMode.NORMAL)

        while True:
            if self.player.collided(self.pipes, self.floor):
                return
            
            
            
            if self.cmd and self.cmd[-1] == 'Flap':
                self.player.flap()
                self.cmd.clear()

            for i, pipe in enumerate(self.pipes.upper):
                if self.player.crossed(pipe):
                    self.score.add()

            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    self.player.flap()

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def game_over(self):
        """crashes the player down and shows gameover image"""

        self.player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        while True:
            
            if self.cmd and self.cmd[-1] == 'Flap':
                self.cmd.clear()
                fake_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(0,0))
                pygame.event.post(fake_event)
            
            
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    if self.player.y + self.player.h >= self.floor.y - 1:
                        return

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()
            self.game_over_message.tick()

            self.config.tick()
            pygame.display.update()
            await asyncio.sleep(0)
