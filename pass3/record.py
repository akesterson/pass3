class Record(object):
    def __init__(self, scheme, host, path, user=None, password=None, title=None):
        self.scheme = scheme
        self.host = host
        self.path = path
        self.user = user
        self.password = password
        self.title = title
        self.alternates = []

    def to_dict(self):
        ret = {}
        for key in ['scheme', 'host', 'path', 'user', 'password', 'title']:
            ret[key] = getattr(self, key)
        ret['alternates'] = [x.to_dict() for x in self.alternates]
        return ret
    
    @staticmethod
    def from_dict(obj):
        ret = Record(
            obj['scheme'],
            obj['host'],
            obj['path'],
            obj['user'],
            obj['password'],
            obj['title']
            )
        ret.alternates = [Record.from_dict(x) for x in obj['alternates']]
        return ret
        
    def match(self, scheme=None, host=None, path=None, title=None):
        """
        Return True if this record (or any of its alternates) match the parameters
        """
        for alternate in self.alternates:
            if alternate.match(scheme, host, path, title):
                return True
        if title and title.lower() in title.lower():
            return True

        if (scheme is not None) and scheme.lower() != scheme.lower():
            return False
        if (host is not None) and host.lower() != host.lower():
            return False
        if (path is not None) and path.lower() != path.lower():
            return False

        return True
    
    def add_alternate(self, record):
        if not issubclass(record.__class__, Record):
            raise TypeError("Object %s is not a subclass of Record" % repr(record))
        self.alternates.append(record)
        
    def __repr__(self):
        return "<%s object at %s> (%s : %s @ %s://%s/%s)" % (
            self.__class__.__name__,
            id(self),
            self.title,
            self.user,
            self.scheme,
            self.host,
            self.path
        )
