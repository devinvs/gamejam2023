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
    # The width and height of the object and x,y position in world coordinates
    positions = []
    # The x,y velocity of the object
    velocities = []
    # A set of the objects that we have collided with
    collisions = []
    # Health
    healths = []
    # Damage
    damages = []
    #Collidable
    collidable = []

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
        self.velocities.append(None)
        self.collisions.append(None)
        self.healths.append(None)
        self.damages.append(None)
        self.collidable.append(False)

        me = self.next_id
        self.next_id += 1
        return me

    # Delete an entity. Just overwrites with Nones and adds to
    # the delete list, to be properly deleted on a flush call
    def remove_entity(self, id):
        self.types[id] = None
        self.positions[id] = None
        self.velocities[id] = None
        self.collisions[id] = None
        self.healths[id] = None
        self.damages[id] = None
        self.collidable[id] = False

        self.delete.add(id)

    # Actually remove deleted entities from their componenet lists
    def flush(self):
        for id in self.delete:
            del self.types[id]
            del self.positions[id]
            del self.velocities[id]
            del self.collisions[id]
            del self.healths[id]
            del self.damages[id]
            del self.collidable[id]

        self.delete.clear()
       
