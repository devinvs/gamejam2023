import pygame
import pygame.freetype
import pygame.draw

from ecs import ECS

class GameEngine:

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = False
    mouse_pos = None

    def __init__(self):
        pygame.init()

        self.ecs = ECS()

        # Load font(s)
        self.font = pygame.freetype.Font('./assets/russo.ttf', 24)
    
    def new_game(self):
        self.running = True
        while self.running:
            self.handle_input()
            self.tick()
            self.draw()
        self.clock.tick(60)  # limits FPS to 60

        pygame.quit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = pygame.mouse.get_pos()
                print(self.mouse_pos)
            if event.type == pygame.QUIT:
                self.running = False
    
    def tick(self):
        return
    
    # Rendering helpers and main function
    def draw_text(self, x, y, text):
        self.font.render_to(self.screen, (x, y), text, (0, 0, 0))
 
    def draw(self):
        self.screen.fill((0, 0, 0))

        for id in self.ecs.ids():
            rect = self.ecs.positions[id]
            color = self.colors[id]

            if rect is None or color is None:
                continue

            pygame.draw.rect(self.screen, color, rect)
        
        pygame.display.flip()

game1 = GameEngine()
game1.new_game()
