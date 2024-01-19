import pygame
from conveyor import Conveyor

GRID_SIZE = 180

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
    gs = GRID_SIZE
    x = engine.mouse_pos[0]
    y = engine.mouse_pos[1]

    if engine.unit_bought is not None and engine.entity_map[y // gs][x // gs] is None:
        match engine.unit_bought:
            case "TURRET":
                id = engine.ecs.add_turret(x - x % gs + 5, y - y % gs + 5)
                engine.bank -= 1
            case "HEAVY":
                id = engine.ecs.add_heavy(x - x % gs + 5, y - y % gs + 5)
                engine.bank -= 3
            case "FIRE":
                id = engine.ecs.add_fire(x - x % gs + 5, y - y % gs + 5)
                engine.bank -= 4
            case "ICE":
                id = engine.ecs.add_ice(x - x % gs + 5, y - y % gs + 5)
                engine.bank -= 2
            case "UP":
                id = engine.ecs.add_conveyor(x - x % gs, y - y % gs, Conveyor.UP)
            case "DOWN":
                id = engine.ecs.add_conveyor(x - x % gs, y - y % gs, Conveyor.DOWN)
            case "LEFT":
                id = engine.ecs.add_conveyor(x - x % gs, y - y % gs, Conveyor.LEFT)
            case "RIGHT":
                id = engine.ecs.add_conveyor(x - x % gs, y - y % gs, Conveyor.RIGHT)
        
        engine.entity_map[y // gs][x // gs] = id
        engine.unit_bought = None

def click_unit(unit, cost):
    def inner(engine):
        if engine.bank >= cost:
            engine.unit_bought = unit
    
    return inner

class UIBox:

    rect = None
    color = None
    texture = None
    text = None
    action = None
    children = []
    
    def __init__(self, rect, color, texture, text, action, children) -> None:
        self.rect = rect
        self.color = color
        self.texture = texture
        self.text = text
        self.action = action
        self.children = children

    def click(self, engine, mouse_pos):
        if not self.rect.collidepoint(mouse_pos):
            return False
        
        child_hit = False
        
        for child in self.children:
            if child.click(engine, mouse_pos):
                child_hit = True
        
        if not child_hit and self.action is not None:
            self.action(engine)

        return True

    def draw(self, screen, font):
        if self.color is not None:
            pygame.draw.rect(screen, self.color, self.rect)
        tr = font.get_rect(self.text)
        font.render_to(screen, (self.rect.x + (self.rect.w - tr.w)/2, self.rect.y + (self.rect.h - tr.h)/2), self.text, (0, 0, 0))

        for child in self.children:
            child.draw(screen, font)

map_editor = UIBox(pygame.Rect(0, 0, 800, 600), None, None, "", None, [
    UIBox(pygame.Rect(0, 0, 800, 520), None, None, "", click_grid, []), 
    UIBox(pygame.Rect(0, 520, 800, 80), (230, 150, 230), None, "", None, [
        UIBox(pygame.Rect(740, 540, 40, 40), (0, 0, 255), None, "R", click_unit("RIGHT", 0), []),
        UIBox(pygame.Rect(680, 540, 40, 40), (255, 0, 0), None, "L", click_unit("LEFT", 0), []),
        UIBox(pygame.Rect(620, 540, 40, 40), (0, 255, 255), None, "D", click_unit("DOWN", 0), []),
        UIBox(pygame.Rect(560, 540, 40, 40), (0, 255, 0), None, "U", click_unit("UP", 0), [])
    ])
])

title_screen = UIBox(pygame.Rect(0, 0, 800, 600), (200, 200, 200), None, "", None, [
    UIBox(pygame.Rect(200, 200, 200, 20), (255, 0, 0), None, "GameNameHere", None, []),
    UIBox(pygame.Rect(400, 400, 200, 20), (0, 255, 0), None, "PLAY", click_play, []),
    UIBox(pygame.Rect(400, 450, 200, 20), (0, 255, 0), None, "MAP", click_edit, [])
])

pause_screen = UIBox(pygame.Rect(400, 400, 200, 20), (0, 255, 0), None, "RESUME", click_play, [])

game_screen = UIBox(pygame.Rect(0, 0, 800, 600), None, None, "", None, [
    UIBox(pygame.Rect(0, 0, 800, 520), None, None, "", click_grid, []), 
    UIBox(pygame.Rect(0, 520, 800, 80), (230, 150, 230), None, "", None, [
        UIBox(pygame.Rect(740, 540, 40, 40), (0, 0, 255), None, "2", click_unit("ICE", 2), []),
        UIBox(pygame.Rect(680, 540, 40, 40), (255, 0, 0), None, "4", click_unit("FIRE", 4), []),
        UIBox(pygame.Rect(620, 540, 40, 40), (0, 255, 255), None, "3", click_unit("HEAVY", 3), []),
        UIBox(pygame.Rect(560, 540, 40, 40), (0, 255, 0), None, "1", click_unit("TURRET", 1), [])
    ])
])

victory_screen = []
