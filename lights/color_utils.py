import colors

wheel = colors.ColorWheel()

def fade_out(curr_color, step=int(255 / 12)):
    return (
        max(curr_color[0] - step, 0),
        max(curr_color[1] - step, 0),
        max(curr_color[2] - step, 0),
    )

def to_pixel(color: colors.Color):
    return tuple([int(c) for c in color.rgb])


def get_random_color():
    return to_pixel(wheel.next())

def transition(from_color: tuple[int, int, int], to_color: tuple[int, int, int], step: int = 20):
    next_color = [0, 0, 0]
    for pos, val in enumerate(from_color):
        direction = 1 if to_color[pos] >= val else -1
        next_val = val + (step * direction)
        next_color[pos] = min(to_color[pos], next_val) if direction == 1 else max(next_val, to_color[pos])

    return next_color