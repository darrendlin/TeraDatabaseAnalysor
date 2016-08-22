import os.path
import time
import json
import collections
import statistics

directory = "/media/sf_TeraStats/processing"
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


if __name__ == "__main__":
    start_time = time.time()

    analyzer = statistics.Analyzer()

    for encounter in parseall(directory):
        analyzer.consume(encounter)

    analyzer.results()

    print ("Errors:", errors)
    print("--- %s seconds ---" % (time.time() - start_time))


