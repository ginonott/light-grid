from datetime import datetime, timedelta
from enum import Enum, auto
from random import choice, randint
from typing import Callable

from neopixel import NeoPixel
from lights.animations import Animation, Animator, Color, animator, get_random_color
from lights.timing import FuzzyInterval, Interval, is_after
from lights.layout.maze import maze

min_switch_time = timedelta(seconds=30)
max_switch_time = timedelta(seconds=120)
color_switch_time = timedelta(seconds=30)

class Modes(Enum):
    with_background = auto()
    without_background = auto()

modes = [Modes.without_background, Modes.with_background]

class LavaLampBlob:
    location: list[int]
    switch_interval: FuzzyInterval
    move_interval: Interval
    color_interval: FuzzyInterval
    grow_interval: FuzzyInterval
    color: Color
    size: int

    def __init__(self, location: int) -> None:
        self.color = get_random_color()
        self.location = [location, location, location]
        self.direction = choice((-1, 1))
        self.switch_interval = FuzzyInterval(60, 120)
        self.color_interval = FuzzyInterval(60, 240)
        self.move_interval = Interval(timedelta(seconds=randint(2, 6)))
        self.grow_interval = FuzzyInterval(30, 120)
        self.size = randint(2, 4)

    def tick(self):
        if not self.move_interval.is_ready():
            return
        
        if self.color_interval.is_ready():
            self.color = get_random_color()
    

        # tiny chance we shrink or grow
        if self.grow_interval.is_ready():
            self.size += choice((1, -1))
            self.size = max(2, min(5, self.size))
        
        self.last_moved = datetime.now()

        if self.switch_interval.is_ready():
             self.location.reverse()

        # move it
        prev_location = self.location[1]
        new_location: int
        node = maze.graph[self.location[0]]
        match node:
            case [prev, turn, next]:
                options = {prev, turn, next} - {prev_location}
                new_location = choice(list(options))
            case [prev, next]:
                if prev_location == prev:
                    new_location = next
                else:
                    new_location = prev
            case [back]:
                new_location = back

        self.location.insert(0, new_location)
        self.location = self.location[0:self.size]

    def get_occupied_locations(self):
        return self.location


class LavaLampAnimation(Animation):
    lava_lamp_blobs: list[LavaLampBlob]
    background_color: Color
    background_color_switched_at: datetime

    def __init__(self, *, on_finished: Callable[[], None] | None = None) -> None:
        super().__init__(on_finished=on_finished)

        self.lava_lamp_blobs = [LavaLampBlob(location) for location in range(len(animator.pixels)) if location % 10 == 0]
        self.background_color = self.get_random_color()
        self.background_color_switched_at = datetime.now()

    def run(self, pixels: NeoPixel, animator: Animator) -> None:
        locations: set[int] = set()
        for blob in self.lava_lamp_blobs:
            blob.tick()
            for location in blob.location:
                pixels[location] = self.transition(pixels[location], blob.color, step=1)
                locations.add(location)

        for led in range(len(pixels)):
            if led not in locations:
                pixels[led] = self.transition(pixels[led], self.background_color if modes[0] == Modes.with_background else (0, 0, 0), step=1)

        if is_after(self.background_color_switched_at, color_switch_time):
            self.background_color = self.get_random_color()
            self.background_color_switched_at = datetime.now()



def setup():
    animator.add_animation(LavaLampAnimation())

def change_modes():
    modes.append(modes.pop(0))