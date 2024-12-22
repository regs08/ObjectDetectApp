from abc import ABC

class NamedEntity(ABC):

    def __init__(self):
        self.name = None

    def initialize(self, **args):
        raise NotImplementedError ("Must Implement initialize!")