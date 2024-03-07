from datetime import datetime, timedelta
from typing import Callable, Literal, TypeAlias
import time

from neopixel import NeoPixel
import board
import colors

from lights.timing import is_after

Color: TypeAlias = tuple[int, int, int] | list[int, int, int]
OnFinished: TypeAlias = Callable[[], None] | None
wheel = colors.ColorWheel()

def to_pixel(color: colors.Color):
    return tuple([int(c) for c in color.rgb])

def get_random_color():
    return to_pixel(wheel.next())

class Animation:
    _finished: bool
    _on_finished: Callable[[], None] | None

    def fade_out(self, pixel: Color, step=10):
        return (
            max(pixel[0] - step, 0),
            max(pixel[1] - step, 0),
            max(pixel[2] - step, 0),
        )

    def to_pixel(self, color: colors.Color):
        return to_pixel(color)

    def get_random_color(self):
        return get_random_color()

    def transition(self, from_color: tuple[int, int, int], to_color: tuple[int, int, int], step: int = 20):
        next_color = [0, 0, 0]
        for pos, val in enumerate(from_color):
            direction = 1 if to_color[pos] >= val else -1
            next_val = val + (step * direction)
            next_color[pos] = min(to_color[pos], next_val) if direction == 1 else max(next_val, to_color[pos])

        return next_color

    def compare_color(self, c1: Color, c2: Color):
        return tuple(c1) == tuple(c2)
    
    def __init__(self, *, on_finished: OnFinished = None) -> None:
        self._finished = False
        self._on_finished = on_finished

    def is_finished(self):
        return self._finished

    def finished(self):
        self._finished = True

        if self._on_finished:
            self._on_finished()
    
    def run(self, pixels: NeoPixel, animator: "Animator") -> None:
        """
        If this functions return True, it will be removed from the animator. If it returns None,
        nothing happens. If it returns an Animation, then this animation will be replaced by the
        next animation.
        """
        raise NotImplementedError()

class Animator:
    frame_rate: float
    animations: list[Animation]
    animations_to_remove: set[Animation]
    animations_to_add: set[Animation]

    pixels: NeoPixel
    running: bool

    def __init__(self, *, frame_rate: float = 1/60) -> None:
        self.running = True
        self.frame_rate = frame_rate
        self.animations = []
        self.animations_to_remove = set()
        self.animations_to_add = set()

    def init_pixels(self, num_pixels: int, brightness=0.5):
        self.pixels = NeoPixel(board.D18, num_pixels, auto_write=False, brightness=brightness)

    def add_animation(self, *animations: list[Animation]):
        for animation in animations:
            self.animations_to_add.add(animation)

    def remove_animation(self, *animations: Animation):
        for animation in animations:
            self.animations_to_remove.add(animation)

    def replace_animation(self, animation: Animation, new_animation: Animation):
        self.remove_animation(animation)
        self.add_animation(new_animation)

    def clear(self):
        self.animations.clear()
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def stop(self):
        self.pixels.deinit()

    def run(self):
        for animation in self.animations:
            animation.run(pixels=self.pixels, animator=self)

            if animation.is_finished():
                self.remove_animation(animation)

        for animation in self.animations_to_remove:
            self.animations.remove(animation)

        self.animations_to_remove.clear()

        for animation in self.animations_to_add:
            self.animations.append(animation)

        self.animations_to_add.clear()

        self.pixels.show()
        time.sleep(self.frame_rate)


class AnimationGroup(Animation):
    animations: tuple[Animation]

    def __init__(self, animations: tuple[Animation], on_finished: OnFinished) -> None:
        super().__init__(on_finished=on_finished)
        self.animations = animations

    def run(self, pixels: NeoPixel, animator: Animator) -> None:
        all_finished = True
        for animation in self.animations:
            animation.run(pixels, animator)

            if not animation.is_finished():
                all_finished = False

        if all_finished:
            self.finished()


class FadeOutAnimation(Animation):
    def __init__(self, *, on_finished: Callable[[], None] | None = None) -> None:
        super().__init__(on_finished=on_finished)

    def run(self, pixels: NeoPixel, animator: Animator) -> None | Animation | None:
        is_faded_out = True

        for led, pixel in enumerate(pixels):
            if not self.compare_color(pixel, (0, 0, 0)):
                pixels[led] = self.fade_out(pixel)
                is_faded_out = False

        if is_faded_out:
            self.finished()

animator = Animator()