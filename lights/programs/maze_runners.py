from random import choice, randint
from typing import Callable
from datetime import datetime, timedelta

from neopixel import NeoPixel
from lights.animations import Animation, Animator, Color, animator, get_random_color
from lights.layout.maze import maze
from lights.timing import Interval

class MazeRunner:
    prev_location: int
    location: int
    color: Color
    move_interval: Interval

    def __init__(
        self, color: Color, starting_location: int
    ):
        self.location = starting_location
        self.prev_location = starting_location
        self.color = color
        self.move_interval = Interval(timedelta(milliseconds=choice(100, 200, 300, 400, 500)))

    def tick(self):
        if not self.move_interval.is_ready():
            return
        
        new_location: int
        node = maze.graph[self.location]
        match node:
            case [prev, turn, next]:
                new_location = choice(list({prev, turn, next} - {self.prev_location}))
            case [prev, next]:
                if self.prev_location == prev:
                    new_location = next
                else:
                    new_location = prev
            case [back]:
                new_location = back
                self.color = get_random_color()

        self.prev_location = self.location
        self.location = new_location


class MazeRunnerAnimation(Animation):
    maze_runners: list[MazeRunner]

    def __init__(self, *, on_finished: Callable[[], None] | None = None) -> None:
        super().__init__(on_finished=on_finished)

        self.maze_runners = [
            MazeRunner(self.get_random_color(), location) for location in maze.dead_ends
        ]
        self.maze_runners = self.maze_runners[0:3]

    def run(self, pixels: NeoPixel, animator: Animator) -> None:
        maze_runner_locations: set[int] = set()
        for maze_runner in self.maze_runners:
            maze_runner.tick()
            location = maze_runner.location
            maze_runner_locations.add(location)
            pixels[location] = maze_runner.color


        for led in range(len(pixels)):
            if led not in maze_runner_locations:
                pixels[led] = self.fade_out(pixels[led], step=5)


def setup():
    animator.add_animation(MazeRunnerAnimation())