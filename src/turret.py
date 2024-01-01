import time

# The turret system is responsible for
# making the turret track creatures and fire upon
# them by spawning a bullet in the world
def turret_system(ecs):
    for id in ecs.ids():
        type = ecs.types[id]
        w = ecs.weapons[id]

        if type is None or w is None:
            continue

        # If we have fired recently wait for our cooldown
        if w.last_fired - time.monotonic() - w.cooldown <= 0.0:
            continue

        # Find creatures within the radius, choose a random one,
        # and fire upon it
