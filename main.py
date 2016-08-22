import os.path
import time
import json
import collections
import statistics

directory = "G:\TeraStats\processing"
#directory = "../tera_data_full"
errors = 0

#thanks to Loriri for these
moonrunes = {
    "인술사": "Ninja", 
    "비검사": "Reaper", 
    "정령사": "Mystic", 
    "궁수": "Archer", 
    "사제": "Priest", 
    "광전사": "Berserker", 
    "창기사": "Lancer", 
    "권술사": "Brawler", 
    "무사": "Slayer", 
    "검투사": "Warrior", 
    "마공사": "Gunner", 
    "마법사": "Sorcerer", 
}

def translate_moonrune_classes(encounter):
    for member in encounter["members"]:
        if member["playerClass"] in moonrunes:
            member["playerClass"] = moonrunes[member["playerClass"]]


def parse(filename):
    global errors
    with open(filename) as data_file:
        try:
            data = json.load(data_file)
            return data
        except:
          errors += 1

        return None


def parseall(datadir):
    for root, dirs, files in os.walk(datadir):
        for fight in files:
            data = parse(os.path.join(root, fight))
            if(data == None ): 
                continue
            translate_moonrune_classes(data)

            yield data

def count_files(datadir):
    res = 0

    for root, dirs, files in os.walk(datadir):
        res += len(files)

    return res


if __name__ == "__main__":
    start_time = time.time()

    print("Counting encounters...")
    total = count_files(directory)

    print(total, "encounters")
    print("Loading statistic colectors...")

    analyzer = statistics.Analyzer()

    print("Loaded", *[type(obj).__name__ for obj in analyzer.stats])

    loaded = 0
    for encounter in parseall(directory):
        if loaded % 42 == 0:
            print ("\rParsing {:.4%}".format(loaded / total), end="")

        analyzer.consume(encounter)
        loaded += 1

    print ("\rParsing {:.4%}".format(loaded / total))
    print ()

    print ("Collecting results... ")
    analyzer.results()


    print("{:-^40}".format(" {:.2f} seconds ".format(time.time() - start_time)))
    print ("Errors:", errors)


