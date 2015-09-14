from __future__ import absolute_import
import pass3.record
import pass3.storage

class Engine(object):
    def __init__(self, password, storage=None):
        super(Engine, self).__init__()
        self.__passphrase__ = password
        if storage is None:
            storage = pass3.storage.MemoryStorage()
        self.__storage__ = storage

    def store(self, record):
        if not issubclass(record.__class__, pass3.record.Record):
            raise TypeError("Object %s is not a subclass of Record" % repr(record))
        self.__storage__.store(record, passphrase=self.__passphrase__)

    def search(self, scheme=None, host=None, path=None, title=None):
        for record in self.__storage__.iteritems(passphrase=self.__passphrase__):
            if record.match(scheme, host, path, title):
                yield record
