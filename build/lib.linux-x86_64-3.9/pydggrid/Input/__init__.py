from abc import ABC

from pydggrid.Input._Auto import Input as AutoInput
from pydggrid.Input._Array import Input as ArrayInput
from pydggrid.Input._Sequence import Input as SequenceInput
from pydggrid.Input._Location import Input as LocationInput
from pydggrid.Input._Coordinate import Input as CoordinateInput
from pydggrid.Input._ShapeFIle import Input as ShapeFileInput
from pydggrid.Input._GeoJSON import Input as GeoJSONInput
from pydggrid.Input._GDAL import Input as GDALInput
from pydggrid.Input._AIGen import Input as AIGenInput
from pydggrid.Input._Cells import Input as CellTemplate
from pydggrid.Input._Template import Template as InputTemplate


class Auto(AutoInput):
    pass


class Array(ArrayInput):
    pass


class Sequence(SequenceInput):
    pass


class Location(LocationInput):
    pass


class Coordinate(CoordinateInput):
    pass


class ShapeFile(ShapeFileInput):
    pass


class GeoJSON(GeoJSONInput):
    pass


class GDAL(GDALInput):
    pass


class AIGen(AIGenInput):
    pass


class Template(InputTemplate, ABC):
    pass


class Cells(CellTemplate):
    pass
