from types import EntityType

# Creatures that collide with bullets have their
# Health decreased. The bullets are despawned
def health_system(ecs):
    for id in ecs.ids():
        ty = ecs.types[id]
        cols = ecs.collisions[id]
        health = ecs.healths[id]

        if cols is None or cols.empty():
            continue

        # If a bullet hits anything it despawns
        if ty==EntityType.BULLET:
            ecs.remove_entity(id)

        # If a creature is hit by anything with damage
        # it takes that amount of damage
        for other in cols:
            dmg = ecs.damages[other]
            if dmg is not None:
                health -= dmg

        # If health is <= 0 we die, else just set the health
        if health <= 0:
            ecs.remove_entity(id)
        else:
            ecs.healths[id] = health

