import pygame

# The entity component system has no concept of a grid. Every object
# is placed and referred to in world coordinates. Any handling of
# the grid should be done at a layer that is above the ecs
class ECS:
    next_id = 0
    # list of ids to delete at next flush
    delete = set([])

    #
    # component arrays
    #

    # The type of object that we are working with
    types = []
    # The x,y position in world coordinates
    positions = []
    # the width and height of the object
    geometries = []
    # The x,y velocity of the object
    velocities = []
    # A set of the objects that we have collided with
    collisions = []
    # Health
    healths = []
    # Damage
    damages = []

    def __init__(self):
        return

    # Return a generator over all our ids
    def ids(self):
        return range(len(self.types))

    # Create a new entity where each component is set to None,
    # returns the index into the component arrays of that entity
    def new_entity(self):
        self.types.append(None)
        self.positions.append(None)
        self.geometries.append(None)
        self.velocities.append(None)
        self.collisions.append(None)
        self.healths.append(None)
        self.damages.append(None)

        me = self.next_id
        self.next_id += 1
        return me

    # Delete an entity. Just overwrites with Nones and adds to
    # the delete list, to be properly deleted on a flush call
    def remove_entity(self, id):
        self.types[id] = None
        self.positions[id] = None
        self.geometries[id] = None
        self.velocities[id] = None
        self.collisions[id] = None
        self.healths[id] = None
        self.damages[id] = None

        self.delete.add(id)

    # Actually remove deleted entities from their componenet lists
    def flush(self):
        for id in self.delete:
            del types[id]
            del positions[id]
            del geometries[id]
            del velocities[id]
            del collisions[id]
            del healths[id]
            del damages[id]

        self.delete.clear()
       
