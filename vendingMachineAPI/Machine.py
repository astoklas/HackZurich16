import time
import random
import uuid
import json

class Machine:
    #
    # Common base class for HackZurich16 Machine simulator
    #
    # Datastructure for a machine object
    # {
    #   id : someid,
    #   type : undefined,vendingmachine,other
    #   timestamp : timestamp
    #   data : [
    #     {
    #       id : id,
    #       value : val,
    #       type  : env_temperatur | op_temperatur | level | hummidity | power
    #       unit : C | F | %
    #     } ,
    #     {
    #       id : id,
    #       value : val,
    #       type  : temperatur | level | hummidity
    #       unit : C | F | % | W
    #     } ,
    #     {
    #       id : id,
    #       value : val,
    #       type  : temperatur | level | hummidity
    #       unit : C | F | %
    #     } ,
    #     ]
    #
    #
    #

    value = []
    lookup = [0, 1, 0, 1, 2, 3, 0, 5]
    myData = {'id': '', 'type': 'vendingmachine', 'timestamp': time.strftime("%d/%m/%Y-%X %Z"),'msgcounter' : '', 'data': []}
    msgcounter = 0
    lastreset = None
    lastclean = None
    starttime = None
    resetcount = 0
    cleancount = 0
    fillcount = 0
    lastfill = None


    def __init__(self, slots):
        for i in range(0, slots):
            self.value.append(100)
        self.myData['id'] = str(uuid.uuid4())
        self.nextIteration()
        self.msgcounter = 0
        self.starttime = time.strftime("%d/%m/%Y-%X %Z")
        self.lastreset = time.strftime("%d/%m/%Y-%X %Z")
        self.lastclean = time.strftime("%d/%m/%Y-%X %Z")
        self.lastfill = time.strftime("%d/%m/%Y-%X %Z")
        print self.myData

    def retriveValue(self):
        return json.dumps(self.myData, indent=2)

    def nextIteration(self):
        self.msgcounter = self.msgcounter + 1
        # Setting a time stamp
        self.myData['timestamp'] = time.strftime("%d/%m/%Y-%X %Z")
        self.myData['msgcounter'] = self.msgcounter
        self.myData['data'] = []
        for i in range(0, len(self.value)):
            self.value[i] = self.value[i] - self.lookup[random.randint(0, len(self.lookup)-1)]
            if self.value[i] < 0:
                self.value[i] = 0
            self.myData['data'].append(self.valStruct(self.value[i], id=i, type='level', unit="%", description='Supply Fill Level'))
        # Random Value for Tempertatur, Humudity and power
        self.myData['data'].append(self.valStruct(random.randint(10, 45), type='env_temperatur', description='Environment Temperatur'))
        self.myData['data'].append(self.valStruct(random.randint(-5, 15), type='op_temperatur', description='Operational Temperatur'))
        self.myData['data'].append(self.valStruct(random.randint(0, 100), type='humidity', unit="%", description='Environment Humidity'))
        self.myData['data'].append(self.valStruct(random.randint(300, 1500), type='power', unit="W", description='Power Consumption'))
        return json.dumps(self.myData)

    def sumFill(self):
        return sum(self.value)

    def refill(self):
        for i in range(0,len(self.value)):
            self.value[i] = 100
        self.fillcount = self.fillcount + 1
        self.lastfill = time.strftime("%d/%m/%Y-%X %Z")
        return

    def clean(self):
        self.lastclean = time.time()
        self.cleancount = self.cleancount + 1
        return

    def reset(self):
        self.msgcounter = 0
        self.refill(self)
        self.clean(self)
        self.lastreset = time.strftime("%d/%m/%Y-%X %Z")
        self.resetcount = self.resetcount + 1
        return

    def statistics(self):
        stats = { "id" : self.myData['id'], "start": self.starttime, "msgcount" : self.msgcounter, "lastreset":  self.lastreset, "resetcount": self.resetcount ,"lastclean":  self.lastclean,"cleancount": self.cleancount, "lastfill": self.lastfill, "fillcount": self.fillcount }
        return json.dumps(stats)
    #
    # With a little helper from my friends to write values in the json struct
    #
    def valStruct(self, val, id=0, type="temperatur", unit="C", description=""):
        return {"id": id, "value": val, "type": type, "unit":unit, "description":description}

#
# Main Code
#


