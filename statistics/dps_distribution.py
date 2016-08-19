from statistics import statistic
from functools import partial
from collections import defaultdict
from matplotlib import pyplot
import numpy
import os.path

#collumns of 50k/s
GRANULARITY = 50000

class Histogram:
    def __init__(self, granularity):
        self.granularity = granularity
        self.data = defaultdict(int)

    def consume(self, value):
        collumn = int(value) // self.granularity
        self.data[collumn] += 1

    def __iter__(self):
        size = max(self.data) + 1
        yield from [self.data[i] for i in range(size)]

    def export(self, filename):
        values = list(self)
        indices = numpy.arange(len(values))
        width = 1

        pyplot.bar(indices, values, width)
        pyplot.savefig(filename)
        pyplot.clf()

GranularHistogram = partial(Histogram, GRANULARITY)

@statistic
class DpsDistribution:
    def __init__(self):
        self.total = GranularHistogram()
        self.bycls = defaultdict(GranularHistogram)
        self.byboss = defaultdict(GranularHistogram)
        self.byclsboss = defaultdict(GranularHistogram)

    def consume(self, encounter):
        boss = encounter["areaId"] + "." + encounter["bossId"]

        for member in encounter["members"]:
            dps = member["playerDps"]
            cls = member["playerClass"]
            
            self.total.consume(dps)
            self.bycls[cls].consume(dps)
            self.byboss[boss].consume(dps)
            self.byclsboss[(cls, boss)].consume(dps)

    def results(self):
        for dirname in ["histograms/by_class", "histograms/by_boss", "histograms/by_class_boss"]:
            if os.path.isdir(dirname): continue

            #should probably delete it here, cause if it's a file it will fail, but meh
            os.makedirs(dirname)

        self.total.export("histograms/total.png")
        
        for cls, plot in self.bycls.items():
            plot.export("histograms/by_class/{}.png".format(cls))

        for boss, plot in self.byboss.items():
            plot.export("histograms/by_boss/{}.png".format(boss))

        for (cls, boss), plot in self.byclsboss.items():
            plot.export("histograms/by_class_boss/{}.{}.png".format(cls, boss))
