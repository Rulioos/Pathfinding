class Unit:
    """
    An Unit here is a moving character. It possesses stamina which determines how much time
    he can act without resting.
    It possesses a home which is a position that can be modified where the character can rest.
    It also possess a cost. It's the money needed to create such a unit.
    """

    def __init__(self, stamina, home, cost):
        self.home = home
        self.stamina = stamina
        self.exhaustion = 0
        self.cost = cost

    def is_exhausted(self):
        """
        We assume that each unit needs at least one stamina to go back home.
        :return: A boolean. If True the unit must rest. Else the unit can continue its work.
        """
        return self.exhaustion > self.stamina

    def rest(self):
        """
        Makes an unit recover.
        :return: None
        """
        self.exhaustion = 0

    def act(self):
        """
        Is used when the unit does an action. ( Mining for miner , exploring for explorer ... )
        :return:None
        """
        self.exhaustion += 1


class Explorer(Unit):
    """
    An Explorer is an Unit which goal is to explore the surroundings of his home.
    Its goal is to find the ore and inform the miners.
    It has a distance limit from his actual home. It can not go further.
    If the explorer can't find anymore ore in its range it will go back home and be destroyed.
    The cost of the unit will be refund.

    """

    def __init__(self, home, stamina, cost, max_distance):
        super().__init__(stamina=stamina, home=home, cost=cost)
        self.max_distance = max_distance

    def is_too_far(self, distance):
        return distance >= self.max_distance


class Miner(Unit):
    """
    A Miner is a unit that will mine the ore found by the explorer.
    Each ore has multiple uses and each use count as an action for the miner.
    If the miner inventory is full or its stamina is fully used it will go back home and
    empty his bag.
    The mined ore is only valuable once it's out of the miner bag.
    """

    def __init__(self, home, capacity, cost, stamina):
        super().__init__(stamina=stamina, home=home, cost=cost)
        self.capacity = capacity
        self.inventory = 0

    def is_full(self):
        return self.inventory >= self.capacity


class BronzeMiner(Miner):
    """
    BronzeMiner is the cheapest unit with the smallest bag and the smallest stamina.
    """

    def __init__(self, home):
        super().__init__(stamina=10, home=home, capacity=10, cost=5)


class SilverMiner(Miner):
    """
    SilverMiner is an intermediate unit.
    """

    def __init__(self, home):
        super().__init__(stamina=15, home=home, capacity=15, cost=15)


class GoldMiner(Miner):
    """
    GoldMiner is the most expensive unit but it has the best attributes.
    """

    def __init__(self, home):
        super().__init__(stamina=25, home=home, capacity=30, cost=30)
