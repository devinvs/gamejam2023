import time
import random

delay = 0
last_spawn = 0

def creature_system(ecs):
    global delay
    global last_spawn

    if time.monotonic() - last_spawn - delay <= 0.0:
        return

    # Spawn
    x = random.randrange(0, 800)
    y = random.randrange(0, 600)
    health = random.randrange(5, 20)
    ecs.add_creature(x, y, health)
    

    # Set delay
    delay = random.uniform(0.2, 100.0)
    last_spawn = time.monotonic()
    
