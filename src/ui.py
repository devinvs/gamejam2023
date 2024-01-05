import pygame

from conveyor import Conveyor

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
