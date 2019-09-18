class Quote(object):
    def __init__(self, open, high, low, close, volume=-1):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
