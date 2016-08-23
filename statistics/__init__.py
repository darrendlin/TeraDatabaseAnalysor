_registered = []

def statistic(cls):
    global _registered
    _registered += [cls]


class Analyzer:
    def __init__(self):
        self.stats = [cls() for cls in _registered]

    def consume(self, json, basedir, filename):
        for obj in self.stats:
            obj.consume(json, basedir, filename)

    def results(self):
        for obj in self.stats:
            print("{:-^40}".format(" " + type(obj).__name__ + " "))

            obj.results()

import statistics.class_count
import statistics.dps_distribution