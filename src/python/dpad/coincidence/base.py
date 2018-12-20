from ..correction.actual2theroy import Single

class Coincidence:
    def __init__(self,time,energy,events:Single):
        self.time = time
        self.energy = energy
        self.events = events

    