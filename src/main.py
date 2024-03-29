from enum import Enum
import os
import pygame

import ui
from textures import TextureCache
from ecs import ECS
from physics import position_system, collision_system
from conveyor import conveyor_system, Conveyor
from creatures import creature_system
from turrets import turret_system
from health import health_system
from animation import animation_system
from cleanup import cleanup_system

class GameEngine:
    tc = TextureCache()
    screen = pygame.display.set_mode((3840, 2160), flags=pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    mouse_pos = None
    running = True
    paused = True
    bank = 10
    unit_bought = None
    entity_map = [[None for _ in range(20)] for _ in range(13)]

    ui = ui.title_screen

    def __init__(self):
        pygame.init()

        self.ecs = ECS()
        # Load entitities for testing (optional)
        
        # self.add_conveyor(EntityType.CONV_RIGHT, 0, 4, self.tc)
        # self.add_conveyor(EntityType.CONV_RIGHT, 1, 4)
        # self.add_conveyor(EntityType.CONV_RIGHT, 2, 4)
        # self.add_conveyor(EntityType.CONV_RIGHT, 3, 4)
        # self.add_conveyor(EntityType.CONV_RIGHT, 4, 4)
        # self.add_conveyor(EntityType.CONV_DOWN, 5, 4)
        # self.add_conveyor(EntityType.CONV_DOWN, 5, 5)
        # self.add_conveyor(EntityType.CONV_DOWN, 5, 6)
        # self.add_conveyor(EntityType.CONV_LEFT, 5, 7)
        # self.add_conveyor(EntityType.CONV_UP, 10, 10)

        # self.ecs.add_conveyor(80, 80, Conveyor.RIGHT)
        # self.ecs.add_conveyor(100, 80, Conveyor.DOWN)
        # self.ecs.add_conveyor(100, 100, Conveyor.LEFT)
        # self.ecs.add_conveyor(80, 100, Conveyor.UP)

        # self.ecs.add_creature(85, 85, 10)
        
        # Load font(s)
        self.font = pygame.freetype.Font('./assets/russo.ttf', 24)
    
    def new_game(self):
        self.running = True
        while self.running:
            self.handle_input()
            self.tick()
            self.draw()

        pygame.quit()

    def handle_input(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEBUTTONDOWN:
                    self.mouse_pos = pygame.mouse.get_pos()
                case pygame.QUIT:
                    self.running = False
                case pygame.MOUSEBUTTONUP:
                # if the mouse went down and up on the same button thats a click
                    up_pos = pygame.mouse.get_pos()

                    self.ui.click(self, self.mouse_pos)
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.ui is ui.game_screen:
                            self.ui = ui.pause_screen
                            self.paused = True
                        elif self.ui is ui.pause_screen:
                            self.ui = ui.game_screen
                            self.paused = False
                
    
    def tick(self):
        t = self.clock.tick() / 1000
        if not self.paused:
            creature_system(self.ecs)
            turret_system(self.ecs)
            position_system(self.ecs, t)
            collision_system(self.ecs)
            conveyor_system(self.ecs)
            health_system(self.ecs)
            animation_system(self.ecs)
            cleanup_system(self.ecs)
    
    # Rendering helpers and main function
    def draw_text(self, x, y, text, color):
        self.font.render_to(self.screen, (x, y), text, color)

    def draw_grid(self):
        w = ui.GRID_SIZE
        nc = 3840 // w
        nr = 2160 // w

        for i in range(nr+1):
            y = i*w
            pygame.draw.line(self.screen, "black", (0, y), (3840, y))

        for i in range(nc+1):
            x = i*w
            pygame.draw.line(self.screen, "black", (x, 0), (x, 2160))
                
 
    def draw(self):
        self.screen.fill("white")
        self.draw_grid()

        for id in self.ecs.ids():
            rect = self.ecs.geometries[id]
            texture = self.ecs.textures[id]
            color = self.ecs.colors[id]

            if rect is None:
                continue

            if color is not None:
                pygame.draw.rect(self.screen, color, rect)

            if texture is not None:
                (path, size, off) = texture
                tex = self.tc.load(path, size)

                if off is not None:
                    rect = rect.copy()
                    rect.x -= off[0]
                    rect.y -= off[1]
                
                self.screen.blit(tex, rect)

        
        self.ui.draw(self.screen, self.font)
        if self.ui == ui.game_screen or self.ui == ui.pause_screen:
            self.draw_text(40, 560, "Disney Princess Power: " + str(self.bank), "Light Blue")
        pygame.display.flip()

        

game1 = GameEngine()
game1.new_game()
