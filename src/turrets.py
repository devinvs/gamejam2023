import time
from dataclasses import dataclass
import random
import math

BULLET_SPEED = 80

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
        ovel = ecs.velocities[other]

        tx = opos.x - pos.x
        ty = opos.y - pos.y
        vx = ovel.x
        vy = ovel.y

        try:
            rcrossv = tx * vy - ty * vx
            magr = math.sqrt(tx*tx + ty*ty)
            angle_adjust = math.asin(rcrossv / (BULLET_SPEED * magr))

            angle = angle_adjust + math.atan2(ty, tx)

            vx = BULLET_SPEED * math.cos(angle)
            vy = BULLET_SPEED * math.sin(angle)

            # Fire!
            ecs.add_bullet(pos.x, pos.y, vx, vy, w.damage)
            ecs.weapons[id].last_fired = time.monotonic()
        except:
            # Domain error, no solutions
            pass

