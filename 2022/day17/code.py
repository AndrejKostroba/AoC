from time import perf_counter


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(perf_counter()-t) + ' sec')
        return ret
    return wrapper_method


minus = [
    list("####")
]
plus = [
    list(".#."),
    list("###"),
    list(".#."),
]

l = [
    list("..#"),
    list("..#"),
    list("###"),
][::-1]

eye = [
    ["#"], ["#"], ["#"], ["#"]
]

square = [
    list("##"),
    list("##")
]

shapes = [minus, plus, l, eye, square]


class grid:
    def __init__(self, pattern) -> None:
        self.data = set()
        self.top = 0
        self.current_shape_idx = 0
        self.shape_x = 2
        self.shape_y = 3
        self.settled = 0
        self.pattern = pattern
        self.pat_idx = 0

    def can_move_horizontal(self, direction) -> bool:
        if direction == "<":
            nx = self.shape_x - 1
        else:
            nx = self.shape_x + 1

        if nx in [-1, 7]:
            return False

        for y, l in enumerate(shapes[self.current_shape_idx]):
            for x, c in enumerate(l):
                if c == "#":
                    if (nx + x, self.shape_y + y) in self.data or nx + x > 6:
                        return False
        return True

    def can_move_down(self) -> bool:
        ny = self.shape_y - 1

        if ny < 0:
            return False

        for y, l in enumerate(shapes[self.current_shape_idx]):
            for x, c in enumerate(l):
                if c == "#":
                    if (self.shape_x + x, ny + y) in self.data:
                        return False
        return True

    def move(self):
        direction = self.pattern[self.pat_idx % len(self.pattern)]
        self.pat_idx = self.pat_idx + 1

        if self.can_move_horizontal(direction):
            if direction == "<":
                self.shape_x -= 1
            else:
                self.shape_x += 1

        if self.can_move_down():
            self.shape_y -= 1
        else:
            return True

        return False

    def drop(self):
        while True:
            ret = self.move()
            if ret:
                break

        self.draw()
        self.settled += 1

    def get_top(self) -> int:
        return max(c[1] for c in self.data)

    def draw(self):
        for y, l in enumerate(shapes[self.current_shape_idx]):
            for x, c in enumerate(l):
                if c == "#":
                    self.data.add((self.shape_x + x, self.shape_y + y))

        self.settled += 1
        self.top = self.get_top()
        self.current_shape_idx = (self.current_shape_idx + 1) % 5
        self.shape_x = 2
        self.shape_y = self.top + 3 + 1

    def plot(self):
        buff = []
        for y in range(100):
            st = ""
            for x in range(7):
                st += "#" if (x, y) in self.data else "."
            buff.append(st)

        for l in buff[::-1]:
            print(l)

    def find_pattern(self):
        pass


@profiler
def part1():
    g = grid(open("day17/input.txt").read())

    for _ in range(2022):
        g.drop()

    print(g.get_top() + 1)


@profiler
def part2():
    pass


if __name__ == "__main__":

    part1()
    part2()
