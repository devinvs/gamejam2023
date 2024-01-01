from enum import Enum
import pygame

from ecs import ECS
from physics import position_system, collision_system
from conveyor import conveyor_system
from entity_types import EntityType


# Here's a fun way to do UI:
# Each screen is just a list of tuples, where each
# tuple is a rect, a color, some text, and an action!

def click_play(engine):
    engine.ui = game_screen
    engine.paused = False

def click_grid(engine):
    x = engine.mouse_pos[0]
    y = engine.mouse_pos[1]

    if engine.unit_bought is not None and engine.entity_map[y // 40][x // 40] is None or True:
        
        id = engine.ecs.new_entity()
        engine.ecs.positions[id] = pygame.Rect(x - x % 40 + 5, y - y % 40 + 5, 30.0, 30.0)
        engine.ecs.colors[id] = (255, 0, 0)
        
        engine.entity_map[y // 40][x // 40] = id
        engine.unit_bought = None
    

title_screen = [
    (pygame.Rect(0, 0, 200, 20), (255, 0, 0), "GameNameHere", None),
    (pygame.Rect(400, 400, 200, 20), (0, 255, 0), "PLAY", click_play)
]

pause_screen = [
    (pygame.Rect(400, 400, 200, 20), (0, 255, 0), "RESUME", click_play)
]

game_screen = [
    (pygame.Rect(0, 0, 800, 520), None, None, click_grid),
    (pygame.Rect(0, 520, 800, 80), (0, 255, 0), "You have no money :_(", None)
]


victory_screen = []


class GameEngine:
    screen = pygame.display.set_mode((800, 600), pygame.SCALED | pygame.RESIZABLE)
    clock = pygame.time.Clock()
    mouse_pos = None
    running = True
    paused = True
    unit_bought = None
    entity_map = [[None for _ in range(20)] for _ in range(13)]

    ui = title_screen

    def add_conveyor(self, type, x, y):
        id = self.ecs.new_entity()
        self.ecs.types[id] = type
        self.ecs.positions[id] = pygame.Vector2(x, y)
        self.ecs.geometries[id] = pygame.Rect(x, y, 20, 20)
        self.ecs.colors[id] = (255, 0, 0)
        self.ecs.collidable[id] = True

    def __init__(self):
        pygame.init()

        self.ecs = ECS()
        # Load entitities for testing (optional)
        
        self.add_conveyor(EntityType.CONV_RIGHT, 80, 80)
        self.add_conveyor(EntityType.CONV_DOWN, 100, 80)
        self.add_conveyor(EntityType.CONV_LEFT, 100, 100)
        self.add_conveyor(EntityType.CONV_UP, 80, 100)


        # creature
        id = self.ecs.new_entity()
        self.ecs.types[id] = EntityType.CREATURE
        self.ecs.positions[id] = pygame.Vector2(80.0, 80.0)
        self.ecs.geometries[id] = pygame.Rect(80.0, 90.0, 10.0, 10.0)
        self.ecs.colors[id] = (0, 0, 255)
        self.ecs.velocities[id] = pygame.math.Vector2(0, 0)
        self.ecs.collidable[id] = True
        
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
            position_system(self.ecs, t)
            collision_system(self.ecs)
            conveyor_system(self.ecs)
    
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
            color = self.ecs.colors[id]

            if rect is None or color is None:
                continue

            pygame.draw.rect(self.screen, color, rect)

        
        self.draw_ui()
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
