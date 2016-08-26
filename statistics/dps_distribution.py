from statistics import statistic
from functools import partial
from collections import defaultdict
from matplotlib import pyplot
import numpy
import os.path

#collumns of 50k/s
GRANULARITY = 50000
MAX_DPS = 2500000
TICS_SPACING = 500000
MULTIPLIER = 1000000

class Histogram:
    def __init__(self, granularity):
        self.granularity = granularity
        self.data = defaultdict(int)

    def consume(self, value):
        if value > MAX_DPS: return

        collumn = value // self.granularity
        self.data[collumn] += 1

    def __iter__(self):
        size = max(self.data) + 1
        yield from [self.data[i] for i in range(size)]

    def export(self, filename):
        indices = numpy.arange(0, MAX_DPS / MULTIPLIER, GRANULARITY / MULTIPLIER)
        values = list(self)
        values += [0 for i in range(len(values), len(indices))]

        f = open(filename, 'w')
        for i in range(0, len(values) - 1):
            f.write("{}:{}\n".format(round(indices[i], 2), values[i]))
        f.close()

GranularHistogram = partial(Histogram, GRANULARITY)

@statistic
class DpsDistribution:
    def __init__(self):
        self.total = GranularHistogram()
        self.bycls = defaultdict(GranularHistogram)
        self.byboss = defaultdict(GranularHistogram)
        self.byclsboss = defaultdict(GranularHistogram)

    def consume(self, encounter, basedir, filename):
        boss = encounter["areaId"] + "." + encounter["bossId"]

        for member in encounter["members"]:
            dps = int(member["playerDps"])
            cls = member["playerClass"]
            
            self.total.consume(dps)
            self.bycls[cls].consume(dps)
            self.byboss[boss].consume(dps)
            self.byclsboss[(cls, boss)].consume(dps)

    def results(self):
        for dirname in ["data/dps/by_class", "data/dps/by_boss", "data/dps/by_class_boss"]:
            if os.path.isdir(dirname): continue

            #should probably delete it here, cause if it's a file it will fail, but meh
            os.makedirs(dirname)

        print ("Creating total")

        self.total.export("data/dps/total.txt")
        
        print ("Creating class histograms")
        for cls, plot in self.bycls.items():
            plot.export("data/dps/by_class/{}.txt".format(cls))

        print ("Creating boss histograms")
        for boss, plot in self.byboss.items():
            plot.export("data/dps/by_boss/{}.txt".format(boss))

        print ("Creating class-boss histograms")
        for (cls, boss), plot in self.byclsboss.items():
            dirname = "data/dps/by_class_boss/"+boss+"/"
            if os.path.isdir(dirname): continue
            os.makedirs(dirname)
            plot.export(dirname+"{}.txt".format(cls))
