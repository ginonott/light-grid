# from random import choice
# from maze import LedMaze, maze

# import time
# import board
# import neopixel
# import colors


# def fade_out(curr_color, step=int(255 / 12)):
#     return (
#         max(curr_color[0] - step, 0),
#         max(curr_color[1] - step, 0),
#         max(curr_color[2] - step, 0),
#     )

# def to_pixel(color: colors.Color):
#     return tuple([int(c) for c in color.rgb])


# class MazeRunner:
#     prev_location: int
#     location: int
#     maze: LedMaze
#     color: colors.Color
#     flip: bool

#     def __init__(
#         self, maze: LedMaze, color: colors.Color, starting_location: int
#     ):
#         self.location = starting_location
#         self.prev_location = starting_location
#         self.maze = maze
#         self.color = color
#         self.flip = False

#     def tick(self):
#         if self.flip:
#             self.flip = False
#             return
        
#         new_location: int
#         node = self.maze.graph[self.location]
#         match node:
#             case [prev, turn, next]:
#                 new_location = choice(list({prev, turn, next} - {self.prev_location}))
#             case [prev, next]:
#                 if self.prev_location == prev:
#                     new_location = next
#                 else:
#                     new_location = prev
#             case [back]:
#                 new_location = back

#         self.prev_location = self.location
#         self.location = new_location
#         self.flip = True

#     def rgb(self):
#         return to_pixel(self.color)




# pixels = neopixel.NeoPixel(board.D18, 105, auto_write=False, brightness=0.2)
# pixels.fill((0, 0, 0))

# wheel = colors.ColorWheel()
# runner_colors = [
#     wheel.next(),
#     wheel.next(),
#     wheel.next(),
#     wheel.next(),
#     wheel.next(),
#     wheel.next(),
# ]
# maze_runners = [
#     MazeRunner(maze, runner_colors.pop(), location) for location in maze.dead_ends
# ]

# while True:
#     maze_runner_locations: dict[int, MazeRunner] = {}
#     for maze_runner in maze_runners:
#         maze_runner.tick()
#         location = maze_runner.location

#         if other := maze_runner_locations.get(location):
#             pixels[location] = to_pixel(maze_runner.color.overlay(other.color))
#         else:
#             r, g, b = pixels[location]
#             if (r, g, b) != (0, 0, 0):
#                 c = colors.RGBColor(r, g, b)
#                 pixels[location] = to_pixel(maze_runner.color.overlay(c))
#             else:
#                 pixels[location] = to_pixel(maze_runner.color)
            
#         maze_runner_locations[maze_runner.location] = maze_runner

#     for led in range(len(pixels)):
#         if led not in maze_runner_locations:
#             pixels[led] = fade_out(pixels[led], step=5)

#     pixels.show()
#     time.sleep(1 / 24)
