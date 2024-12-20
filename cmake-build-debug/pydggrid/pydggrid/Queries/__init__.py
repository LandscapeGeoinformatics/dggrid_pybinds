from pydggrid.Queries._Custom import Query as CustomQuery
from pydggrid.Queries._Generate import Query as GenerateQuery
from pydggrid.Queries._PointPresence import Query as PointPresenceQuery
from pydggrid.Queries._PointValue import Query as PointValueQuery
from pydggrid.Queries._PointGen import Query as PointGenQuery
from pydggrid.Queries._Statistics import Query as StatisticsQuery
from pydggrid.Queries._Transform import Query as TransformQuery


class Generate(GenerateQuery):
    pass


class PointPresence(PointPresenceQuery):
    pass


class PointValue(PointValueQuery):
    pass


class PointGen(PointGenQuery):
    pass


class Statistics(StatisticsQuery):
    pass
    pass


class Transform(TransformQuery):
    pass


class Custom(CustomQuery):
    pass
