
class LedMaze:
    Graph = dict[int, list[int]]
    graph: dict[int, list[int]]
    dead_ends: set[int]

    def __init__(self) -> None:
        self.graph = {}
        self.dead_ends = set()

    def find_path(self, start: int, end: int) -> list[int]:
        def _find_path(prev_pos: int, cur_pos: int, path: list[int]) -> bool:
            path.append(cur_pos)

            if cur_pos == end:
                return True
            
            # no backtracking
            options = set(self.graph[cur_pos]) - {prev_pos}

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

    def bridge_segment(self, end_segment_led: int, start_segment_led: int):
        self.graph[end_segment_led] = [end_segment_led - 1, start_segment_led]
        self.graph[start_segment_led] = [end_segment_led, start_segment_led + 1]

    def make_segment(
        self,
        start_led: int,
        end_led: int,
        connect_start_to_prev: bool = True,
        connect_end_to_next: bool = True,
    ):
        if start_led in self.graph or end_led in self.graph:
            raise ValueError(
                f"{start_led} and {end_led} must not be in the graph already"
            )

        if end_led <= start_led:
            raise ValueError(f"start_led must be less than end_led")

        for led in range(start_led, end_led + 1):
            if led == start_led and not connect_start_to_prev:
                self.graph[led] = [led + 1]
            elif led == end_led and not connect_end_to_next:
                self.graph[led] = [led - 1]
            else:
                self.graph[led] = [led - 1, led + 1]

    def make_dead_end(self, dead_end_led: int, connecting_led: int):
        self.dead_ends.add(dead_end_led)

        self.graph[dead_end_led] = [connecting_led]

    def connect_fork(self, led_1, led_2):
        if led_1 not in self.graph or led_2 not in self.graph:
            raise ValueError(f"LED {led_1} and {led_2} must already be in the graph")

        self.graph[led_1].insert(1, led_2)
        self.graph[led_2].insert(1, led_1)


def build_maze():
    # build graph
    maze = LedMaze()

    # dead ends
    maze.make_dead_end(0, 1)
    maze.make_dead_end(49, 48)
    maze.make_dead_end(50, 51)
    maze.make_dead_end(68, 69)
    maze.make_dead_end(95, 96)
    maze.make_dead_end(104, 103)

    # continous segments
    maze.make_segment(1, 48)
    maze.make_segment(51, 67, connect_end_to_next=False)
    maze.make_segment(69, 76, connect_end_to_next=False)
    maze.make_segment(77, 80, connect_start_to_prev=False, connect_end_to_next=False)
    maze.bridge_segment(76, 81)
    maze.make_segment(82, 94, connect_end_to_next=False)
    maze.make_segment(96, 103)

    # connect forks
    maze.connect_fork(27, 80)
    maze.connect_fork(43, 67)
    maze.connect_fork(74, 77)
    maze.connect_fork(94, 98)

    return maze

maze = build_maze()