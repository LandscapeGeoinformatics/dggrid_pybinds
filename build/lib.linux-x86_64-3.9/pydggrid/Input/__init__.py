from abc import ABC

from pydggrid.Input._Auto import Input as AutoTemplate
from pydggrid.Input._PointList import Input as PointListTemplate
from pydggrid.Input._ArrayList import Input as ArrayListTemplate
from pydggrid.Input._Template import Template as InputTemplate
from pydggrid.Input._Geometry import Input as GeometryInput


class Auto(AutoTemplate):
    pass


class PointList(PointListTemplate):
    pass


class Geometry(GeometryInput):
    pass


class ArrayList(ArrayListTemplate):
    pass


class Template(InputTemplate, ABC):
    pass
