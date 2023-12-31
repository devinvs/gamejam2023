import pygame

class GameEngine:

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = False
    color = pygame.Color(0,0,0,255)
    mouse_pos = None

    def __init__(self):
        pygame.init()
    
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
    
    def draw(self):
        self.screen.fill(self.color)
        pygame.display.flip()

game1 = GameEngine()
game1.new_game()