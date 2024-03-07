grid = [
#   0      1     2     3     4     5     6     7     8     9     10    11    12    13    14    15    16    17
    [None, 34  , 33  , 32  , 31  , 30  , 29  , 28  , 27  , 26  , 25  , 24  , 23  , 22  , 21  , 20  , 19  , None], # 0
    [35  , None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 18  ], # 1
    [36  , None, None, None, None, None, None, None, None, None, 80  , None, None, None, None, None, None, 17  ], # 2
    [37  , None, None, None, None, None, None, None, None, None, 79  , None, None, None, None, None, None, 16  ], # 3
    [38  , None, None, None, None, None, None, None, None, None, 78  , None, None, None, None, None, None, 15  ], # 4
    [39  , None, None, None, None, None, None, None, None, None, 77  , None, None, None, None, None, None, 14  ], # 5
    [40  , None, None, None, 68  , 69  , 70  , 71  , 72  , 73  , 74  , 75  , 76  , 81  , 82  , None, None, 13  ], # 6
    [41  , None, None, None, None, None, None, None, None, None, None, None, None, None, None, 83  , None, 12  ], # 7
    [42  , None, None, None, None, None, None, None, None, None, None, None, None, None, None, 84  , None, 11  ], # 8
    [43  , None, None, None, None, None, None, None, None, None, None, None, None, None, None, 85  , None, 10  ], # 9
    [45  , None, 67  , 66  , 65  , 64  , None, None, None, None, None, None, None, None, None, 86  , None, 9   ], # 10
    [46  , None, None, None, None, None, 63  , None, None, None, None, 103 , 104 , None, None, 87  , None, 8   ], # 11
    [47  , None, None, None, None, None, 62  , None, None, None, 102 , None, None, None, None, 88  , None, 7   ], # 12
    [48  , None, None, None, None, None, 61  , None, None, None, 101 , None, None, None, None, 89  , None, 6   ], # 13
    [49  , None, None, None, None, None, 60  , None, None, None, 100 , None, None, None, None, 90  , None, 5   ], # 14
    [None, None, None, None, None, None, 59  , None, None, None, 99  , 94  , 93  , 92  , 91  , None, None, 4   ], # 15
    [None, None, None, None, None, None, 58  , None, None, None, 98  , None, None, None, None, None, None, 3   ], # 16
    [None, None, None, None, None, None, 57  , None, None, None, 97  , None, None, None, None, None, None, 2   ], # 17
    [None, None, None, None, None, None, 56  , None, None, None, 96  , None, None, None, None, None, None, 1   ], # 18
    [50  , 51  , 52  , 53  , 54  , 55  , None, None, None, None, 95  , None, None, None, None, None, None, 0   ], # 19
]

def get_leds_in_row(r: int):
    s = set()

    for led in grid[r]:
        if led is not None:
            s.add(led)

    return s

def get_leds_in_column(c: int):
    s = set()
    for row in grid:
        if (led := row[c]) is not None:
            s.add(led)

    return s

def get_leds_above_row(r: int) -> set[int]:
    s = set()
    for row_num, row in enumerate(grid):
        if row_num >= r:
            break

        for led in row:
            if led is not None:
                s.add(led)

    return s

def get_leds_below_row(r: int) -> set[int]:
    s = set()
    for row_num, row in enumerate(reversed(grid)):
        row_num = len(grid) - row_num
        if row_num <= r:
            break

        for led in row:
            if led is not None:
                s.add(led)

    return s

def get_leds_left_of_column(c: int) -> set[int]:
    s = set()
    for row in grid:
        for col, led in enumerate(row):
            if col >= c:
                break

            if led is not None:
                s.add(led)

    return s

def get_leds_right_of_column(c: int) -> set[int]:
    s = set()
    for row in grid:
        for col, led in enumerate(reversed(row)):
            col = len(row) - col
            if col <= c:
                break

            if led is not None:
                s.add(led)

    return s

# composite functions
def get_leds_inside_of_rows(r1: int, r2: int):
    if r1 > r2:
        raise ValueError(f"{r1=} must be less than {r2=}")
    
    return get_leds_above_row(r2).intersection(get_leds_below_row(r1))

def get_leds_outside_of_rows(r1: int, r2: int):
    if r1 > r2:
        raise ValueError(f"{r1=} must be less than {r2=}")
    
    return get_leds_above_row(r1).union(get_leds_below_row(r2))


def get_leds_inside_of_columns(c1: int, c2: int):
    if c1 > c2:
        raise ValueError(f"{c1=} must be less than {c2=}")
    
    return get_leds_left_of_column(c2).intersection(get_leds_right_of_column(c1))


def get_leds_outside_of_columns(c1: int, c2: int):
    if c1 > c2:
        raise ValueError(f"{c1=} must be less than {c2=}")
    
    return get_leds_left_of_column(c1).union(get_leds_right_of_column(c2))


def get_leds_inside_of_rectangle(r1: int, r2: int, c1: int, c2: int):
    return get_leds_inside_of_rows(r1, r2).intersection(get_leds_inside_of_columns(c1, c2))


def get_leds_outside_of_rectangle(r1: int, r2: int, c1: int, c2: int):
    return get_leds_outside_of_rows(r1, r2).union(get_leds_outside_of_columns(c1, c2))

def get_row_sections(num_sections: int):
    match num_sections:
        case 2:
            return ((0, 9), (10, 19))
        case 3:
            return ((0, 5), (6, 14), (15, 19))
        case _:
            return ((0, 19))

def get_column_sections(num_sections: int):
    sections = [[
        int(len(grid[0]) / num_sections) * section,
        int(len(grid[0]) / num_sections) * section + int(len(grid[0]) / num_sections)
     ] for section in range(num_sections)]
    
    sections[-1][1] = len(grid[0])

    return sections


if __name__ == '__main__':
    import neopixel
    import board

    running = True
    pixels = neopixel.NeoPixel(board.D18, 105, auto_write=False, brightness=0.1)
    while running:
        cmd = input("> ").split(" ")
        leds = set()
        match cmd:
            case ["exit"]:
                running = False
            case ["above", r]:
                leds = get_leds_above_row(int(r))
            case ["below", r]:
                leds = get_leds_below_row(int(r))
            case ["left", c]:
                leds = get_leds_left_of_column(int(c))
            case ["right", c]:
                leds = get_leds_right_of_column(int(c))
            case ["inside-rows", r1, r2]:
                leds = get_leds_inside_of_rows(int(r1), int(r2))
            case ["inside-columns", c1, c2]:
                leds = get_leds_inside_of_columns(int(c1), int(c2))
            case ["outside-rows", r1, r2]:
                leds = get_leds_outside_of_rows(int(r1), int(r2))
            case ["outside-columns", c1, c2]:
                leds = get_leds_outside_of_columns(int(c1), int(c2))
            case ["inside-rectangle", r1, r2, c1, c2]:
                leds = get_leds_inside_of_rectangle(int(r1), int(r2), int(c1), int(c2))
            case ["outside-rectangle", r1, r2, c1, c2]:
                leds = get_leds_outside_of_rectangle(int(r1), int(r2), int(c1), int(c2))

        pixels.fill((0, 0, 0))
        for led in leds:
            pixels[led] = (255, 0, 0)

        pixels.show()