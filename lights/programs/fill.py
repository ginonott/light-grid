from typing import Literal
from enum import Enum, auto
from random import choice

from neopixel import NeoPixel
from lights.animations import Animation, AnimationGroup, Animator, Color, FadeOutAnimation, OnFinished, animator
from lights.layout.grid import get_column_sections, get_leds_inside_of_columns, get_leds_inside_of_rectangle, get_leds_inside_of_rows, get_leds_left_of_column, get_leds_outside_of_rectangle, get_leds_right_of_column, get_row_sections, grid, get_leds_above_row, get_leds_below_row

class Modes(Enum):
    default = auto()
    fade_out = auto()

current_mode = Modes.default

class FillBaseAnimation(Animation):
    target_color: Color
    def __init__(self, *, on_finished: OnFinished = None) -> None:
        super().__init__(on_finished=on_finished)
        self.target_color = self.get_random_color()

    def get_leds(self) -> list[int] | set[int]:
        raise NotImplementedError()
    
    def get_target_color(self):
        return self.target_color

    def on_leds_filled(self):
        raise NotImplementedError()

    def run(self, pixels: NeoPixel, animator: Animator) -> None:
        filled = True
        for led in self.get_leds():
            target_color = self.get_target_color()

            if not self.compare_color(pixels[led], target_color):
                pixels[led] = self.transition(pixels[led], target_color)
                filled = False
        
        if filled:
            self.on_leds_filled()


class FillRowAnimation(FillBaseAnimation):
    target_color: Color
    current_row: int
    target_row: int
    starting_row: int
    direction: int
    leds: set

    def __init__(self, starting_row: int, target_row: int, *, on_finished: OnFinished = None) -> None:
        super().__init__(on_finished=on_finished)
        self.target_color = self.get_random_color()
        self.current_row = starting_row
        self.starting_row = starting_row
        self.target_row = target_row
        self.direction = 1 if starting_row <= target_row else -1

    def get_leds(self) -> list[int] | set[int]:
        if self.direction == 1:
            # bottom to top fill
            return get_leds_inside_of_rows(self.starting_row, self.current_row)
        else:
            return get_leds_inside_of_rows(self.current_row, self.starting_row)
        
    def on_leds_filled(self):
        if self.current_row == self.target_row:
            self.finished()
        else:
            self.current_row += self.direction


class FillColAnimation(FillBaseAnimation):
    target_color: Color
    starting_col: int
    current_col: int
    target_col: int
    direction: int
    leds: set

    def __init__(self, starting_col: int, target_col: int, *, on_finished: OnFinished = None) -> None:
        super().__init__(on_finished=on_finished)
        self.target_color = self.get_random_color()
        self.current_col = starting_col
        self.target_col = target_col
        self.starting_col = starting_col
        self.direction = 1 if starting_col <= target_col else -1

    def get_leds(self) -> list[int] | set[int]:
        if self.direction == 1:
            # left to right fill
            return get_leds_inside_of_columns(self.starting_col, self.current_col)
        else:
            return get_leds_inside_of_columns(self.current_col, self.starting_col)
        
    def on_leds_filled(self):
        if self.current_col == self.target_col:
            self.finished()
        else:
            self.current_col += self.direction


class FillOutsideRectangleAnimation(FillBaseAnimation):
    r1: int
    r2: int
    c1: int
    c2: int

    def __init__(self, *, on_finished: OnFinished = None) -> None:
        super().__init__(on_finished=on_finished)
        self.r1 = 0
        self.r2 = len(grid)
        self.c1 = 0
        self.c2 = len(grid[0])

    def get_leds(self) -> list[int] | set[int]:
        return get_leds_outside_of_rectangle(self.r1, self.r2, self.c1, self.c2)
        
    def on_leds_filled(self):
        if self.r1 == self.r2 and self.c1 == self.c2:
            self.finished()
            return
        
        self.r1 += 1
        self.r2 -= 1
        self.c1 += 1
        self.c2 -= 1

        if self.r1 > self.r2:
            self.r1 = self.r2

        if self.c1 > self.c2:
            self.c1 = self.c2


class FillInsideRectangleAnimation(FillBaseAnimation):
    r1: int
    r2: int
    c1: int
    c2: int

    def __init__(self, *, on_finished: OnFinished = None) -> None:
        super().__init__(on_finished=on_finished)
        self.r1 = int(len(grid)/2)
        self.r2 = int(len(grid)/2)
        self.c1 = int(len(grid[0])/2)
        self.c2 = int(len(grid[0])/2)

    def get_leds(self) -> list[int] | set[int]:
        return get_leds_inside_of_rectangle(self.r1, self.r2, self.c1, self.c2)
        
    def on_leds_filled(self):
        if self.r1 < 0 and self.r2 >= len(grid) and self.c1 < 0 and self.c2 >= len(grid[0]):
            self.finished()
            return
        
        self.r1 -= 1
        self.r2 += 1
        self.c1 -= 1
        self.c2 += 1


def get_next_animation():
    def on_finished():
        if current_mode == Modes.fade_out:
            animator.add_animation(FadeOutAnimation(on_finished=lambda: animator.add_animation(get_next_animation())))
        else:
            animator.add_animation(get_next_animation())

    return choice(
        (
            FillRowAnimation(0, len(grid), on_finished=on_finished),
            FillRowAnimation(len(grid), 0, on_finished=on_finished),
            FillColAnimation(0, len(grid[0]), on_finished=on_finished),
            FillColAnimation(len(grid[0]), 0, on_finished=on_finished),
            AnimationGroup((
                FillRowAnimation(0, int(len(grid) / 2)),
                FillRowAnimation(len(grid), int(len(grid) / 2)),
            ), on_finished=on_finished),
            AnimationGroup((
                FillRowAnimation(int(len(grid) / 2) - 1, 0),
                FillRowAnimation(int(len(grid) / 2), len(grid)),
            ), on_finished=on_finished),
            AnimationGroup((
                FillColAnimation(0, int(len(grid[0]) / 2)),
                FillColAnimation(len(grid[0]), int(len(grid[0]) / 2)),
            ), on_finished=on_finished),
            FillOutsideRectangleAnimation(on_finished=on_finished),
            FillInsideRectangleAnimation(on_finished=on_finished),
        )
    )


def setup():
    animator.add_animation(get_next_animation())


def change_modes():
    global current_mode
    if current_mode == Modes.default:
        current_mode = Modes.fade_out
    else:
        current_mode = Modes.default