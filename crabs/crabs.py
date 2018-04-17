class Crabs:
    _ROUTE = None
    _SEEDS = []

    @classmethod
    def set_route(cls, route):
        cls._ROUTE = route

    @classmethod
    def set_seeds(cls, seeds):
        if not isinstance(seeds, list):
            raise TypeError("List required.")
        cls._SEEDS = seeds

    @classmethod
    def run(cls):
        pass
