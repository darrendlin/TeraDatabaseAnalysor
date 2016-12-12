from statistics import statistic
from functools import partial
from collections import defaultdict
import numpy
import datetime
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
        self.bycls = defaultdict(GranularHistogram)
        self.byregioncls = defaultdict(GranularHistogram)
        self.byboss = defaultdict(GranularHistogram)
        self.byregionboss = defaultdict(GranularHistogram)
        self.bybosscls = defaultdict(GranularHistogram)
        self.byregionbosscls = defaultdict(GranularHistogram)
        self.bybossclsdate = defaultdict(GranularHistogram)
        self.byregionbossclsdate = defaultdict(GranularHistogram)

    def consume(self, encounter, directory):
        region = directory.split(".")[0]
        boss = encounter["areaId"] + "." + encounter["bossId"]
        timestamp = encounter["timestamp"]
        date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m')

        for member in encounter["members"]:

            dps = int(member["playerDps"])
            cls = member["playerClass"]
            self.bycls[cls].consume(dps)
            self.byregioncls[(region, cls)].consume(dps)
            self.byboss[boss].consume(dps)
            self.byregionboss[(region, boss)].consume(dps)
            self.bybosscls[(cls, boss)].consume(dps)
            self.byregionbosscls[(region, cls, boss)].consume(dps)
            self.bybossclsdate[(boss, cls, date)].consume(dps)
            self.byregionbossclsdate[(region, boss, cls, date)].consume(dps)


    def results(self):
        for dirname in ["data/dps/by_class", "data/dps/by_boss", "data/dps/by_class_boss"]:
            if os.path.isdir(dirname): continue

            #should probably delete it here, cause if it's a file it will fail, but meh
            os.makedirs(dirname)

        print ("Creating total")
        print ("Creating class histograms")
        for cls, plot in self.bycls.items():
            plot.export("data/dps/by_class/{}.txt".format(cls))

        print("Creating class histograms by region")
        for (region, cls), plot in self.byregioncls.items():
            dirname = "data/dps/by_region_class/" + region + "/"
            if not os.path.isdir(dirname): os.makedirs(dirname)
            plot.export(dirname + "{}.txt".format(cls))

        print ("Creating boss histograms")
        for boss, plot in self.byboss.items():
            plot.export("data/dps/by_boss/{}.txt".format(boss))

        print("Creating boss histograms by region")
        for (region, boss), plot in self.byregionboss.items():
            dirname = "data/dps/by_region_boss/" + region + "/"
            if not os.path.isdir(dirname): os.makedirs(dirname)
            plot.export(dirname + "{}.txt".format(boss))

        print ("Creating class-boss histograms")
        for (cls, boss), plot in self.bybosscls.items():
            dirname = "data/dps/by_boss_class/"+boss+"/"
            if not os.path.isdir(dirname): os.makedirs(dirname)
            plot.export(dirname+"{}.txt".format(cls))

        print("Creating class-boss histograms by region")
        for (region, cls, boss), plot in self.byregionbosscls.items():
            dirname = "data/dps/by_boss_region_class/" + boss + "/" + cls + "/"
            if not os.path.isdir(dirname): os.makedirs(dirname)
            plot.export(dirname + "{}.txt".format(region))

        print("Creating boss-class-date histograms")
        for (boss, cls, date), plot in self.bybossclsdate.items():
            dirname = "data/dps/by_boss_class_date/" + boss + "/"+cls+"/"
            if not os.path.isdir(dirname): os.makedirs(dirname)
            plot.export(dirname + "{}.txt".format(date))

        print("Creating boss-class-date histograms by region")
        for (region, boss, cls, date), plot in self.byregionbossclsdate.items():
            dirname = "data/dps/by_boss_class_region_date/" + boss + "/" + cls + "/" + region + "/"
            if not os.path.isdir(dirname): os.makedirs(dirname)
            plot.export(dirname + "{}.txt".format(date))