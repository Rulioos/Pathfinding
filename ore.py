import random


class Ore:
    """
    An ore is an entity that can be consumed by a miner.
    Each Ore has a value and a capacity.
    If the ore is empty then there is no point trying to mine it.
    """

    def __init__(self, value, capacity, weight):
        self.value = value
        self.capacity = capacity
        self.weight = weight
        self.use = 0

    def is_empty(self):
        return self.use >= self.capacity


class BlueOre(Ore):
    """
    Blue ore is the less valuable ore
    """

    def __init__(self):
        super().__init__(value=1, weight=1, capacity=random.random(1, 5))


class RedOre(Ore):
    """
    Red ore is the most valuable ore.
    """

    def __init__(self):
        super().__init__(value=2, weight=2, capacity=random.random(2, 7))
