class JSONType(object):
    types = {}

    def __init__(self, description):
        self.description = description
        JSONType.types[description] = self

    def __eq__(self, other):
        return self.description == other.description

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.description

    @classmethod
    def parse(cls, s):
        return cls.types[s]


class JSONTypes(object):

    INT = JSONType("int")
    FLOAT = JSONType("float")
    STRING = JSONType("str")
    CHAR = JSONType("char")
    BOOL = JSONType("bool")

    @classmethod
    def parse(cls, s):
        return JSONType.parse(s)


class JSONContainer(JSONType):
    def __init__(self, subtype):
        self.subtype = subtype
        self.degree = (
            1 + (subtype.degree if isinstance(subtype, JSONContainer) else 0)
        )
        self.root_type = (
            subtype.root_type if isinstance(subtype, JSONContainer) else subtype
        )
        super(JSONContainer, self).__init__('list_' + subtype.description)
