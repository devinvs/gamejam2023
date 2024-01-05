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
    health = random.randrange(5, 20)
    ecs.add_creature(50, 50, health)

    # Set delay
    delay = random.uniform(1.0, 6.0)
    last_spawn = time.monotonic()
    
