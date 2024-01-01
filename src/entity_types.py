from enum import Enum

class EntityType(Enum):
    CONV_RIGHT = 1
    CONV_LEFT = 2
    CONV_UP = 3
    CONV_DOWN = 4
    # TODO: Expand into all types of turrets
    TURRET = 5
    # TODO: Expand into all types of creatures
    CREATURE = 6
    BULLET = 7

    def is_conveyor(self):
        return (self == EntityType.CONV_RIGHT or
                self == EntityType.CONV_LEFT or
                self == EntityType.CONV_DOWN or
                self == EntityType.CONV_UP)

    def is_creature(self):
        return self == EntityType.CREATURE
