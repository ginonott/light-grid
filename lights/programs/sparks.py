from typing import Callable
from lights.animations import Animation, Animator, Color, animator
from lights.layout.maze import LedMaze, maze
from random import shuffle
import neopixel

clear_previous_pixels = False

def find_path(maze: LedMaze, start: int, end: int) -> list[int]:
    def _find_path(prev_pos: int, cur_pos: int, path: list[int]) -> bool:
        path.append(cur_pos)

        if cur_pos == end:
            return True
        
        # no backtracking
        options = set(maze.graph[cur_pos]) - {prev_pos}

        # no where left to go
        if not options:
            return False
        
        for opt in options:
            found_path = _find_path(cur_pos, opt, path)

            if found_path:
                return True
            else:
                path.pop()

        # path.append(prev_pos)
        return False
    
    path = [start]
    _find_path(start, start, path)
    return path

class SparksAnimation(Animation):
    path: list[int]
    color: Color

    def __init__(self, *, on_finished: Callable[[], None] | None = None) -> None:
        super().__init__(on_finished=on_finished)

        dead_ends = list(maze.dead_ends)
        shuffle(dead_ends)
        start, stop = dead_ends.pop(), dead_ends.pop()

    
        self.path = find_path(maze, start, stop)
        self.color = self.get_random_color()

    def run(self, pixels: neopixel.NeoPixel, animator: Animator) -> None:
        current_led = self.path[0]
        if self.compare_color(pixels[current_led], self.color):
            self.path.pop(0)
        else:
            pixels[current_led] = self.transition(pixels[current_led], self.color)

        if clear_previous_pixels:
            for led in range(len(pixels)):
                if led != current_led and not self.compare_color(pixels[led], (0,0,0)):
                    pixels[led] = self.transition(pixels[led], (0, 0, 0), step=1)

        if len(self.path) == 0:
            self.finished()
            animator.add_animation(SparksAnimation())

def setup():
    animator.add_animation(SparksAnimation())


def change_modes():
    global clear_previous_pixels
    print("here!")
    clear_previous_pixels = not clear_previous_pixels