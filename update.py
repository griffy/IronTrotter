from stats import Stats

class Update:
    def __init__(self, idnum, enttype, stats, name = ""):
        self.idnum = idnum
        self.enttype = enttype
        self.stats = stats

        self.name = name

nullUpdate = Update(0, 0, Stats(0,0,0))
