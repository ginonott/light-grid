import click
import board
import neopixel
import re

@click.command()
@click.argument("leds", nargs=1, type=int)
def cycle(leds):
    print("This will turn each LED on and display its number. Press enter to move forward")
    
    if leds < 1:
        print(f"leds must be a positive integer. Got {leds}")
        exit(-1)

    pixels = neopixel.NeoPixel(board.D18, leds, auto_write=True)
    current_pixel = 0
    while True:
        pixels[current_pixel] = (255, 0, 0)
        inp = input(f"displaying LED {current_pixel}. Press enter to continue, b to go back, or a number to jump to that LED.\n> ")
        pixels[current_pixel] = (0, 0, 0)

        if re.match(r'^\d+$', inp):
            current_pixel = int(inp)
        elif inp == 'b':
            current_pixel -= 1
        else:
            current_pixel += 1

        if current_pixel >= leds:
            current_pixel = 0
        elif current_pixel < 0:
            current_pixel = leds - 1


if __name__ == "__main__":
    cycle()