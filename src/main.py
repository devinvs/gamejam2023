import pygame
import pygame.freetype

class GameEngine:

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = False
    color = pygame.Color(0,0,0,255)
    mouse_pos = None

    def __init__(self):
        pygame.init()

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
                self.color.r += 5
            if event.type == pygame.QUIT:
                self.running = False
    
    def tick(self):
        self.mouse_pos = pygame.mouse.get_pos

    def draw_text(self, x, y, text):
        self.font.render_to(self.screen, (x, y), text, (0, 0, 0))
    
    def draw(self):
        self.screen.fill(self.color)
        self.draw_text(50, 50, "Hello World!")
        pygame.display.flip()

game1 = GameEngine()
game1.new_game()
