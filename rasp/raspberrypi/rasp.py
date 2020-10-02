class Rasp():
    def __init__(self):
        self.opened = True

    def get_state(self):
        pass

    def set_state(self, opened):
        pass


class VirtualRasp(Rasp):
    def get_state(self):
        return self.opened

    def set_state(self, opened):
        self.opened = opened
