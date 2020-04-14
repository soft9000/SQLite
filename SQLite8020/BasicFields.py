from collections import OrderedDict

class BasicFields(object):

    """
    Name implies that we are interested in basic, SQLite, data types?
    The ID field should always be present. Integral. Constraint is AUTO.
    Foreign-key relationships - if required - must be user-managed.
    User-defined field constraints, are not supported.
    """

    BADIES = ' ', '\n', '\r', '\t'

    def __init__(self):
        self.fields = OrderedDict()
        self.fields["ID"] = "Integer"

    @staticmethod
    def IsType(zType):
        return zType.upper() in ("INTEGER", "REAL", "TEXT", "BLOB")

    @staticmethod
    def MkGoodName(zName):
        ''' We could do a lot more here, covering the basics... '''
        for ch in BasicFields.BADIES:
            zName = zName.replace(ch, '_')
        return zName

    @staticmethod
    def IsGoodName(zName):
        ''' We could do a lot more here, covering the basics... '''
        for ch in BasicFields.BADIES:
            if zName.find(ch) != -1:
                return False
        return True

    def add(self, zName, zType):
        if not BasicFields.IsGoodName(zType):
            return False
        if not BasicFields.IsType(zType):
            return False
        self.fields[zName] = zType
        return True

    def get_od(self):
        return self.fields


