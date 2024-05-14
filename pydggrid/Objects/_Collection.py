import json
import os.path
import sys
import tempfile
from io import StringIO
from typing import List, Any, Dict, Tuple

import fiona
import geojson
import geopandas
import numpy
import pandas
from shapely.geometry import Polygon, Point, GeometryCollection, LineString
from shapely.geometry import shape, mapping

from pydggrid.Types import ReadMode

fiona.drvsupport.supported_drivers['kml'] = 'rw'  # enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['KML'] = 'rw'  # enable KML support which is disabled by default

fiona.supported_drivers['KML'] = "rw"

# Enable fiona driver
geopandas.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)


class Object:

    def __init__(self):
        self._text: str = ""
        self._data: Any = list([])
        self._cols: List[str] = list(["id", "lat", "long"])
        self._type: [ReadMode, None] = None
        self._crs: str = "epsg:4326"
        self._content: Dict[str, str] = dict({})
        pass

    def save(self, data: bytes, read_mode: ReadMode) -> None:
        """
        Saves data into byte array
        :param data: Data Bytes
        :param read_mode: Data Interpreter
        :return: None
        """
        if read_mode == ReadMode.AIGEN:
            self._text = bytes(data).decode()
            string_blocks: List[str] = self._text.split("END")
            records: List[Dict[str, Any]] = list([])
            record_set: List[List[Dict[str, Any]]] = list([])
            [record_set.append(self._aigen_extract(n)) for n in string_blocks]
            [[records.append(n) for n in d] for d in record_set]
            frame: pandas.DataFrame = pandas.DataFrame(records)
            unique_sets: List[int] = list(frame["id"].unique())
            geometry_elements: List[Polygon, Point] = list([])
            for unique_set in unique_sets:
                coordinate_frame = frame[frame["id"] == unique_set]
                if coordinate_frame.shape[0] > 2:
                    geometry_elements.append(Polygon(zip(
                        list(coordinate_frame["lat"]),
                        list(coordinate_frame["long"]))))
                else:
                    geometry_elements.append(Point(
                        list(coordinate_frame["lat"])[0],
                        list(coordinate_frame["long"])[0]))
            self._data = geopandas.GeoDataFrame({"id": unique_sets, "geometry": geometry_elements})
            self._type = geopandas.GeoDataFrame
            self._content["kml"] = self._get_kml()
            # TODO: KML 
        elif read_mode == ReadMode.KML:
            self._text = bytes(data).decode()
            self._type = geopandas.GeoDataFrame
            payload: StringIO = StringIO(self._text)
            self._data = geopandas.read_file(payload, driver="KML")
            self._data = self._data.rename(columns={"Name": "id"})
            self._content["kml"] = self._get_kml()
        elif read_mode == ReadMode.GEOJSON or \
                read_mode == ReadMode.GDAL_COLLECTION:
            self._type = geopandas.GeoDataFrame
            self._text = bytes(data).decode().replace("\n", "").replace("},]", "}]")
            if len(self._text) > 0:
                self._data = geopandas.GeoDataFrame.from_features(geojson.loads(self._text))
                self._data = self._data.rename(columns={"name": "id"})
            else:
                self._data = geopandas.GeoDataFrame()
        elif read_mode == ReadMode.SHAPEFILE:
            shape_file: str = ""
            ext_array: List[str] = ["shp", "dbf", "prj", "sbn", "sbx", "shx"]
            # noinspection PyUnresolvedReferences,PyProtectedMember
            temp_file = os.path.join(tempfile.gettempdir(), f"{next(tempfile._get_candidate_names())}")
            for extension in ext_array:
                extension = "".join([chr(c) for c in data[0:3]])
                file_name: str = f"{temp_file}.{extension}"
                shape_file = file_name if extension == "shp" else shape_file
                data = data[3:]
                #
                byte_size: int = int.from_bytes(bytearray(data[:4]), "little")
                data = data[4:]
                #
                file = open(file_name, "wb")
                file.write(bytearray(data[:byte_size]))
                file.close()
                print(file_name)
                data = data[byte_size:]
            self._type = geopandas.GeoDataFrame
            self._data = geopandas.GeoDataFrame.from_file(shape_file)
            self._data = self._data.rename(columns={"global_id": "id"})
            self._text = str(self._data)
        elif read_mode == ReadMode.NONE:
            return
        else:
            print(read_mode)
            sys.exit(0)

    def __str__(self) -> str:
        """
        Outputs Collection Info
        :return: Collection info as string
        """
        if self._type == pandas.DataFrame:
            return str(self._data)
        if self._type == geopandas.GeoDataFrame:
            return str(pandas.DataFrame(self._data))
        return "UNKNOWN"

    def get_columns(self) -> List[str]:
        """
        Returns a list of columns for the collection
        :return: Columns List in order of datas
        """
        return self._cols

    def get_text(self) -> str:
        """
        Returns response data as raw text
        :return: Response Text
        """
        return self._text

    def get_frame(self) -> [pandas.DataFrame, None]:
        """
        Returns the record as a data frame
        :return: Pandas DataFrame or None if not available
        """
        if self._type is None:
            return pandas.DataFrame()
        elif self._type == pandas.DataFrame:
            return self._data
        elif self._type == geopandas.GeoDataFrame:
            elements: List[Dict[str, Any]] = list([])
            frame: pandas.DataFrame({"id": [], "lat": [], "long": []})
            for data_node in self._data.itertuples():
                points: List[Tuple[float, float]] = self._list_points(data_node.geometry)
                index_id = data_node.id if hasattr(data_node, "id") else data_node.Name
                [elements.append({
                    self._cols[0]: str(index_id),
                    self._cols[1]: n[0],
                    self._cols[2]: n[1]
                }) for n in points]
            return pandas.DataFrame(elements)
        else:
            raise NotImplementedError(f"This collection cannot be exported as a DataFrame [ {self._type} ]")

    def get_geoframe(self) -> geopandas.GeoDataFrame:
        """
        Returns the record as a geo data frame
        :return: Geo Pandas Data Frame
        """
        if self._type is None:
            return geopandas.GeoDataFrame()
        elif self._type == pandas.DataFrame:
            return geopandas.GeoDataFrame(self._data)
        elif self._type == geopandas.GeoDataFrame:
            return self._data
        else:
            raise NotImplementedError("This collection cannot be exported as a GeoDataFrame")

    def get_xml(self) -> str:
        """
        Returns the XML string of the content
        :return: XML String
        """
        if self._type == pandas.DataFrame:
            return self._data.to_xml()
        elif self._type == geopandas.GeoDataFrame:
            return self._content["kml"]
        else:
            raise NotImplementedError("This collection cannot be exported as XML")

    def get_numpy(self) -> numpy.ndarray:
        """
        Returns the record as a numpy ndarray
        :return: Numpy ND Array
        """
        if self._type is None:
            return numpy.array([])
        if self._type == pandas.DataFrame:
            return self._data.to_numpy()
        elif self._type == geopandas.GeoDataFrame:
            return self.get_frame().to_numpy()
        else:
            raise NotImplementedError("This collection cannot be exported as Numpy NDArray")

    def un_static(self) -> None:
        """
        Un Statics a method
        :return: None
        """
        pass

    # INTERNAL

    def _aigen_extract(self, string_block: str) -> List[Dict[str, Any]]:
        """
        Extract records from a single aigen block
        :param string_block: String block data
        :return: Extracted Records
        """
        self.un_static()
        block_id: int = 0
        coordinates: List[str] = list(["", ""])
        records: List[Dict[str, Any]] = list([])
        element_blocks: List[str] = string_block.split("\n")
        for element_block in element_blocks:
            elements: List[str] = element_block.split(" ")
            if len(elements) < 2:
                continue
            if len(elements) == 3:
                block_id = int(elements[0].strip())
                coordinates[0] = elements[1]
                coordinates[1] = elements[2]
            if len(elements) == 2:
                coordinates[0] = elements[0]
                coordinates[1] = elements[1]
            records.append({
                "id": block_id,
                "lat": float(coordinates[0]),
                "long": float(coordinates[1])
            })
        return records

    def _list_points(self,
                     geometry: [Polygon, Point, GeometryCollection],
                     point_list: [List[Tuple[float, float]], None] = None) -> List[Tuple[float, float]]:
        """
        Lists all points in a geometry
        :param geometry: Geometry Object
        :param point_list: Point List Object
        :return: Points List as [(x, y),...]
        """
        self.un_static()
        point_list = list([]) if point_list is None else point_list
        if isinstance(geometry, GeometryCollection):
            for index in list(range(0, len(mapping(geometry)['geometries'][0]))):
                self._list_points(shape(mapping(geometry)['geometries'][index]), point_list)
        elif isinstance(geometry, Point):
            x, y = geometry.coords.xy
            point_list.append(list(zip(x, y)))
        elif isinstance(geometry, Polygon):
            x, y = geometry.exterior.coords.xy
            point_list.append(list(zip(x, y)))
        elif isinstance(geometry, LineString):
            x, y = geometry.coords.xy
            point_list.append(list(zip(x, y)))
        else:
            raise NotImplementedError(f"Geometry type not implemented {type(geometry)}")
        return [point for point_set in point_list for point in point_set]

    def _get_kml(self):
        # dump text
        with tempfile.TemporaryDirectory() as tmp:
            # noinspection PyUnresolvedReferences,PyProtectedMember
            path: str = os.path.join(tmp, next(tempfile._get_candidate_names()))
            geopandas.GeoDataFrame(self._data).to_file(path, driver="KML")
            file = open(path, "rt")
            kml_string = file.read()
            file.close()
            os.remove(path)
            return kml_string

