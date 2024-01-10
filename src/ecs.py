import pygame

from turrets import Weapon
from conveyor import Conveyor
from animation import Animation

# The entity component system has no concept of a grid. Every object
# is placed and referred to in world coordinates. Any handling of
# the grid should be done at a layer that is above the ecs
class ECS:
    next_id = 0
    # list of ids that are free to reclaim
    delete = set([])

    #
    # component arrays
    #

    # The width and height of the object and x,y position in world coordinates
    positions = []
    # The color of the rectangle
    colors = []
    # Texture
    textures = []
    # Geometries (rectangles) Real pixel coordinates of the rectangle
    geometries = []
    # The x,y velocity of the object
    velocities = []
    # A set of the objects that we have collided with
    collisions = []
    # Health
    healths = []
    # Damage, basically only for bullets
    damages = []
    #Collidable
    collidable = []
    # Conveyor Belt directions
    conveyors = []
    # All the weapon stats
    weapons = []
    # All the animations
    animations = []

    def __init__(self):
        return

    # Return a generator over all our ids
    def ids(self):
        return range(len(self.positions))

    # Create a new entity where each component is set to None,
    # returns the index into the component arrays of that entity
    def new_entity(self):
        me = 0

        if len(self.delete) > 0:
            print(self.delete)
            me = self.delete.pop()
        else:
            print(self.next_id)
            me = self.next_id
            self.next_id += 1
            self.positions.append(None)
            self.colors.append(None)
            self.textures.append(None)
            self.geometries.append(None)
            self.velocities.append(None)
            self.collisions.append(None)
            self.healths.append(None)
            self.damages.append(None)
            self.collidable.append(False)
            self.conveyors.append(None)
            self.weapons.append(None)
            self.animations.append(None)

        return me

    # Delete an entity. Just overwrites with Nones and adds to
    # the delete list, to be properly deleted on a flush call
    def remove_entity(self, id):
        self.positions[id] = None
        self.colors[id] = None
        self.textures[id] = None
        self.geometries[id] = None
        self.velocities[id] = None
        self.collisions[id] = None
        self.healths[id] = None
        self.damages[id] = None
        self.collidable[id] = False
        self.conveyors[id] = None
        self.weapons[id] = None
        self.animations[id] = None

        self.delete.add(id)

    def add_conveyor(self, x, y, dir):
        id = self.new_entity()
        self.positions[id] = pygame.Vector2(x, y)
        self.geometries[id] = pygame.Rect(x, y, 220, 220)
        self.collidable[id] = True
        self.conveyors[id] = dir

        if dir == Conveyor.RIGHT:
            self.animations[id] = Animation([
                ("./assets/belth/frame_1.png", (220, 220), (10, 15)),
                ("./assets/belth/frame_2.png", (220, 220), (10, 15)),
                ("./assets/belth/frame_3.png", (220, 220), (10, 15)),
            ], 0.2, True)
        elif dir == Conveyor.LEFT:
            self.animations[id] = Animation([
                ("./assets/belth/frame_3.png", (60, 60), (5, 8)),
                ("./assets/belth/frame_2.png", (60, 60), (5, 8)),
                ("./assets/belth/frame_1.png", (60, 60), (5, 8)),
            ], 0.2, True)
        elif dir == Conveyor.UP:
            self.animations[id] = Animation([
                ("./assets/beltv/frame_1.png", (60, 60), (5, 8)),
                ("./assets/beltv/frame_2.png", (60, 60), (5, 8)),
                ("./assets/beltv/frame_3.png", (60, 60), (5, 8)),
            ], 0.2, True)
        elif dir == Conveyor.DOWN:
            self.animations[id] = Animation([
                ("./assets/beltv/frame_3.png", (60, 60), (5, 8)),
                ("./assets/beltv/frame_2.png", (60, 60), (5, 8)),
                ("./assets/beltv/frame_1.png", (60, 60), (5, 8)),
            ], 0.2, True)

        return id

    def add_creature(self, x, y, health):
        id = self.new_entity()
        self.positions[id] = pygame.Vector2(x, y)
        self.geometries[id] = pygame.Rect(x, y, 30.0, 30.0)
        self.velocities[id] = pygame.math.Vector2(0, 0)
        self.collidable[id] = True
        self.healths[id] = health
        self.animations[id] = Animation([
            ("./assets/chicken/frame_01.png", (400, 400), (27, 27)),
        ], 0.2, True)

        return id
        
    def add_bullet(self, x, y, vx, vy, dmg):
        id = self.new_entity()
        self.positions[id] = pygame.Vector2(x, y)
        self.geometries[id] = pygame.Rect(x, y, 3.0, 3.0)
        self.colors[id] = (0, 255, 0)
        self.velocities[id] = pygame.math.Vector2(vx, vy)
        self.collidable[id] = True
        self.damages[id] = dmg

        return id

    def add_turret(self, x, y):
        id = self.new_entity()
        self.positions[id] = pygame.Vector2(x, y)
        self.geometries[id] = pygame.Rect(x, y, 30.0, 30.0)
        self.weapons[id] = Weapon(20.0, 1000.0, 1.0)
        self.textures[id] = ("./assets/penguin/frame_01.png", (40, 40), None)

        return id

    def add_heavy(self, x, y):
        id = self.new_entity()
        self.positions[id] = pygame.Vector2(x, y)
        self.geometries[id] = pygame.Rect(x, y, 30.0, 30.0)
        self.colors[id] = (0, 255, 255)
        self.weapons[id] = Weapon(2.0, 5.0, 1.0)

        return id

    def add_fire(self, x, y):
        id = self.new_entity()
        self.positions[id] = pygame.Vector2(x, y)
        self.geometries[id] = pygame.Rect(x, y, 30.0, 30.0)
        self.colors[id] = (255, 0, 0)
        self.weapons[id] = Weapon(2.0, 5.0, 1.0)

        return id

    def add_ice(self, x, y):
        id = self.new_entity()
        self.positions[id] = pygame.Vector2(x, y)
        self.geometries[id] = pygame.Rect(x, y, 30.0, 30.0)
        self.colors[id] = (0, 0, 255)
        self.weapons[id] = Weapon(2.0, 5.0, 1.0)

        return id

