import re

class Set:
    def __init__(self):
        self._set = set()

    def add(self, item):
        if item is not None:
            self._set.add(item)
    
    def pop(self):
        if self.len():
            return self._set.pop()
        else:
            raise SetEmptyExp

    def len(self):
        return len(self._set)

    def __len__(self):
        return self.len()

    def __repr__(self):
        return self._set.__repr__()

    def __str__(self):
        return self.__repr__()

    def __contains__(self, obj):
        return obj in self._set

class SetEmptyExp(Exception):
    pass