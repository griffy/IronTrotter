from stats import Stats

class Update:
    def __init__(self, idnum, enttype, stat, name = ""):
        self.idnum = idnum
        self.enttype = enttype
        self.stat = stat

        self.name = name

