from enum import Enum
import pygame

from ecs import ECS
from physics import position_system, collision_system


# Here's a fun way to do UI:
# Each screen is just a list of tuples, where each
# tuple is a rect, a color, some text, and an action!

def click_play(engine):
    engine.ui = game_screen
    engine.paused = False


title_screen = [
    (pygame.Rect(0, 0, 200, 20), (255, 0, 0), "GameNameHere", None),
    (pygame.Rect(400, 400, 200, 20), (0, 255, 0), "PLAY", click_play)
]

pause_screen = [
    (pygame.Rect(400, 400, 200, 20), (0, 255, 0), "RESUME", click_play)
]

game_screen = []


victory_screen = []


class GameEngine:
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    mouse_pos = None
    running = True
    paused = True

    ui = title_screen

    def __init__(self):
        pygame.init()

        self.ecs = ECS()
        # Load entitities for testing (optional)

        id = self.ecs.new_entity()
        self.ecs.positions[id] = pygame.Rect(50.0, 50.0, 200.0, 200.0)
        self.ecs.colors[id] = (255, 0, 0)
        self.ecs.velocities[id] = pygame.math.Vector2(5.0, 0.0)
        
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
                        self.ui = pause_screen
                        self.paused = True
                
    
    def tick(self):
        self.clock.tick(60)
        if not self.paused:
            position_system(self.ecs, 1)
            collision_system(self.ecs)
    
    # Rendering helpers and main function
    def draw_text(self, x, y, text, color):
        self.font.render_to(self.screen, (x, y), text, color)
 
    def draw(self):
        self.screen.fill((0, 0, 0))

        for id in self.ecs.ids():
            rect = self.ecs.positions[id]
            color = self.ecs.colors[id]

            if rect is None or color is None:
                continue

            pygame.draw.rect(self.screen, color, rect)

        
        self.draw_ui()
        pygame.display.flip()

    # Draw the ui of the screen
    def draw_ui(self):
        for (rect, color, text, _) in self.ui:
            pygame.draw.rect(self.screen, color, rect)
            self.draw_text(rect.x, rect.y, text, (0, 0, 0))
        

game1 = GameEngine()
game1.new_game()
