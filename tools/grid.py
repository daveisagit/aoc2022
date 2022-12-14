from collections import namedtuple

Point = namedtuple(
    "P", ["x", "y"]
)

ORTHOGONAL_DIRECTIONS = (
    Point(1, 0),
    Point(0, 1),
    Point(-1, 0),
    Point(0, -1),
)

DIAGONAL_DIRECTIONS = (
    Point(1, 1),
    Point(-1, 1),
    Point(-1, -1),
    Point(1, -1),
)

ALL_DIRECTIONS = ORTHOGONAL_DIRECTIONS + DIAGONAL_DIRECTIONS


def cmp_scalar(a, b):
    return (a > b) - (a < b)


def str_to_point(s: str) -> Point:
    """Parse a string to a Point tuple"""
    s = s.strip()
    ct = None
    if s.startswith(("(", "[", "{")):
        s = s[1:-1]
    if "," in s:
        ct = s.split(",")
    if " " in s:
        ct = s.split(" ")
    return Point(x=int(ct[0]), y=int(ct[1]))


def make_point(t: tuple) -> Point:
    return Point(t[0], t[1])


def point_sub(a: Point, b: Point) -> Point:
    return Point(*[x[0] - x[1] for x in zip(a, b)])


def point_add(a: Point, b: Point) -> Point:
    return Point(*[x[0] + x[1] for x in zip(a, b)])


def straight_path_of_points_between(a: Point, b: Point):
    """Generate a list of points between 2 points that vertical/horizontally aligned"""
    # diff = tuple([x[0]-x[1] for x in zip(a, b)])
    if not isinstance(a, Point):
        a = make_point(a)
    if not isinstance(b, Point):
        b = make_point(b)

    if a.x == b.x and a.y == b.y:
        yield a

    elif a.x == b.x:
        dy = 0 - cmp_scalar(a.y, b.y)
        for i in range(a.y, b.y + dy, dy):
            yield Point(x=a.x, y=i)

    elif a.y == b.y:
        dx = 0 - cmp_scalar(a.x, b.x)
        for i in range(a.x, b.x + dx, dx):
            yield Point(x=i, y=a.y)

    else:
        raise ValueError(f"Points {a},{b} are not aligned")


def limits_of_point_set(points) -> (Point, Point):
    """Given a lst/set of points what are the limits"""
    x_vals = [p.x for p in points]
    y_vals = [p.y for p in points]
    return Point(x=min(x_vals), y=min(y_vals)), Point(x=max(x_vals), y=max(y_vals))


def orthogonal_points(p: Point, dist=1, directions=ORTHOGONAL_DIRECTIONS):
    for direction in directions:
        trg = Point(*[o * dist for o in direction])
        yield point_add(p, trg)


assert Point(4, 5) == (4, 5)
assert list(straight_path_of_points_between((1, 3), (1, 5))) == [(1, 3), (1, 4), (1, 5)]
assert list(straight_path_of_points_between((7, 13), (7, 11))) == [(7, 13), (7, 12), (7, 11)]

# print(
#     list(
#         orthogonal_points(
#             Point(0, 0),
#             dist=5,
#             directions=ALL_DIRECTIONS
#         )
#     )
# )
