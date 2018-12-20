


class Single:
    def __init__(self,time,energy,blockid,crystalid):
        self.time = time
        self.energy = energy
        self.blockid = blockid
        self.crystalid = crystalid

    def update_blockid(new_blockid):
        return Single_event(self.time,self.energy,new_blockid,self.crystalid)

    def update_crystalid(new_crystalid):
        return Single_event(self.time,self.energy,self.blockid,new_crystalid)


def smooth_event_time(event:Single)->Single:
    pass