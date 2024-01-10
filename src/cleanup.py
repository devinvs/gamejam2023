# Make sure that anything that flies out of bounds
# will be despawned
def cleanup_system(ecs):
    for id in ecs.ids():
        g = ecs.geometries[id]

        if g is None:
            continue

        if g.y > 600 or g.x > 800 or g.y+g.h < 0 or g.x+g.w < 0:
            ecs.remove_entity(id)

        
