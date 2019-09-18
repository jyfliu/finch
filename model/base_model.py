# eventually switch to some sort of database
class BaseModel(object):

    def __init__(self):
        self.fields = {}

    def __getattr__(self, name):
        if name in self.fields:
            return self.fields[name]
        raise AttributeError

    def set(self, **kwargs):
        self.fields.update(kwargs)

    def save():
        pass
