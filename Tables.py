import random
import time,datetime

class TableClass:
    def __init__(self):
        self.nr_of_items = 0
        self.items = []
        self.priority = 0
        self.ocupped = False

    def orderGenerator(self):
        self.nr_of_items = random.randint(1, 10)
        self.priority = random.randint(1,5)
        #print("nr of items:" + str(self.nr_of_items))
        #print("priority:" + str(self.priority))
        for i in range(self.nr_of_items):
            foodid = random.randint(1,13)
            self.items.append(foodid)
        self.ocupped = True
        #print("items" + str(self.items))
