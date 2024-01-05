from enum import Enum
import os
import pygame

from textures import TextureCache
from ecs import ECS
from physics import position_system, collision_system
from conveyor import conveyor_system, Conveyor
from creatures import creature_system
from turrets import turret_system
from health import health_system


# Here's a fun way to do UI:
# Each screen is just a list of tuples, where each
# tuple is a rect, a color, some text, and an action!

def click_play(engine):
    engine.ui = game_screen
    engine.paused = False

def click_edit(engine):
    engine.ui = map_editor
    engine.paused = False

def click_grid(engine):
    x = engine.mouse_pos[0]
    y = engine.mouse_pos[1]

    if engine.unit_bought is not None and engine.entity_map[y // 40][x // 40] is None:
        match engine.unit_bought:
            case "TURRET":
                id = engine.ecs.add_turret(x - x % 40 + 5, y - y % 40 + 5)
                engine.bank -= 1
            case "HEAVY":
                id = engine.ecs.add_heavy(x - x % 40 + 5, y - y % 40 + 5)
                engine.bank -= 3
            case "FIRE":
                id = engine.ecs.add_fire(x - x % 40 + 5, y - y % 40 + 5)
                engine.bank -= 4
            case "ICE":
                id = engine.ecs.add_ice(x - x % 40 + 5, y - y % 40 + 5)
                engine.bank -= 2
            case "UP":
                id = engine.ecs.add_conveyor(x - x % 40, y - y % 40, Conveyor.UP, engine.tc)
                print("UP")
            case "DOWN":
                id = engine.ecs.add_conveyor(x - x % 40, y - y % 40, Conveyor.DOWN, engine.tc)
            case "LEFT":
                id = engine.ecs.add_conveyor(x - x % 40, y - y % 40, Conveyor.LEFT, engine.tc)
            case "RIGHT":
                id = engine.ecs.add_conveyor(x - x % 40, y - y % 40, Conveyor.RIGHT, engine.tc)
        
        engine.entity_map[y // 40][x // 40] = id
        engine.unit_bought = None

def click_unit(unit, cost):
    def inner(engine):
        if engine.bank >= cost:
            engine.unit_bought = unit
    
    return inner

map_editor = [
    (pygame.Rect(0, 0, 800, 520), None, "", click_grid),
    (pygame.Rect(0, 520, 800, 80), (230, 150, 230), "", None),
    (pygame.Rect(740, 540, 40, 40), (0, 0, 255), "R", click_unit("RIGHT", 0)),
    (pygame.Rect(680, 540, 40, 40), (255, 0, 0), "L", click_unit("LEFT", 0)),
    (pygame.Rect(620, 540, 40, 40), (0, 255, 255), "D", click_unit("DOWN", 0)),
    (pygame.Rect(560, 540, 40, 40), (0, 255, 0), "U", click_unit("UP", 0))
]

title_screen = [
    (pygame.Rect(0, 0, 800, 600), (200, 200, 200), "", None),
    (pygame.Rect(200, 200, 200, 20), (255, 0, 0), "GameNameHere", None),
    (pygame.Rect(400, 400, 200, 20), (0, 255, 0), "PLAY", click_play),
    (pygame.Rect(400, 450, 200, 20), (0, 255, 0), "MAP", click_edit)
]

pause_screen = [
    (pygame.Rect(400, 400, 200, 20), (0, 255, 0), "RESUME", click_play)
]

game_screen = [

    (pygame.Rect(0, 0, 800, 520), None, "", click_grid),
    (pygame.Rect(0, 520, 800, 80), (230, 150, 230), "", None),
    (pygame.Rect(740, 540, 40, 40), (0, 0, 255), "2", click_unit("ICE", 2)),
    (pygame.Rect(680, 540, 40, 40), (255, 0, 0), "4", click_unit("FIRE", 4)),
    (pygame.Rect(620, 540, 40, 40), (0, 255, 255), "3", click_unit("HEAVY", 3)),
    (pygame.Rect(560, 540, 40, 40), (0, 255, 0), "1", click_unit("TURRET", 1))

]


victory_screen = []


class GameEngine:
    tc = TextureCache()
    screen = pygame.display.set_mode((800, 600), pygame.SCALED | pygame.RESIZABLE)
    clock = pygame.time.Clock()
    mouse_pos = None
    running = True
    paused = True
    bank = 10
    unit_bought = None
    entity_map = [[None for _ in range(20)] for _ in range(13)]

    ui = title_screen

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

        self.ecs.add_conveyor(80, 80, Conveyor.RIGHT, self.tc)
        # self.ecs.add_conveyor(100, 80, Conveyor.DOWN)
        # self.ecs.add_conveyor(100, 100, Conveyor.LEFT)
        # self.ecs.add_conveyor(80, 100, Conveyor.UP)

        self.ecs.add_creature(85, 85, 10)
        
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

                    for (rect, _, _, action) in self.ui:
                        if rect.collidepoint(self.mouse_pos) and rect.collidepoint(up_pos):
                            if action is not None:
                                action(self)
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.ui is game_screen:
                            self.ui = pause_screen
                            self.paused = True
                        elif self.ui is pause_screen:
                            self.ui = game_screen
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
    
    # Rendering helpers and main function
    def draw_text(self, x, y, text, color):
        self.font.render_to(self.screen, (x, y), text, color)

    def draw_grid(self):
        w = 40
        nc = 800 // w
        nr = 600 // w

        for i in range(nr+1):
            y = i*w
            pygame.draw.line(self.screen, (255, 255, 255), (0, y-1), (800, y-1))
            pygame.draw.line(self.screen, (255, 255, 255), (0, y), (800, y))

        for i in range(nc+1):
            x = i*w
            pygame.draw.line(self.screen, (255, 255, 255), (x-1, 0), (x-1, 600))
            pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, 600))
        
        
 
    def draw(self):
        self.screen.fill((0, 0, 0))
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
                self.screen.blit(texture, rect)

        
        self.draw_ui()
        if self.ui == (game_screen or pause_screen):
            self.draw_text(40, 560, "Disney Princess Power: " + str(self.bank), "Light Blue")
        pygame.display.flip()

    # Draw the ui of the screen
    def draw_ui(self):
        for (rect, color, text, _) in self.ui:
            if color is None:
                continue

            pygame.draw.rect(self.screen, color, rect)
            self.draw_text(rect.x, rect.y, text, (0, 0, 0))
        

game1 = GameEngine()
game1.new_game()
