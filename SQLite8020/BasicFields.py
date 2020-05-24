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
        ''' Check to see if a string represents a canonical SQLite type. '''
        return zType.upper() in ("INTEGER", "REAL", "TEXT", "BLOB")

    @staticmethod
    def MkGoodName(zName):
        ''' Concoct a database token. Return database token that is PROBABLY
        okay. (i.e. Presently covering the 80:20 basics of what most geeks 
        need do.) '''
        for ch in BasicFields.BADIES:
            zName = zName.replace(ch, '_')
        return zName

    @staticmethod
    def IsGoodName(zName):
        ''' Check to see if a database token might work out okay.
        Return True is PROBABLY okay, else false.
        (One could do a lot more (check for SQL keywords, etc.)
        Mission is to support 80:20 of what most geeks need do.) 
        '''
        for ch in BasicFields.BADIES:
            if zName.find(ch) != -1:
                return False
        return True

    def add(self, zName, zType):
        ''' Check the type, and add the name + tag definition to the 
        row set if supported. Returns True on success, else False on error. '''
        if not BasicFields.IsGoodName(zType):
            return False
        if not BasicFields.IsType(zType):
            return False
        self.fields[zName] = zType
        return True

    def get_od(self):
        ''' Return an ordered dictionary for the defined column-set. Key is name, value is
        the canonical SQLite type. '''
        return self.fields



