def position_system(ecs, t):
    pass

def collision_system(ecs, t):
    pass


# If a creature is on top of a conveyor belt
# it receives a velocity that moves it along
# the direction of the conveyor belt.
#
# Additionally if the center of the creature
# is past the center in the orthogonal direction
# it is stopped.
def conveyor_system(ecs):

