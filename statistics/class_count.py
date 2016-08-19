from statistics import statistic
import collections

@statistic
class Class_Count:
    def __init__(self):
        self.data = collections.defaultdict(int)

    def consume(self, encounter):
        for member in encounter["members"]:
            self.data[member["playerClass"]] += 1

    def results(self):
        for cls, count in self.data.items():
            print (cls.encode("utf8"), count)