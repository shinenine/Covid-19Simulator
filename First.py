import math
from World import World


def DistanceCount(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


start = World(100, 0.0001, True, 0.33, 6000)  # 床位，杀伤力，治愈者是否带有抗体
start.Happen()
