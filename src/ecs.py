import pygame


class ECS:
    next_id = 0

    # component arrays
    positions = []
    velocities = []

    def __init__(self):
        return

    # Create a new entity where each component is set to None,
    # returns the index into the component arrays of that entity
    def new_entity(self):
        self.positions.append(None)
        self.velocities.append(None)

        me = self.next_id
        self.next_id += 1
        return me

    # Delete an entity
    def remove_entity(self, id):
        # Need to think a bit about the lifetimes of our objects...
        # for now just set to nones
        positions[id] = None
        velocities[id] = None

    #
    # Functions to add specific types of entities maybe
    #

    # just an example, probably remove
    def add_stationary(self, x, y):
        id = self.new_entity()
        self.positions[id] = pygame.Vector2(x, y)
        return id


# An example system that calculates the new position after t seconds
def position_system(ecs, t):
    for i in range(len(ecs.positions)):
        pos = ecs.positions[i]
        vel = ecs.velocities[i]

        ecs.positions[i] = pos + vel * t

