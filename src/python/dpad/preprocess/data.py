from doufo import dataclass,List


class Carriage_data:
    def __init__(self,energy,time,channel,module):
        self.energy = energy
        self.time = time
        self.channel = channel
        self.module = module


class Train_data:
    def __init__(self,headstock,data:List(Carriage_data),carriage_tail,carriage_tail):
        self.headstock = headstock
        self.data = data
        self.carriagetail = Carriage_data
        self.tail = tail

    @property
    def train_id(self):
        return headstock

    @property
    def 



