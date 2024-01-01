import math

CONV_VEL = 40

class Conveyor:
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

# If a creature is on top of a conveyor belt
# it receives a velocity that moves it along
# the direction of the conveyor belt.
#
# Additionally if the center of the creature
# is past the center in the orthogonal direction
# it is stopped.
def conveyor_system(ecs):
    for id in ecs.ids():
        cols = ecs.collisions[id]
        dir = ecs.conveyors[id]

        # we must be a conveyor
        if dir is None or cols is None:
            continue

        conv_pos = ecs.geometries[id]
        centerx = conv_pos.x + conv_pos.w/2
        centery = conv_pos.y + conv_pos.h/2

        # Move all creatures on the conveyor belt
        # A creature has health, so use that to identifier them
        for other in cols:
            if ecs.healths[other] is None:
                continue

            # We keep moving in the orthogonal direction until
            # we are aligned on the center
            other_pos = ecs.geometries[other]
            ocenterx = other_pos.x + other_pos.w/2
            ocentery = other_pos.y + other_pos.h/2

            if ecs.velocities[other].x != 0 or ecs.velocities[other].y != 0:
                if dir==Conveyor.RIGHT or dir==Conveyor.LEFT:
                    # y is orthogonal
                    if abs(centery-ocentery) > 2:
                        continue
                else:
                    # x is orthogonal
                    if abs(centerx-ocenterx) > 2:
                        continue

           
            # We are a creature on top of a conveyor belt
            if dir==Conveyor.RIGHT:
                ecs.velocities[other].x = CONV_VEL
                ecs.velocities[other].y = 0
            if dir==Conveyor.LEFT:
                ecs.velocities[other].x = -CONV_VEL
                ecs.velocities[other].y = 0
            if dir==Conveyor.UP:
                ecs.velocities[other].y = -CONV_VEL
                ecs.velocities[other].x = 0
            if dir==Conveyor.DOWN:
                ecs.velocities[other].y = CONV_VEL
                ecs.velocities[other].x = 0



