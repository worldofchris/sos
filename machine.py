# Dummy library to stand in for the micropython machine lib so we can test calls to it

class Pin:

    def __init__(self, pin):
        pass

class PWM:

    def __init__(self, pin):
        pass

    def init(self, freq, duty):
        pass

    def deinit(self):
        pass
