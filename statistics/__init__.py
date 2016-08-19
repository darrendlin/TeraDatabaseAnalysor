_registered = []

def statistic(cls):
    global _registered
    _registered += [cls]


class Analyzer:
    def __init__(self):
        self.stats = [cls() for cls in _registered]

    def consume(self, json):
        for obj in self.stats:
            obj.consume(json)

    def results(self):
        for obj in self.stats:
            obj.results()

import statistics.class_count