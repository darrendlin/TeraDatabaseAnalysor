from statistics import statistic
import collections
@statistic

class ClassCount:
    def __init__(self):
        self.data = collections.defaultdict(int)

    def consume(self, encounter):
        for member in encounter["members"]:
            self.data[member["playerClass"]] += 1

    def results(self):
        f = open('class_count.txt', 'w')
        for cls, count in self.data.items():
            f.write("{}:{}\n".format(cls, count))
        f.close()
