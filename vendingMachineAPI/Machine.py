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
    #       type  : temperatur | level | hummidity | power
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
    myData = {'id': '', 'type': 'vendingmachine', 'timestamp': time.time(),'cleancounter' : '', 'data': []}
    cleancounter = 0

    def __init__(self, slots):
        for i in range(0, slots):
            self.value.append(100)
        self.myData['id'] = str(uuid.uuid4())
        self.nextIteration()

    def retriveValue(self):
        return json.dumps(self.myData, indent=2)

    def nextIteration(self):
        self.cleancounter = self.cleancounter + 1
        # Setting a time stamp
        self.myData['timestamp'] = time.time()
        self.myData['cleancounter'] = self.cleancounter
        self.myData['data'] = []
        for i in range(0, len(self.value)):
            self.value[i] = self.value[i] - self.lookup[random.randint(0, len(self.lookup)-1)]
            if self.value[i] < 0:
                self.value[i] = 0
            self.myData['data'].append(self.valStruct(self.value[i], id=i, type='level', unit="%", description='Supply Fill Level'))
        # Random Value for Tempertatur, Humudity and power
        self.myData['data'].append(self.valStruct(random.randint(10, 45), type='env_temperatur', description='Environment Temp'))
        self.myData['data'].append(self.valStruct(random.randint(-5, 15), type='op_temperatur', description='Operational Temp'))
        self.myData['data'].append(self.valStruct(random.randint(0, 100), type='humidity', unit="%", description='Environment Humidity'))
        self.myData['data'].append(self.valStruct(random.randint(300, 1500), type='power', unit="W", description='Power Consumption'))
        return json.dumps(self.myData)

    def sumFill(self):
        return sum(self.value)

    def refill(self):
        for i in range(0,len(self.value)):
            self.value[i] = 100
        return

    def celan(self):
        self.cleancounter = 0
        return

    def reset(self):
        self.cleancounter = 0
        self.refill(self)

    #
    # With a little helper from my friends to write values in the json struct
    #
    def valStruct(self, val, id=0, type="temperatur", unit="C", description=""):
        return {"id": id, "value": val, "type": type, "unit":unit, "description":description}

#
# Main Code
#


