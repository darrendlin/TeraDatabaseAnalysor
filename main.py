import os
import time
import json

class Analysor:

    priest = 0
    mystic = 0
    ninja = 0
    slayer = 0
    warrior = 0
    lancer = 0
    brawler = 0
    gunner = 0
    archer = 0
    sorcerer = 0
    berserker = 0
    reaper = 0
    errors = 0

    def parse(self, filename):
        with open(filename) as data_file:
            try:
               data = json.load(data_file)
            except ValueError as e :
              self.errors = self.errors+1
            else:
                #pprint(data)
                for member in data["members"]:
                    playerClass=member["playerClass"]
                    if playerClass == "Mystic":
                        self.mystic = self.mystic+1
                    elif playerClass == "Priest":
                        self.priest = self.priest+1
                    elif playerClass == "Slayer":
                        self.slayer = self.slayer+1
                    elif playerClass == "Warrior":
                        self.warrior = self.warrior+1
                    elif playerClass == "Gunner":
                        self.gunner = self.gunner+1
                    elif playerClass == "Archer":
                        self.archer = self.archer+1
                    elif playerClass == "Berserker":
                        self.berserker = self.berserker+1
                    elif playerClass == "Ninja":
                        self.ninja = self.ninja+1
                    elif playerClass == "Brawler":
                        self.brawler = self.brawler+1
                    elif playerClass == "Lancer":
                        self.lancer = self.lancer+1
                    elif playerClass == "Reaper":
                        self.reaper = self.reaper+1
                    elif playerClass == "Sorcerer":
                        self.sorcerer = self.sorcerer +1


    def printstats(self):
        print("Mystic:" + str(self.mystic))
        print("Priest:" + str(self.priest))
        print("Slayer:" + str(self.slayer))
        print("Berserker:" + str(self.berserker))
        print("Warrior:" + str(self.warrior))
        print("Reaper:" + str(self.reaper))
        print("Lancer:" + str(self.lancer))
        print("Ninja:" + str(self.ninja))
        print("Archer:" + str(self.archer))
        print("Gunner:" + str(self.gunner))
        print("Brawler:" + str(self.brawler))
        print("Sorcerer:" + str(self.sorcerer))
        print("Invalid json files:"+str(self.errors))

    def __init__(self):

        for boss in os.listdir('/media/sf_Stats/processing/'):
             #print(boss)
             for fight in os.listdir('/media/sf_Stats/processing/'+boss):
                 self.parse('/media/sf_Stats/processing/'+boss+'/'+fight)
        self.printstats()

start_time = time.time()
analysor = Analysor()
print("--- %s seconds ---" % (time.time() - start_time))