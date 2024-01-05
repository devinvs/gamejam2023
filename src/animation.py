from dataclasses import dataclass
import time

@dataclass
class Animation:
    states: list[str]
    rate: float = 1
    repeat: bool = False
    last_tick: float = 0
    curr: int = 0

def animation_system(ecs):
    for id in ecs.ids():
        anim = ecs.animations[id]

        # skip if we have no animation
        if anim is None:
            continue

        # skip if we have no states
        if len(anim.states) == 0:
            continue

        # if we have reached the end are not repeating
        # remove the animation
        if not anim.repeat and anim.curr == len(anim.states)-1:
            ecs.animations[id] = None

        # If we are waiting do nothing
        if time.monotonic() - anim.last_tick < anim.rate:
            continue
        
        ecs.animations[id].last_tick = time.monotonic()
        ecs.animations[id].curr = (anim.curr + 1) % len(anim.states)
        ecs.textures[id] = ecs.animations[id].states[ecs.animations[id].curr]

