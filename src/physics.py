import pygame

def position_system(ecs, t):
    for id in ecs.ids():
        vel = ecs.velocities[id]
        pos = ecs.positions[id]

        if vel is None or pos is None:
            continue

        ecs.positions[id].x = pos.x + vel.x * t
        ecs.positions[id].y = pos.y + vel.y * t

def collision_system(ecs):
    for id in ecs.ids():
        if not ecs.collidable[id]:
            continue

        ecs.collisions[id] = set([])
        pos = ecs.positions[id]

        for other in ecs.ids():
            if not ecs.collidable[other] or id == other:
                continue
            
            pos_other = ecs.positions[other]

            if pos.colliderect(pos_other):
                ecs.collisions[id].add(other)
