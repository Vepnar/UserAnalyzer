class cooldown:
    def __init__(self,uid,time):
        self.id = uid
        self.time = time
        self.remove =False
    def tick(self):
        self.time-=1
        if 1> self.time:
            self.remove=True
    def check(self,uid):
        if self.id == uid:
            return True
        return False
    def remain(self):
        return self.time
def initclasses():
    pass