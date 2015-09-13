class SimpleStorage(object):
    def __init__(self):
        self.__records__ = []

    def store(self, record):
        self.__records__.append(record)

    def retrieve(self, record_id):
        if record_id < len(self.__records__):
            return self.__records__[record_id]
        raise IndexError("Record %s not in storage engine" % repr(record_id))

    def iteritems(self):
        for record in self.__records__:
            yield record

    def size(self):
        return len(self.__records__)
