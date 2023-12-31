import pygame

def position_system(ecs, t):
    for id in ecs.ids():
        pos = ecs.positions[id]

        if pos is None:
            continue

        ecs.geometries[id].x = ecs.positions[id].x
        ecs.geometries[id].y = ecs.positions[id].y
        
        vel = ecs.velocities[id]

        if vel is None:
            continue

        ecs.positions[id].x = pos.x + vel.x * t
        ecs.positions[id].y = pos.y + vel.y * t

        ecs.geometries[id].x = ecs.positions[id].x
        ecs.geometries[id].y = ecs.positions[id].y

def collision_system(ecs):
    for id in ecs.ids():
        if not ecs.collidable[id]:
            continue

        ecs.collisions[id] = set([])
        pos = ecs.geometries[id]

        for other in ecs.ids():
            if not ecs.collidable[other] or id == other:
                continue
            
            pos_other = ecs.geometries[other]

            if pos.colliderect(pos_other):
                ecs.collisions[id].add(other)
