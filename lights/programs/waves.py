from datetime import timedelta, datetime
from enum import Enum, auto
from random import choice
from typing import Callable, Literal

from neopixel import NeoPixel
from lights.animations import Animation, Animator, Color, animator
from lights.layout.grid import get_leds_in_row, get_leds_in_column, grid
from lights.timing import is_after, AnimationTiming

DEFAULT_DELTA = timedelta(milliseconds=150)
DEFAULT_WAVE_DELAY = timedelta(seconds=2)

class Modes(Enum):
    default = auto()
    clear_previous = auto()
    clear_previous_one_led = auto()

current_mode = [Modes.default, Modes.clear_previous, Modes.clear_previous_one_led]

class FillRow(Animation, AnimationTiming):
    current_row: int
    direction: Literal[-1, 1]
    color: Color
    delta: timedelta = DEFAULT_DELTA

    def __init__(self, *, reversed: bool = False, on_finished: Callable[[], None] | None = None) -> None:
        super().__init__(on_finished=on_finished)

        self.current_row = len(grid) - 1 if reversed else 0
        self.direction = -1 if reversed else 1
        self.color = self.get_random_color()

    def run(self, pixels: NeoPixel, animator: Animator) -> None:
        if not self.should_run():
            return
        
        leds = get_leds_in_row(self.current_row)

        if current_mode[0] == Modes.clear_previous_one_led:
            led = choice(list(leds))
            pixels[led] = self.color
        else:
            for led in leds:
                pixels[led] = self.color

        if current_mode[0] in (Modes.clear_previous, Modes.clear_previous_one_led):
            try:
                leds = get_leds_in_row(self.current_row - self.direction)
                for led in leds:
                    pixels[led] = (0, 0, 0)
            except:
                pass

        self.current_row += self.direction

        if self.current_row == len(grid) or self.current_row == -1:
            self.finished()

class FillColumn(Animation, AnimationTiming):
    current_column: int
    direction: Literal[-1, 1]
    color: Color
    delta: timedelta = DEFAULT_DELTA

    def __init__(self, *, reversed: bool = False, on_finished: Callable[[], None] | None = None) -> None:
        super().__init__(on_finished=on_finished)
        self.current_column = len(grid[0]) - 1 if reversed else 0
        self.direction = -1 if reversed else 1
        self.color = self.get_random_color()

    def run(self, pixels: NeoPixel, animator: Animator) -> None:
        if not self.should_run():
            return
        
        leds = get_leds_in_column(self.current_column)

        if current_mode[0] == Modes.clear_previous_one_led:
            led = choice(list(leds))
            pixels[led] = self.color
        else:
            for led in leds:
                pixels[led] = self.color

        if current_mode[0] in (Modes.clear_previous, Modes.clear_previous_one_led):
            try:
                leds = get_leds_in_column(self.current_column - self.direction)
                for led in leds:
                    pixels[led] = (0, 0, 0)
            except:
                pass

        self.current_column += self.direction

        if self.current_column >= len(grid[0]) or self.current_column == -1:
            self.finished()

class WaveGenerator(Animation):
    delay_between_waves: timedelta = DEFAULT_WAVE_DELAY
    last_wave: datetime
    animations: list[Animation]
    current_animation: int

    def __init__(self, animations: list[Animation], *, on_finished: Callable[[], None] | None = None) -> None:
        super().__init__(on_finished=on_finished)
        self.last_wave = datetime.now() - self.delay_between_waves
        self.animations = animations
        self.current_animation = 0

    def run(self, pixels: NeoPixel, animator: Animator) -> None:
        if is_after(self.last_wave, self.delay_between_waves) and self.current_animation < len(self.animations):
            self.last_wave = datetime.now()
            animator.add_animation(self.animations[self.current_animation])
            self.current_animation += 1

        all_finished = True
        for animation in self.animations:
            all_finished &= animation.is_finished()

        if all_finished:
            self.finished()

def set_next_animation():
    animations = [
        WaveGenerator(animations=[FillRow() for _ in range(10)], on_finished=lambda: set_next_animation()),
        WaveGenerator(animations=[FillRow(reversed=True) for _ in range(10)], on_finished=lambda: set_next_animation()),
        WaveGenerator(animations=[FillRow(reversed=(i % 2 == 0)) for i in range(10)], on_finished=lambda: set_next_animation()),
        WaveGenerator(animations=[FillColumn() for _ in range(10)], on_finished=lambda: set_next_animation()),
        WaveGenerator(animations=[FillColumn(reversed=True) for _ in range(10)], on_finished=lambda: set_next_animation()),
        WaveGenerator(animations=[FillColumn(reversed=(i % 2 == 0)) for i in range(10)], on_finished=lambda: set_next_animation()),
        WaveGenerator(animations=[FillColumn() if i % 2 == 0 else FillRow() for i in range(10)], on_finished=lambda: set_next_animation()),
        WaveGenerator(animations=[FillColumn(reversed=True) if i % 2 == 0 else FillRow(reversed=True) for i in range(10)], on_finished=lambda: set_next_animation()),
        WaveGenerator(animations=[FillColumn() if i % 2 == 0 else FillRow(reversed=True) for i in range(10)], on_finished=lambda: set_next_animation()),
        WaveGenerator(animations=[FillColumn(reversed=True) if i % 2 == 0 else FillRow() for i in range(10)], on_finished=lambda: set_next_animation()),
    ]

    animator.add_animation(choice(animations))

    
def setup():
    set_next_animation()


def change_modes():
    animator.clear()
    current_mode.append(current_mode.pop(0))
    set_next_animation()