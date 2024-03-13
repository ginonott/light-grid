from random import choice
from typing import Callable

from neopixel import NeoPixel
from lights.animations import Animation, Animator, Color, FadeOutAnimation, animator
from lights.layout.maze import maze
from lights.timing import FuzzyInterval


class LightningAnimation(Animation):
    paths: list[list[int]]
    color: Color
    target_color: Color
    delay_interval: FuzzyInterval | None

    def __init__(self, *, on_finished: Callable[[], None] | None = None) -> None:
        super().__init__(on_finished=on_finished)

        starting_point = choice(list(maze.dead_ends))
        ending_points = maze.dead_ends - {starting_point}
        self.paths = [
            maze.find_path(starting_point, ending_point)
            for ending_point in ending_points
        ]
        self.color = self.get_random_color()
        self.target_color = self.get_inverted_color(self.color)
        self.delay_interval = FuzzyInterval(10, 60)

    def run(self, pixels: NeoPixel, animator: Animator) -> None:
        if self.delay_interval:
            if not self.delay_interval.is_ready():
                return
            else:
                # clear the interval
                self.delay_interval = None
        
        is_finished = True
        for path in self.paths:
            if path:
                pixel = path.pop(0)
                is_finished = False
                pixels[pixel] = self.color

        if is_finished:
            self.finished()

        self.color = self.transition(self.color, self.target_color, step=2)


def setup():
    start_animation()

def start_animation():
     animator.add_animation(
        LightningAnimation(on_finished=lambda: animator.add_animation(
            FadeOutAnimation(step=1, on_finished=lambda: start_animation())
        ))
    )
