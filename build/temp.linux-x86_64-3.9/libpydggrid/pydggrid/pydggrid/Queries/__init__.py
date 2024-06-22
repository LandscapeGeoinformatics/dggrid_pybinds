from pydggrid.Queries._Custom import Query as CustomQuery
from pydggrid.Queries._Generate import Query as GenerateQuery
from pydggrid.Queries._PointPresence import Query as PointPresenceQuery
from pydggrid.Queries._PointValue import Query as PointValueQuery


class Generate(GenerateQuery):
    pass


class PointPresence(PointPresenceQuery):
    pass


class PointValue(PointValueQuery):
    pass


class Custom(CustomQuery):
    pass
