class Cache:
    def __init__(self, maximum=2000000):
        self.__store = {}
        self.__max = maximum

    def set(self, key, val):
        if key in val:
            return

        if len(self.__store) < self.__max:
            self.__store[key] = val
        else:
            self.__store.pop(list(self.__store.keys())[0]) # .keys() are the same as insertion order since Python 3.7+
            self.__store[key] = val

    def keyIn(self, key):
        return key in self.__store

    def get(self, key):
        return self.__store[key]