import math

from entity_types import EntityType

CONV_VEL = 5


# If a creature is on top of a conveyor belt
# it receives a velocity that moves it along
# the direction of the conveyor belt.
#
# Additionally if the center of the creature
# is past the center in the orthogonal direction
# it is stopped.
def conveyor_system(ecs):
    for id in ecs.ids():
        type = ecs.types[id]
        cols = ecs.collisions[id]

        # We must be a conveyor belt
        if not type.is_conveyor():
            continue

        conv_pos = ecs.positions[id]

        # Move all creatures on the conveyor belt
        for other in cols:
            if not ecs.types[other].is_creature():
                continue

            # We are a creature on top of a conveyor belt
            if type==EntityType.CONV_RIGHT:
                ecs.velocities[other].x = CONV_VEL
            if type==EntityType.CONV_LEFT:
                ecs.velocities[other].x = -CONV_VEL
            if type==EntityType.CONV_UP:
                ecs.velocities[other].y = CONV_VEL
            if type==EntityType.CONV_DOWN:
                ecs.velocities[other].y = -CONV_VEL

            # We keep moving in the orthogonal direction until
            # we are aligned on the center
            other_pos = ecs.positions[id]

            if type==EntityType.CONV_RIGHT or type==EntityType.CONV_LEFT:
                # y is orthogonal
                if math.abs(conv_pos.centery-other_pos.centery) < 10:
                    ecs.velocities[other].y = 0
            else:
                # x is orthogonal
                if math.abs(conv_pos.centerx-other_pos.centerx) < 10:
                    ecs.velocities[other].x = 0

