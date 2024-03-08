import click
from datetime import datetime, timedelta

from gpiozero import Button
from signal import signal, SIGINT, SIGHUP, SIGTERM
from lights.animations import animator
from lights.programs import fill, sparks, maze_runners, waves, lava_lamp

running = True

program_to_color = {
    fill: (255, 0, 0),
    sparks: (0, 255, 0),
    maze_runners: (0, 0, 255),
    waves: (255, 255, 0),
    lava_lamp: (255, 0, 255)
}

def stop_program(*args, **kwargs):
    global running
    running = False

for s in [SIGINT, SIGTERM]:
    signal(s, stop_program)

def handle_brightness_button_pressed(brightness_options: list[float]):
    last_clicked = datetime.now()
    def _handler():
        nonlocal last_clicked
        now = datetime.now()
        if (last_clicked + timedelta(milliseconds=500) < now):
            last_clicked = now
            brightness_options.append(brightness_options.pop(0))
            animator.pixels.brightness = brightness_options[0]

    return _handler

def handle_next_program_button_pressed(programs: list):
    last_clicked = datetime.now()
    def _handler():
        nonlocal last_clicked
        now = datetime.now()
        if (last_clicked + timedelta(seconds=1) < now):
            last_clicked = now
            animator.clear()
            programs.append(programs.pop(0))
            animator.flash_led(0, color=program_to_color[programs[0]])
            programs[0].setup()

    return _handler


def handle_options_button_pressed(programs: list):
    last_clicked = datetime.now()
    def _handler():
        nonlocal last_clicked
        now = datetime.now()
        if (last_clicked + timedelta(seconds=1) < now):
            if change_modes := getattr(programs[0], "change_modes", None):
                change_modes()

    return _handler

@click.command()
@click.option("-i", "--interactive", is_flag=True, default=False)
def main(interactive: bool):
    brightness_options = [0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    animator.init_pixels(105, brightness=brightness_options[0])

    programs = [lava_lamp, waves, maze_runners, fill, sparks]
    programs[0].setup()

    brightness_button = Button(17)
    brightness_button.when_pressed = handle_brightness_button_pressed(brightness_options)

    next_program_button = Button(27)
    next_program_button.when_pressed = handle_next_program_button_pressed(programs)

    options_button = Button(22)
    options_button.when_pressed = handle_options_button_pressed(programs)

    while running:
        animator.run()
        if interactive:
            input("> ")

    animator.stop()

if __name__ == '__main__':
    main()