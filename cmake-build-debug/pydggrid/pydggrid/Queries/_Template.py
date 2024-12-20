import datetime
import os
import pathlib
import sys
import textwrap
import time
from abc import ABC, abstractmethod
from typing import List, Any, Dict, TextIO

import libpydggrid

from pydggrid.System import Constants

from pydggrid.Input import Template as InputTemplate, Auto
from pydggrid.Objects import Attributes, Options, Option
from pydggrid.Types import Operation, ClipType, ClipMethod, DGGSType, DGGSPoly, Topology, DGGSProjection, Aperture, \
    ProjectionDatum, OrientationType, ResolutionType, AddressField, PointDataType, InputAddress, BinCoverage, \
    OutputControl, OutputType, OutputAddress, LongitudeWrap, CellLabel, CellOutput, PointOutput, RandPointOutput, \
    NeighborOutput, ChildrenOutput, GDALFormat


class Template(ABC):
    """
    Query Base Object
    _op: Operation Type
    Attributes: Attributes Object
    """

    def __init__(self,
                 operation: Operation = Operation.CUSTOM,
                 input_object: [Any, None] = None):
        """
        Default constructor
        :param operation: Operation Type
        """
        self._op: Operation = Operation(operation)
        self._time: int = int(time.time() * 1000)
        self.Input: InputTemplate = input_object if isinstance(input_object, InputTemplate) else Auto()
        self.Meta: Attributes = Attributes()
        self._load_defaults(self._op)
        #
        self.Meta.save("dggrid_operation", self._op)

    def type(self, operation: [Operation, None] = None) -> Operation:
        """
        Optionally sets then Returns the operation type
        :return: Operation type
        """
        if operation is not None:
            self._op = operation
            self.Meta.save("dggrid_operation", self._op)
        return self._op

    def time(self) -> int:
        """
        Returns epoch time stamp of the query
        :return: Epoch time stamp as integer
        """
        return self._time

    @abstractmethod
    # noinspection PyPep8Naming
    def UnitTest_ReadPayload(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytes = self.Input.__bytes__()
        return libpydggrid.UnitTest_ReadPayload(dictionary, payload)

    @abstractmethod
    # noinspection PyPep8Naming
    def UnitTest_ReadQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytes = self.Input.__bytes__()
        return libpydggrid.UnitTest_ReadQuery(dictionary, payload)

    @abstractmethod
    # noinspection PyPep8Naming
    def UnitTest_RunQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytes = self.Input.__bytes__()
        return libpydggrid.UnitTest_RunQuery(dictionary, payload)

    @abstractmethod
    def run(self) -> None:
        """
        Runs the query
        :return: None
        """
        raise NotImplementedError("run() must be implemented for individual query types.")

    @abstractmethod
    def __str__(self) -> str:
        """
        Describes the query
        :return: Query Description
        """
        string_array: List[str] = list()
        byte_array: bytes = self.__bytes__()
        string_array.append(f"Type: {self.type().name}")
        string_array.append(f"Time Stamp: {datetime.datetime.fromtimestamp(self.time() / 1000.0)}")
        string_array.append(f"Parameters:")
        string_array.append("\t" + f"{os.linesep}\t".join(self.Meta.__str__().split(os.linesep)))
        string_array.append(f"Binary Data [{len(byte_array)} bytes]:")
        string_array.append("\t" + f"{os.linesep}\t".join(textwrap.wrap(byte_array.hex(), 64)))
        return os.linesep.join(string_array)

    @abstractmethod
    def __bytes__(self) -> bytes:
        """
        Returns the query data as a byte array
        :return: Byte Array base data
        """
        return self.Input.__bytes__()

    def print(self) -> None:
        """
        Prints the query data
        :return: None
        """
        print(self)

    def exec(self, byte_data: [bytes, None] = None) -> Dict[str, bytes]:
        """
        Executes the query and returns a bytes array
        :param byte_data byte payload, if left blank Input.__bytes__() will be used
        :return: DGGRID Response Bytes array
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytes = self.Input.__bytes__() if byte_data is None else byte_data
        return libpydggrid.RunQuery(dictionary, list(payload))

    def io(self, name: str, data: [Any, None]) -> Any:
        """
        Set / Get encoder
        :param name: Parameter Name
        :param data: Parameter data, if set to none it will be ignored
        :return: Any attribute requested
        """
        if data is not None:
            self.Meta.save(name, data)
        return self.Meta.get(name)

    def load(self, meta: [str, pathlib.Path]) -> None:
        """
        Loads a meta-data file
        :param meta: Meta Data source can be
            - String containing meta-data info
            - Path string to a file contiaing a meta-data file
            - pathlib.Path object containing a meta-data file
        :return: None
        """
        parameters: Dict[str, str]
        if isinstance(meta, pathlib.Path):
            with open(meta.absolute()) as file:
                parameters = self._meta_dict(file)
        elif isinstance(meta, str) and "\n" in meta:
            parameters = self._meta_dict(meta.split("\n"))
        else:
            if os.path.isfile(meta):
                with open(meta) as file:
                    parameters = self._meta_dict(file)
            else:
                raise Exception("unrecognized parameter type")
        for parameter in parameters:
            self.Meta.save_str(parameter, parameters[parameter])

    def set_precision(self, precision: int) -> None:
        """
        Sets the precision factor of the query
        :param precision: Precision Factor, Defaults to Constants.DEFAULT_PRECISION
        :return: None
        """
        self.Meta.save("precision", precision)

    def precision(self) -> int:
        """
        Returns the precision value from the meta data
        :return: Integer representing the precision factor
        """
        return self.Meta.as_int("precision")

    def set_dggs(self, dggs_type: [DGGSType, int]) -> None:
        """
        Sets the meta DGGS type
        :param dggs_type: DGGS Type
        :return: None
        """
        self.Meta.save("dggs_type", DGGSType(dggs_type))

    def dggs_type(self) -> DGGSType:
        """
        Returns the DGGS type
        :return: DGGS Type Enumeration
        """
        return DGGSType(self.Meta.as_int("dggs_type"))

    def set_resolution(self, resolution: int) -> None:
        """
        Sets the DGGS Resolution
        :param resolution: DGGS Resolution value
        :return: None
        """
        self.Meta.save("dggs_res_spec", resolution)

    def resolution(self) -> int:
        """
        Returns the DGGS Resolution value
        :return: DGGS Resolution value
        """
        if __name__ == '__main__':
            return self.Meta.as_int("dggs_res_spec")

    # INTERNAL

    def _meta_dict(self, lines: [List[str], TextIO]) -> Dict[str, str]:
        """
        converts string parameters to a dictionary of parameters
        :param lines: Parameter string lines can be
            - TextIO object created with open()
            - String of meta data
        :return: Dictionary of parameters as [str, str]
        """
        self._un_static()
        parameters: Dict[str, str] = dict({})
        lines: List[str] = [line.strip() for line in lines
                            if not line.strip().startswith("#") and line.strip() != ""]
        for line in lines:
            name, value = tuple(line.split(" "))
            parameters[name] = value
        return parameters

    def _un_static(self) -> None:
        """
        Does nothing
        :return:
        """
        pass

    def _load_defaults(self, operation: [Operation, int]) -> None:
        """
        Loads all default attributes
        :param operation Operation identifier
        :return: None
        """
        # dggrid_operation
        self.Meta.define(name="dggrid_operation",
                         data_type=Options,
                         data_options=Options(Operation),
                         data_default=operation,
                         on_verify=None)
        # precision
        self.Meta.define(name="precision",
                         data_type=int,
                         data_options=None,
                         data_default=Constants.DEFAULT_PRECISION,
                         on_verify=lambda value: Constants.MAXIMUM_INT > int(value) > 0)
        # verbosity
        self.Meta.define(name="verbosity",
                         data_type=int,
                         data_options=None,
                         data_default=0,
                         on_verify=lambda value: Constants.MAXIMUM_VERBOSITY > int(value) > -1)
        # pause_on_startup
        self.Meta.define(name="pause_on_startup",
                         data_type=bool,
                         data_options=None,
                         data_default=False,
                         on_verify=None)
        # pause_before_exit
        self.Meta.define(name="pause_before_exit",
                         data_type=bool,
                         data_options=None,
                         data_default=False,
                         on_verify=None)
        # update_frequency
        self.Meta.define(name="update_frequency",
                         data_type=int,
                         data_options=None,
                         data_default=100000,
                         on_verify=lambda value: sys.maxsize > int(value) > 5)
        # geodetic_densify
        self.Meta.define(name="geodetic_densify",
                         data_type=float,
                         data_options=None,
                         data_default=float(0.0),
                         on_verify=lambda value: 0 <= float(value) <=
                                                 Constants.MAXIMUM_GEO_DENSIFY)
        # clip_subset_type
        self.Meta.define(name="clip_subset_type",
                         data_type=Options,
                         data_options=Options(ClipType),
                         data_default=ClipType.WHOLE_EARTH,
                         on_verify=None)
        # clip_subset_type
        self.Meta.define(name="clip_cell_addresses",
                         data_type=str,
                         data_options=None,
                         data_default="",
                         on_verify=None)
        # clip_cell_densification
        self.Meta.define(name="clip_cell_densification",
                         data_type=int,
                         data_options=None,
                         data_default=1,
                         on_verify=lambda value: Constants.MAXIMUM_DENSIFICATION > int(value) > -1)
        # clip_type
        self.Meta.define(name="clip_type",
                         data_type=Options,
                         data_options=Options(ClipMethod),
                         data_default=ClipMethod.POLY_INTERSECT,
                         on_verify=None)
        # clipper_scale_factor
        self.Meta.define(name="clipper_scale_factor",
                         data_type=int,
                         data_options=None,
                         data_default=1000000,
                         on_verify=lambda value: int(value) > 0)
        # clip_using_holes
        self.Meta.define(name="clip_using_holes",
                         data_type=bool,
                         data_options=None,
                         data_default=False,
                         on_verify=None)
        # clip_region_files
        self.Meta.define(name="clip_region_files",
                         data_type=str,
                         data_options=None,
                         data_default="test.gen",
                         on_verify=None)
        # clip_cell_res
        self.Meta.define(name="clip_cell_res",
                         data_type=int,
                         data_options=None,
                         data_default=1,
                         on_verify=lambda value: 0 < int(value) <= Constants.MAX_DGG_RES)
        # dggs_type
        self.Meta.define(name="dggs_type",
                         data_type=Options,
                         data_options=Options(DGGSType),
                         data_default=DGGSType.CUSTOM,
                         on_verify=None)
        # dggs_base_poly
        self.Meta.define(name="dggs_base_poly",
                         data_type=Options,
                         data_options=Options(DGGSPoly),
                         data_default=DGGSPoly.ICOSAHEDRON,
                         on_verify=None)
        # dggs_topology
        self.Meta.define(name="dggs_topology",
                         data_type=Options,
                         data_options=Options(Topology),
                         data_default=Topology.HEXAGON,
                         on_verify=None)
        # dggs_proj
        self.Meta.define(name="dggs_proj",
                         data_type=Options,
                         data_options=Options(DGGSProjection),
                         data_default=DGGSProjection.ISEA,
                         on_verify=None)
        # dggs_aperture_type
        self.Meta.define(name="dggs_aperture_type",
                         data_type=Options,
                         data_options=Options(Aperture),
                         data_default=Aperture.PURE,
                         on_verify=None)
        # dggs_aperture
        self.Meta.define(name="dggs_aperture",
                         data_type=Option,
                         data_options=Option(Constants.APERTURE_VALUES),
                         data_default=4,
                         on_verify=None)
        # dggs_aperture
        self.Meta.define(name="dggs_aperture_sequence",
                         data_type=int,
                         data_options=None,
                         data_default=333333333333,
                         on_verify=None)
        # dggs_num_aperture_4_res
        self.Meta.define(name="dggs_num_aperture_4_res",
                         data_type=int,
                         data_options=None,
                         data_default=0,
                         on_verify=lambda value: -1 < int(value) <= Constants.MAX_DGG_RES)
        # proj_datum
        self.Meta.define(name="proj_datum",
                         data_type=Options,
                         data_options=Options(ProjectionDatum),
                         data_default=ProjectionDatum.WGS84_AUTHALIC_SPHERE,
                         on_verify=None)
        # proj_datum_radius
        self.Meta.define(name="proj_datum_radius",
                         data_type=float,
                         data_options=None,
                         data_default=1.0,
                         on_verify=lambda value: 1.0 <= float(value) <= Constants.MAXIMUM_DATUM_RADIUS)
        # dggs_orient_specify_type
        self.Meta.define(name="dggs_orient_specify_type",
                         data_type=Options,
                         data_options=Options(OrientationType),
                         data_default=OrientationType.SPECIFIED,
                         on_verify=None)
        # dggs_num_placements
        self.Meta.define(name="dggs_num_placements",
                         data_type=int,
                         data_options=None,
                         data_default=0,
                         on_verify=lambda value: 1 < int(value) <= Constants.MAXIMUM_INT)
        # dggs_orient_rand_seed
        self.Meta.define(name="dggs_orient_rand_seed",
                         data_type=int,
                         data_options=None,
                         data_default=Constants.DEFAULT_RAND_SEED,
                         on_verify=lambda value: 1 < int(value) <= sys.maxsize)
        # dggs_vert0_lon
        self.Meta.define(name="dggs_vert0_lon",
                         data_type=float,
                         data_options=None,
                         data_default=Constants.VERT0_LONGITUDE_DEFAULT,
                         on_verify=lambda value: Constants.LONGITUDE_LIMITS[0] <= float(value) <=
                                                 Constants.LONGITUDE_LIMITS[1])
        # dggs_vert0_lat
        self.Meta.define(name="dggs_vert0_lat",
                         data_type=float,
                         data_options=None,
                         data_default=Constants.VERT0_LATITUDE_DEFAULT,
                         on_verify=lambda value: Constants.LATITUDE_LIMITS[0] <= float(value) <=
                                                 Constants.LATITUDE_LIMITS[1])
        # dggs_vert0_azimuth
        self.Meta.define(name="dggs_vert0_azimuth",
                         data_type=float,
                         data_options=None,
                         data_default=Constants.VERT0_AZIMUTH_DEFAULT,
                         on_verify=lambda value: Constants.AZIMUTH_LIMITS[0] <= float(value) <=
                                                 Constants.AZIMUTH_LIMITS[1])
        # region_center_lon
        self.Meta.define(name="region_center_lon",
                         data_type=float,
                         data_options=None,
                         data_default=Constants.CENTER_LONGITUDE_DEFAULT,
                         on_verify=lambda value: Constants.LONGITUDE_LIMITS[0] <= float(value) <=
                                                 Constants.LONGITUDE_LIMITS[1])
        # region_center_lat
        self.Meta.define(name="region_center_lat",
                         data_type=float,
                         data_options=None,
                         data_default=Constants.CENTER_LATITUDE_DEFAULT,
                         on_verify=lambda value: Constants.LATITUDE_LIMITS[0] <= float(value) <=
                                                 Constants.LATITUDE_LIMITS[1])
        # dggs_orient_specify_type
        self.Meta.define(name="dggs_res_specify_type",
                         data_type=Options,
                         data_options=Options(ResolutionType),
                         data_default=ResolutionType.SPECIFIED,
                         on_verify=None)
        # dggs_res_specify_area
        self.Meta.define(name="dggs_res_specify_area",
                         data_type=float,
                         data_options=None,
                         data_default=Constants.DEFAULT_RESOLUTION_AREA,
                         on_verify=lambda value: sys.float_info.epsilon <= float(value) <
                                                 Constants.MAXIMUM_RESOLUTION_AREA * 6500.00)
        # dggs_res_specify_intercell_distance
        self.Meta.define(name="dggs_res_specify_intercell_distance",
                         data_type=float,
                         data_options=None,
                         data_default=Constants.DEFAULT_INTERCELL_DISTANCE,
                         on_verify=lambda value: sys.float_info.epsilon <= float(value) <
                                                 Constants.MAXIMUM_INTERCELL_DISTANCE)
        # dggs_res_specify_rnd_down
        self.Meta.define(name="dggs_res_specify_rnd_down",
                         data_type=bool,
                         data_options=None,
                         data_default=True,
                         on_verify=None)
        # dggs_res_spec
        self.Meta.define(name="dggs_res_spec",
                         data_type=int,
                         data_options=None,
                         data_default=Constants.DEFAULT_DGG_RES,
                         on_verify=lambda value: 0 <= int(value) < Constants.MAX_DGG_RES)
        # input_files
        self.Meta.define(name="input_files",
                         data_type=str,
                         data_options=None,
                         data_default="vals.txt",
                         on_verify=None)
        # input_file_name
        self.Meta.define(name="input_file_name",
                         data_type=str,
                         data_options=None,
                         data_default="valsin.txt",
                         on_verify=None)
        # input_address_field_type
        self.Meta.define(name="input_address_field_type",
                         data_type=Options,
                         data_options=Options(AddressField),
                         data_default=AddressField.GEO_POINT,
                         on_verify=None)
        # input_address_field_type
        self.Meta.define(name="point_input_file_type",
                         data_type=Options,
                         data_options=Options(AddressField),
                         data_default=AddressField.GEO_POINT,
                         on_verify=None)
        # point_input_file_type
        self.Meta.define(name="point_input_file_type",
                         data_type=Options,
                         data_options=Options(PointDataType),
                         data_default=PointDataType.NONE,
                         on_verify=None)
        # input_address_type
        self.Meta.define(name="input_address_type",
                         data_type=Options,
                         data_options=Options(InputAddress),
                         data_default=InputAddress.GEO,
                         on_verify=None)
        # input_delimiter
        self.Meta.define(name="input_delimiter",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_DELIMITER,
                         on_verify=None)
        # bin_coverage
        self.Meta.define(name="bin_coverage",
                         data_type=Options,
                         data_options=Options(BinCoverage),
                         data_default=BinCoverage.GLOBAL,
                         on_verify=None)
        # output_count
        self.Meta.define(name="output_count",
                         data_type=bool,
                         data_options=None,
                         data_default=False,
                         on_verify=None)
        # output_count_field_name
        self.Meta.define(name="output_count_field_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_COUNT_FIELD_NAME,
                         on_verify=lambda value: len(str(value)) > 0)
        # input_value_field_name
        self.Meta.define(name="input_value_field_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_VALUE_FIELD_NAME,
                         on_verify=lambda value: len(str(value)) > 0)
        # output_total
        self.Meta.define(name="output_total",
                         data_type=bool,
                         data_options=None,
                         data_default=False,
                         on_verify=None)
        # output_total_field_name
        self.Meta.define(name="output_total_field_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_TOTAL_FIELD_NAME,
                         on_verify=lambda value: len(str(value)) > 0)
        # output_total
        self.Meta.define(name="output_mean",
                         data_type=bool,
                         data_options=None,
                         data_default=False,
                         on_verify=None)
        # output_mean_field_name
        self.Meta.define(name="output_mean_field_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_MEAN_FIELD_NAME,
                         on_verify=lambda value: len(str(value)) > 0)
        # output_presence_vector
        self.Meta.define(name="output_presence_vector",
                         data_type=bool,
                         data_options=None,
                         data_default=False,
                         on_verify=None)
        # output_presence_vector_field_name
        self.Meta.define(name="output_presence_vector_field_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_PRESENCE_FIELD_NAME,
                         on_verify=lambda value: len(str(value)) > 0)
        # output_num_classes
        self.Meta.define(name="output_num_classes",
                         data_type=bool,
                         data_options=None,
                         data_default=False,
                         on_verify=None)
        # output_num_classes_field_name
        self.Meta.define(name="output_num_classes_field_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_N_CLASS_FIELD_NAME,
                         on_verify=lambda value: len(str(value)) > 0)
        # cell_output_control
        self.Meta.define(name="cell_output_control",
                         data_type=Options,
                         data_options=Options(OutputControl),
                         data_default=OutputControl.OUTPUT_ALL,
                         on_verify=None)
        # output_file_name
        self.Meta.define(name="output_file_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_OUTPUT_FILE_NAME,
                         on_verify=None)
        # output_file_type
        self.Meta.define(name="output_file_type",
                         data_type=Options,
                         data_options=Options(OutputType),
                         data_default=OutputType.NONE,
                         on_verify=None)
        # output_file_type
        self.Meta.define(name="output_file_type",
                         data_type=Options,
                         data_options=Options(OutputType),
                         data_default=OutputType.NONE,
                         on_verify=None)
        # output_address_type
        self.Meta.define(name="output_address_type",
                         data_type=Options,
                         data_options=Options(OutputAddress),
                         data_default=OutputAddress.SEQNUM,
                         on_verify=None)
        # output_delimiter
        self.Meta.define(name="output_delimiter",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_DELIMITER,
                         on_verify=None)
        # densification
        self.Meta.define(name="densification",
                         data_type=int,
                         data_options=None,
                         data_default=0,
                         on_verify=lambda value: 0 <= int(value) <= Constants.MAXIMUM_DENSIFICATION)
        # longitude_wrap_mode
        self.Meta.define(name="longitude_wrap_mode",
                         data_type=Options,
                         data_options=Options(LongitudeWrap),
                         data_default=LongitudeWrap.WRAP,
                         on_verify=None)
        # unwrap_points
        self.Meta.define(name="unwrap_points",
                         data_type=bool,
                         data_options=None,
                         data_default=False,
                         on_verify=None)
        # output_cell_label_type
        self.Meta.define(name="output_cell_label_type",
                         data_type=Options,
                         data_options=Options(CellLabel),
                         data_default=CellLabel.GLOBAL_SEQUENCE,
                         on_verify=None)
        # cell_output_type
        self.Meta.define(name="cell_output_type",
                         data_type=Options,
                         data_options=Options(CellOutput),
                         data_default=CellOutput.NONE,
                         on_verify=None)
        # point_output_type
        self.Meta.define(name="point_output_type",
                         data_type=Options,
                         data_options=Options(PointOutput),
                         data_default=CellOutput.NONE,
                         on_verify=None)
        # randpts_output_type
        self.Meta.define(name="randpts_output_type",
                         data_type=Options,
                         data_options=Options(RandPointOutput),
                         data_default=CellOutput.NONE,
                         on_verify=None)
        # cell_output_gdal_format
        self.Meta.define(name="cell_output_gdal_format",
                         data_type=Options,
                         data_options=Options(GDALFormat),
                         data_default=GDALFormat.GEOJSON,
                         on_verify=None)
        # point_output_gdal_format
        self.Meta.define(name="point_output_gdal_format",
                         data_type=Options,
                         data_options=Options(GDALFormat),
                         data_default=GDALFormat.GEOJSON,
                         on_verify=None)
        # collection_output_gdal_format
        self.Meta.define(name="collection_output_gdal_format",
                         data_type=Options,
                         data_options=Options(GDALFormat),
                         data_default=GDALFormat.GEOJSON,
                         on_verify=None)
        # cell_output_file_name
        self.Meta.define(name="cell_output_file_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_CELL_OUTPUT_FILE,
                         on_verify=None)
        # point_output_file_name
        self.Meta.define(name="point_output_file_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_POINTS_OUTPUT_FILE,
                         on_verify=None)
        # randpts_output_file_name
        self.Meta.define(name="randpts_output_file_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_RAND_POINTS_OUTPUT_FILE,
                         on_verify=None)
        # collection_output_file_name
        self.Meta.define(name="collection_output_file_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_COLLECTION_OUTPUT_FILE,
                         on_verify=None)
        # dggs_orient_output_file_name
        self.Meta.define(name="dggs_orient_output_file_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_DGGS_ORIENT_OUTPUT_FILE,
                         on_verify=None)
        # shapefile_id_field_length
        self.Meta.define(name="shapefile_id_field_length",
                         data_type=int,
                         data_options=None,
                         data_default=Constants.MAXIMUM_ID_FIELD_LEN,
                         on_verify=lambda value: 0 < int(value) < Constants.MAXIMUM_ID_FIELD_LEN)
        # kml_default_width
        self.Meta.define(name="kml_default_width",
                         data_type=int,
                         data_options=None,
                         data_default=Constants.MAXIMUM_ID_FIELD_LEN,
                         on_verify=lambda value: 0 < int(value) < Constants.MAXIMUM_KML_WIDTH)
        # kml_default_color
        self.Meta.define(name="kml_default_color",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_KML_COLOR,
                         on_verify=None)
        # kml_name
        self.Meta.define(name="kml_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_KML_NAME,
                         on_verify=None)
        # kml_description
        self.Meta.define(name="kml_description",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_KML_DESC,
                         on_verify=None)
        # neighbor_output_type
        self.Meta.define(name="neighbor_output_type",
                         data_type=Options,
                         data_options=Options(NeighborOutput),
                         data_default=NeighborOutput.NONE,
                         on_verify=None)
        # neighbor_output_file_name
        self.Meta.define(name="neighbor_output_file_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_NEIGHBOR_OUTPUT_FILE,
                         on_verify=None)
        # children_output_type
        self.Meta.define(name="children_output_type",
                         data_type=Options,
                         data_options=Options(ChildrenOutput),
                         data_default=ChildrenOutput.NONE,
                         on_verify=None)
        # children_output_file_name
        self.Meta.define(name="children_output_file_name",
                         data_type=str,
                         data_options=None,
                         data_default=Constants.DEFAULT_CHILDREN_OUTPUT_FILE,
                         on_verify=None)
        # randpts_concatenate_output
        self.Meta.define(name="randpts_concatenate_output",
                         data_type=bool,
                         data_options=None,
                         data_default=False,
                         on_verify=None)
        # randpts_num_per_cell
        self.Meta.define(name="randpts_num_per_cell",
                         data_type=int,
                         data_options=None,
                         data_default=0,
                         on_verify=lambda value: 0 <= int(value) < Constants.MAXIMUM_INT)
        # randpts_seed
        self.Meta.define(name="randpts_seed",
                         data_type=int,
                         data_options=None,
                         data_default=Constants.DEFAULT_RAND_SEED,
                         on_verify=lambda value: 0 <= int(value) < sys.maxsize)
        # max_cells_per_output_file
        self.Meta.define(name="max_cells_per_output_file",
                         data_type=int,
                         data_options=None,
                         data_default=0,
                         on_verify=lambda value: 0 <= int(value) < sys.maxsize)
        # output_first_seqnum
        self.Meta.define(name="output_first_seqnum",
                         data_type=int,
                         data_options=None,
                         data_default=1,
                         on_verify=lambda value: 0 <= int(value) < sys.maxsize)
        # output_last_seqnum
        self.Meta.define(name="output_last_seqnum",
                         data_type=int,
                         data_options=None,
                         data_default=sys.maxsize - 1,
                         on_verify=lambda value: 0 <= int(value) < sys.maxsize)
