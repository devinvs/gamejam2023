import time
from dataclasses import dataclass
import random

@dataclass
class Weapon:
    damage: float
    radius: float
    cooldown: float
    last_fired: float = 0

# The turret system is responsible for
# making the turret track creatures and fire upon
# them by spawning a bullet in the world
def turret_system(ecs):
    for id in ecs.ids():
        pos = ecs.positions[id]
        w = ecs.weapons[id]

        if w is None or pos is None:
            continue


        # If we have fired recently wait for our cooldown
        if time.monotonic() - w.last_fired - w.cooldown <= 0.0:
            continue

        # Find creatures within the radius, choose a random one,
        # and fire upon it
        cs = []

        for other in ecs.ids():
            opos = ecs.positions[other]
            health = ecs.healths[other]

            if opos is None or health is None or health <= 0.0:
                continue

            if (pos.x-opos.x)**2 + (pos.y-opos.y)**2 < w.radius**2:
                cs.append((other, opos))

        if len(cs) == 0:
            continue

        # Choose a rando
        (other, opos) = random.choice(cs)

        # Fire!!!
        v = (opos - pos).normalize() * 50

        ecs.add_bullet(pos.x, pos.y, v.x, v.y, w.damage)
        ecs.weapons[id].last_fired = time.monotonic()

