# Creatures that collide with bullets have their
# Health decreased. The bullets are despawned
def health_system(ecs):
    for id in ecs.ids():
        cols = ecs.collisions[id]
        health = ecs.healths[id]

        if cols is None or len(cols) == 0 or health is None:
            continue

        # If a creature is hit by anything with damage
        # it takes that amount of damage
        for other in cols:
            dmg = ecs.damages[other]
            if dmg is not None:
                health -= dmg
                ecs.remove_entity(other)

        # If health is <= 0 we die, else just set the health
        if health <= 0:
            ecs.remove_entity(id)
        else:
            ecs.healths[id] = health

