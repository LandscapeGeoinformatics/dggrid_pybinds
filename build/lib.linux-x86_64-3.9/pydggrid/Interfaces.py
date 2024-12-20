import datetime
import os
import pathlib
import sys
import time
from abc import ABC, abstractmethod
from typing import List, Any, Dict, TextIO, Callable

import geojson
import geopandas
import numpy
import pandas
import pyarrow

from pydggrid.System import Constants
from pydggrid.Objects import Attributes, Options, Choice
from pydggrid.Types import Operation, ClipType, ClipMethod, DGGSType, DGGSPoly, Topology, DGGSProjection, DataType
from pydggrid.Types import Aperture, ProjectionDatum, OrientationType, ResolutionType, AddressField, PointDataType
from pydggrid.Types import InputAddress, BinCoverage, OutputControl, OutputType, OutputAddress, LongitudeWrap, CellLabel
from pydggrid.Types import CellOutput, PointOutput, RandPointOutput, NeighborOutput, ChildrenOutput


class Query:
    """
    Query Base Object
    _op: Operation Type
    Attributes: Attributes Object
    """

    def __init__(self, operation: Operation):
        """
        Default constructor
        :param operation: Operation Type
        """
        self._op: Operation = operation
        self._time: int = int(time.time() * 1000)
        self.Attributes: Attributes = Attributes()
        # Setup default parameters
        # dggrid_operation
        self.Attributes.define(name="dggrid_operation",
                               data_type=Options,
                               data_options=Options(Operation),
                               data_default=operation,
                               on_verify=None)
        # precision
        self.Attributes.define(name="precision",
                               data_type=int,
                               data_options=None,
                               data_default=Constants.DEFAULT_PRECISION,
                               on_verify=lambda value: Constants.MAXIMUM_INT > int(value) > 0)
        # verbosity
        self.Attributes.define(name="verbosity",
                               data_type=int,
                               data_options=None,
                               data_default=0,
                               on_verify=lambda value: Constants.MAXIMUM_VERBOSITY > int(value) > -1)
        # pause_on_startup
        self.Attributes.define(name="pause_on_startup",
                               data_type=bool,
                               data_options=None,
                               data_default=False,
                               on_verify=None)
        # pause_before_exit
        self.Attributes.define(name="pause_before_exit",
                               data_type=bool,
                               data_options=None,
                               data_default=False,
                               on_verify=None)
        # update_frequency
        self.Attributes.define(name="update_frequency",
                               data_type=int,
                               data_options=None,
                               data_default=100000,
                               on_verify=lambda value: sys.maxsize > int(value) > 5)
        # geodetic_densify
        self.Attributes.define(name="geodetic_densify",
                               data_type=float,
                               data_options=None,
                               data_default=float(0.0),
                               on_verify=lambda value: sys.float_info.epsilon <= float(value) <=
                                                       Constants.MAXIMUM_GEO_DENSIFY)
        # clip_subset_type
        self.Attributes.define(name="clip_subset_type",
                               data_type=Options,
                               data_options=Options(ClipType),
                               data_default=ClipType.WHOLE_EARTH,
                               on_verify=None)
        # clip_cell_densification
        self.Attributes.define(name="clip_cell_densification",
                               data_type=int,
                               data_options=None,
                               data_default=1,
                               on_verify=lambda value: Constants.MAXIMUM_DENSIFICATION > int(value) > -1)
        # clip_type
        self.Attributes.define(name="clip_type",
                               data_type=Options,
                               data_options=Options(ClipMethod),
                               data_default=ClipMethod.POLY_INTERSECT,
                               on_verify=None)
        # clipper_scale_factor
        self.Attributes.define(name="clipper_scale_factor",
                               data_type=int,
                               data_options=None,
                               data_default=1000000,
                               on_verify=lambda value: int(value) > 0)
        # clip_subset_type
        self.Attributes.define(name="clip_subset_type",
                               data_type=Options,
                               data_options=Options(ClipType),
                               data_default=ClipType.WHOLE_EARTH,
                               on_verify=None)
        # clip_using_holes
        self.Attributes.define(name="clip_using_holes",
                               data_type=bool,
                               data_options=None,
                               data_default=False,
                               on_verify=None)
        # clip_region_files
        self.Attributes.define(name="clip_region_files",
                               data_type=str,
                               data_options=None,
                               data_default="test.gen",
                               on_verify=None)
        # clip_cell_res
        self.Attributes.define(name="clip_cell_res",
                               data_type=int,
                               data_options=None,
                               data_default=1,
                               on_verify=lambda value: 0 < int(value) <= Constants.MAX_DGG_RES)
        # clipper_scale_factor
        self.Attributes.define(name="clipper_scale_factor",
                               data_type=int,
                               data_options=None,
                               data_default=1000000,
                               on_verify=lambda value: 0 < int(value) < sys.maxsize)
        # dggs_type
        self.Attributes.define(name="dggs_type",
                               data_type=Options,
                               data_options=Options(DGGSType),
                               data_default=DGGSType.CUSTOM,
                               on_verify=None)
        # dggs_base_poly
        self.Attributes.define(name="dggs_base_poly",
                               data_type=Options,
                               data_options=Options(DGGSPoly),
                               data_default=DGGSPoly.ICOSAHEDRON,
                               on_verify=None)
        # dggs_topology
        self.Attributes.define(name="dggs_topology",
                               data_type=Options,
                               data_options=Options(Topology),
                               data_default=Topology.HEXAGON,
                               on_verify=None)
        # dggs_proj
        self.Attributes.define(name="dggs_proj",
                               data_type=Options,
                               data_options=Options(DGGSProjection),
                               data_default=DGGSProjection.ISEA,
                               on_verify=None)
        # dggs_aperture_type
        self.Attributes.define(name="dggs_aperture_type",
                               data_type=Options,
                               data_options=Options(Aperture),
                               data_default=Aperture.PURE,
                               on_verify=None)
        # dggs_aperture
        self.Attributes.define(name="dggs_aperture",
                               data_type=Choice,
                               data_options=Choice(Constants.APERTURE_VALUES),
                               data_default=4,
                               on_verify=None)
        # dggs_aperture
        self.Attributes.define(name="dggs_aperture_sequence",
                               data_type=str,
                               data_options=None,
                               data_default="333333333333",
                               on_verify=None)
        # dggs_num_aperture_4_res
        self.Attributes.define(name="dggs_num_aperture_4_res",
                               data_type=int,
                               data_options=None,
                               data_default=0,
                               on_verify=lambda value: -1 < int(value) <= Constants.MAX_DGG_RES)
        # proj_datum
        self.Attributes.define(name="proj_datum",
                               data_type=Options,
                               data_options=Options(ProjectionDatum),
                               data_default=ProjectionDatum.WGS84_AUTHALIC_SPHERE,
                               on_verify=None)
        # proj_datum_radius
        self.Attributes.define(name="proj_datum_radius",
                               data_type=float,
                               data_options=None,
                               data_default=1.0,
                               on_verify=lambda value: 1.0 <= float(value) <= Constants.MAXIMUM_DATUM_RADIUS)
        # dggs_orient_specify_type
        self.Attributes.define(name="dggs_orient_specify_type",
                               data_type=Options,
                               data_options=Options(OrientationType),
                               data_default=OrientationType.SPECIFIED,
                               on_verify=None)
        # dggs_num_placements
        self.Attributes.define(name="dggs_num_placements",
                               data_type=int,
                               data_options=None,
                               data_default=0,
                               on_verify=lambda value: 1 < int(value) <= Constants.MAXIMUM_INT)
        # dggs_orient_rand_seed
        self.Attributes.define(name="dggs_orient_rand_seed",
                               data_type=int,
                               data_options=None,
                               data_default=Constants.DEFAULT_RAND_SEED,
                               on_verify=lambda value: 1 < int(value) <= sys.maxsize)
        # dggs_vert0_lon
        self.Attributes.define(name="dggs_vert0_lon",
                               data_type=float,
                               data_options=None,
                               data_default=Constants.VERT0_LONGITUDE_DEFAULT,
                               on_verify=lambda value: Constants.LONGITUDE_LIMITS[0] <= float(value) <=
                                                       Constants.LONGITUDE_LIMITS[1])
        # dggs_vert0_lat
        self.Attributes.define(name="dggs_vert0_lat",
                               data_type=float,
                               data_options=None,
                               data_default=Constants.VERT0_LATITUDE_DEFAULT,
                               on_verify=lambda value: Constants.LATITUDE_LIMITS[0] <= float(value) <=
                                                       Constants.LATITUDE_LIMITS[1])
        # dggs_vert0_azimuth
        self.Attributes.define(name="dggs_vert0_azimuth",
                               data_type=float,
                               data_options=None,
                               data_default=Constants.VERT0_AZIMUTH_DEFAULT,
                               on_verify=lambda value: Constants.AZIMUTH_LIMITS[0] <= float(value) <=
                                                       Constants.AZIMUTH_LIMITS[1])
        # region_center_lon
        self.Attributes.define(name="region_center_lon",
                               data_type=float,
                               data_options=None,
                               data_default=Constants.CENTER_LONGITUDE_DEFAULT,
                               on_verify=lambda value: Constants.LONGITUDE_LIMITS[0] <= float(value) <=
                                                       Constants.LONGITUDE_LIMITS[1])
        # region_center_lat
        self.Attributes.define(name="region_center_lat",
                               data_type=float,
                               data_options=None,
                               data_default=Constants.CENTER_LATITUDE_DEFAULT,
                               on_verify=lambda value: Constants.LATITUDE_LIMITS[0] <= float(value) <=
                                                       Constants.LATITUDE_LIMITS[1])
        # dggs_orient_specify_type
        self.Attributes.define(name="dggs_res_specify_type",
                               data_type=Options,
                               data_options=Options(ResolutionType),
                               data_default=ResolutionType.SPECIFIED,
                               on_verify=None)
        # dggs_res_specify_area
        self.Attributes.define(name="dggs_res_specify_area",
                               data_type=float,
                               data_options=None,
                               data_default=Constants.DEFAULT_RESOLUTION_AREA,
                               on_verify=lambda value: sys.float_info.epsilon <= float(value) <
                                                       Constants.MAXIMUM_RESOLUTION_AREA)
        # dggs_res_specify_intercell_distance
        self.Attributes.define(name="dggs_res_specify_intercell_distance",
                               data_type=float,
                               data_options=None,
                               data_default=Constants.DEFAULT_INTERCELL_DISTANCE,
                               on_verify=lambda value: sys.float_info.epsilon <= float(value) <
                                                       Constants.MAXIMUM_INTERCELL_DISTANCE)
        # dggs_res_specify_rnd_down
        self.Attributes.define(name="dggs_res_specify_rnd_down",
                               data_type=bool,
                               data_options=None,
                               data_default=True,
                               on_verify=None)
        # dggs_res_spec
        self.Attributes.define(name="dggs_res_spec",
                               data_type=int,
                               data_options=None,
                               data_default=Constants.DEFAULT_DGG_RES,
                               on_verify=lambda value: 0 <= int(value) < Constants.MAX_DGG_RES)
        # input_files
        self.Attributes.define(name="input_files",
                               data_type=str,
                               data_options=None,
                               data_default="vals.txt",
                               on_verify=None)
        # input_file_name
        self.Attributes.define(name="input_file_name",
                               data_type=str,
                               data_options=None,
                               data_default="valsin.txt",
                               on_verify=None)
        # input_address_field_type
        self.Attributes.define(name="input_address_field_type",
                               data_type=Options,
                               data_options=Options(AddressField),
                               data_default=AddressField.GEO_POINT,
                               on_verify=None)
        # point_input_file_type
        self.Attributes.define(name="point_input_file_type",
                               data_type=Options,
                               data_options=Options(PointDataType),
                               data_default=PointDataType.NONE,
                               on_verify=None)
        # input_address_type
        self.Attributes.define(name="input_address_type",
                               data_type=Options,
                               data_options=Options(InputAddress),
                               data_default=InputAddress.GEO,
                               on_verify=None)
        # input_delimiter
        self.Attributes.define(name="input_delimiter",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_DELIMITER,
                               on_verify=None)
        # bin_coverage
        self.Attributes.define(name="bin_coverage",
                               data_type=Options,
                               data_options=Options(BinCoverage),
                               data_default=BinCoverage.GLOBAL,
                               on_verify=None)
        # output_count
        self.Attributes.define(name="output_count",
                               data_type=bool,
                               data_options=None,
                               data_default=False,
                               on_verify=None)
        # output_count_field_name
        self.Attributes.define(name="output_count_field_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_COUNT_FIELD_NAME,
                               on_verify=lambda value: len(str(value)) > 0)
        # input_value_field_name
        self.Attributes.define(name="input_value_field_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_VALUE_FIELD_NAME,
                               on_verify=lambda value: len(str(value)) > 0)
        # output_total
        self.Attributes.define(name="output_total",
                               data_type=bool,
                               data_options=None,
                               data_default=False,
                               on_verify=None)
        # output_total_field_name
        self.Attributes.define(name="output_total_field_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_TOTAL_FIELD_NAME,
                               on_verify=lambda value: len(str(value)) > 0)
        # output_total
        self.Attributes.define(name="output_mean",
                               data_type=bool,
                               data_options=None,
                               data_default=False,
                               on_verify=None)
        # output_mean_field_name
        self.Attributes.define(name="output_mean_field_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_MEAN_FIELD_NAME,
                               on_verify=lambda value: len(str(value)) > 0)
        # output_presence_vector
        self.Attributes.define(name="output_presence_vector",
                               data_type=bool,
                               data_options=None,
                               data_default=False,
                               on_verify=None)
        # output_presence_vector_field_name
        self.Attributes.define(name="output_presence_vector_field_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_PRESENCE_FIELD_NAME,
                               on_verify=lambda value: len(str(value)) > 0)
        # output_num_classes
        self.Attributes.define(name="output_num_classes",
                               data_type=bool,
                               data_options=None,
                               data_default=False,
                               on_verify=None)
        # output_num_classes_field_name
        self.Attributes.define(name="output_num_classes_field_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_N_CLASS_FIELD_NAME,
                               on_verify=lambda value: len(str(value)) > 0)
        # cell_output_control
        self.Attributes.define(name="cell_output_control",
                               data_type=Options,
                               data_options=Options(OutputControl),
                               data_default=OutputControl.OUTPUT_ALL,
                               on_verify=None)
        # output_file_name
        self.Attributes.define(name="output_file_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_OUTPUT_FILE_NAME,
                               on_verify=None)
        # output_file_type
        self.Attributes.define(name="output_file_type",
                               data_type=Options,
                               data_options=Options(OutputType),
                               data_default=OutputType.NONE,
                               on_verify=None)
        # output_file_type
        self.Attributes.define(name="output_file_type",
                               data_type=Options,
                               data_options=Options(OutputType),
                               data_default=OutputType.NONE,
                               on_verify=None)
        # output_address_type
        self.Attributes.define(name="output_address_type",
                               data_type=Options,
                               data_options=Options(OutputAddress),
                               data_default=OutputAddress.SEQNUM,
                               on_verify=None)
        # output_delimiter
        self.Attributes.define(name="output_delimiter",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_DELIMITER,
                               on_verify=None)
        # densification
        self.Attributes.define(name="densification",
                               data_type=int,
                               data_options=None,
                               data_default=0,
                               on_verify=lambda value: 0 <= int(value) <= Constants.MAXIMUM_DENSIFICATION)
        # longitude_wrap_mode
        self.Attributes.define(name="longitude_wrap_mode",
                               data_type=Options,
                               data_options=Options(LongitudeWrap),
                               data_default=LongitudeWrap.WRAP,
                               on_verify=None)
        # unwrap_points
        self.Attributes.define(name="unwrap_points",
                               data_type=bool,
                               data_options=None,
                               data_default=False,
                               on_verify=None)
        # output_cell_label_type
        self.Attributes.define(name="output_cell_label_type",
                               data_type=Options,
                               data_options=Options(CellLabel),
                               data_default=CellLabel.GLOBAL_SEQUENCE,
                               on_verify=None)
        # cell_output_type
        self.Attributes.define(name="cell_output_type",
                               data_type=Options,
                               data_options=Options(CellOutput),
                               data_default=CellOutput.NONE,
                               on_verify=None)
        # point_output_type
        self.Attributes.define(name="point_output_type",
                               data_type=Options,
                               data_options=Options(PointOutput),
                               data_default=CellOutput.NONE,
                               on_verify=None)
        # randpts_output_type
        self.Attributes.define(name="randpts_output_type",
                               data_type=Options,
                               data_options=Options(RandPointOutput),
                               data_default=CellOutput.NONE,
                               on_verify=None)
        # cell_output_gdal_format
        self.Attributes.define(name="cell_output_gdal_format",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_GDAL_FORMAT,
                               on_verify=None)
        # point_output_gdal_format
        self.Attributes.define(name="point_output_gdal_format",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_GDAL_FORMAT,
                               on_verify=None)
        # collection_output_gdal_format
        self.Attributes.define(name="collection_output_gdal_format",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_GDAL_FORMAT,
                               on_verify=None)
        # cell_output_file_name
        self.Attributes.define(name="cell_output_file_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_CELL_OUTPUT_FILE,
                               on_verify=None)
        # point_output_file_name
        self.Attributes.define(name="point_output_file_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_POINTS_OUTPUT_FILE,
                               on_verify=None)
        # randpts_output_file_name
        self.Attributes.define(name="randpts_output_file_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_RAND_POINTS_OUTPUT_FILE,
                               on_verify=None)
        # collection_output_file_name
        self.Attributes.define(name="collection_output_file_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_COLLECTION_OUTPUT_FILE,
                               on_verify=None)
        # dggs_orient_output_file_name
        self.Attributes.define(name="dggs_orient_output_file_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_DGGS_ORIENT_OUTPUT_FILE,
                               on_verify=None)
        # shapefile_id_field_length
        self.Attributes.define(name="shapefile_id_field_length",
                               data_type=int,
                               data_options=None,
                               data_default=Constants.MAXIMUM_ID_FIELD_LEN,
                               on_verify=lambda value: 0 < int(value) < Constants.MAXIMUM_ID_FIELD_LEN)
        # kml_default_width
        self.Attributes.define(name="kml_default_width",
                               data_type=int,
                               data_options=None,
                               data_default=Constants.MAXIMUM_ID_FIELD_LEN,
                               on_verify=lambda value: 0 < int(value) < Constants.MAXIMUM_KML_WIDTH)
        # kml_default_color
        self.Attributes.define(name="kml_default_color",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_KML_COLOR,
                               on_verify=None)
        # kml_name
        self.Attributes.define(name="kml_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_KML_NAME,
                               on_verify=None)
        # kml_description
        self.Attributes.define(name="kml_description",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_KML_DESC,
                               on_verify=None)
        # neighbor_output_type
        self.Attributes.define(name="neighbor_output_type",
                               data_type=Options,
                               data_options=Options(NeighborOutput),
                               data_default=NeighborOutput.NONE,
                               on_verify=None)
        # neighbor_output_file_name
        self.Attributes.define(name="neighbor_output_file_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_NEIGHBOR_OUTPUT_FILE,
                               on_verify=None)
        # children_output_type
        self.Attributes.define(name="children_output_type",
                               data_type=Options,
                               data_options=Options(ChildrenOutput),
                               data_default=ChildrenOutput.NONE,
                               on_verify=None)
        # children_output_file_name
        self.Attributes.define(name="children_output_file_name",
                               data_type=str,
                               data_options=None,
                               data_default=Constants.DEFAULT_CHILDREN_OUTPUT_FILE,
                               on_verify=None)
        # randpts_concatenate_output
        self.Attributes.define(name="randpts_concatenate_output",
                               data_type=bool,
                               data_options=None,
                               data_default=False,
                               on_verify=None)
        # randpts_num_per_cell
        self.Attributes.define(name="randpts_num_per_cell",
                               data_type=int,
                               data_options=None,
                               data_default=0,
                               on_verify=lambda value: 0 <= int(value) < Constants.MAXIMUM_INT)
        # randpts_seed
        self.Attributes.define(name="randpts_seed",
                               data_type=int,
                               data_options=None,
                               data_default=Constants.DEFAULT_RAND_SEED,
                               on_verify=lambda value: 0 <= int(value) < sys.maxsize)
        # max_cells_per_output_file
        self.Attributes.define(name="max_cells_per_output_file",
                               data_type=int,
                               data_options=None,
                               data_default=0,
                               on_verify=lambda value: 0 <= int(value) < sys.maxsize)
        # output_first_seqnum
        self.Attributes.define(name="output_first_seqnum",
                               data_type=int,
                               data_options=None,
                               data_default=1,
                               on_verify=lambda value: 0 <= int(value) < sys.maxsize)
        # output_last_seqnum
        self.Attributes.define(name="output_last_seqnum",
                               data_type=int,
                               data_options=None,
                               data_default=sys.maxsize - 1,
                               on_verify=lambda value: 0 <= int(value) < sys.maxsize)
        #
        self.Attributes.save("dggrid_operation", self._op)

    def type(self) -> Operation:
        """
        Returns the operation type
        :return: Operation type
        """
        return self._op

    def time(self) -> int:
        """
        Returns epoch time stamp of the query
        :return: Epoch time stamp as integer
        """
        return self._time

    def desc(self, show_empty: bool = False) -> str:
        """
        Describes the query
        :param show_empty if enabled empty fields will be shown
        :return: Query Description
        """
        string_array: List[str] = list()
        string_array.append(f"Type: {self.type().name}")
        string_array.append(f"Time Stamp: {datetime.datetime.fromtimestamp(self.time() / 1000.0)}")
        string_array.append(f"Parameters:")
        string_array.append(self.Attributes.__str__())
        return os.linesep.join(string_array)

    def print(self, show_empty: bool = False) -> None:
        """
        Prints the query data
        :param show_empty if enabled empty fields will be shown
        :return: None
        """
        print(self.desc(show_empty))

    def io(self, name: str, data: [Any, None]) -> Any:
        """
        Set / Get encoder
        :param name: Parameter Name
        :param data: Parameter data, if set to none it will be ignored
        :return: Any attribute requested
        """
        if data is not None:
            self.Attributes.save(name, data)
        return self.Attributes.get(name)

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
            self.Attributes.save_str(parameter, parameters[parameter])

    def set_precision(self, precision: int = Constants.DEFAULT_PRECISION) -> int:
        """
        Sets the precision factor of the query
        :param precision: Precision Factor, Defaults to Constants.DEFAULT_PRECISION
        :return: Integer representing the precision factor
        """
        return self.Attributes.as_int("precision")

    # override
    def __str__(self) -> str:
        return self.desc()

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


class Dataset(ABC):

    def __init__(self):
        self.crs: str = "EPSG:4326"
        self.data: List[bytes] = list([])
        self.elements: List[str] = list([])
        self.types: List[DataType] = list([])
        self.callbacks: Dict[str, Callable[[Any, Any], None]] = dict({})
        self.extensions: Dict[str, Callable[[pathlib.Path, bytes, Any], None]] = dict({})

    def register_call(self, data_type: type, callback: Callable[[Any, Any], None]) -> None:
        """
        Registers a callback for processing
        :param data_type: Data Type
        :param callback: Callback, must be registered as function(records, definition) and return None
        :return:
        """
        self.callbacks[str(data_type)] = callback

    def register_extension(self, file_extension: str, callback: Callable[[pathlib.Path, bytes], None] = None) -> None:
        """
        Registers callback to a file extension
        :param file_extension: File extension
        :param callback: Callback should accept (pathlib, bytes)
        :return: None
        """
        self.extensions[file_extension.lower()] = callback

    def register_io(self, extension: str, callback: Callable[[Any, Any], Any]) -> None:
        """
        Registers an extension processing callback
        :param extension: File extension to trigger on
        :param callback: Callback to use
        :return: None
        """
        self.extensions[extension] = callback

    def save(self,
             records: [List,
                       Dict,
                       str,
                       pathlib.Path,
                       pandas.DataFrame,
                       geopandas.geoseries,
                       geopandas.GeoDataFrame,
                       numpy.ndarray,
                       pyarrow.Array,
                       pyarrow.Table,
                       geojson.GeoJSON],
             definition: [List[str], List[int], str, None]) -> None:
        """
        Saves records into dataset
        :param records: Records to save into the buffer
        :param definition: Columns definition data
        :return: None
        """
        type_t: str = str(type(records))
        if type_t not in self.callbacks:
            raise ValueError(f"Record data type {type_t} is not supported for this object.")
        if (type(records) == str and os.path.isfile(records)) or type(records) == pathlib.Path:
            return self.read(records, definition)
        callback: Callable[[Any, Any], None] = self.callbacks.get(type_t, None)
        callback(records, definition)

    def read(self,
             file_path: [str, pathlib.Path],
             definition: [List[str], List[int], str, None]) -> None:
        """
        Reads data from a file
        :param file_path: File path to read
        :param definition: Definition base
        :return: None
        """
        if isinstance(file_path, str):
            return self.read(pathlib.Path(file_path), definition)
        file_extension: str = file_path.suffix.lower()[1:]
        if file_extension not in self.extensions.keys():
            raise ValueError(f"Extension type not supported in object {file_extension}")
        else:
            file = open(file_path.absolute(), "rb")
            file_data: bytes = file.read()
            file.close()
            callback: Callable[[pathlib.Path, bytes, Any], None] = self.extensions[file_extension]
            callback(file_path, file_data, definition)

    def write(self, data: Any, data_type: DataType) -> None:
        """
        Writes data to the buffer
        :param data: Buffer Data
        :param data_type: Data Type definition
        :return: None
        """
        if isinstance(data, str):
            byte_data: List[bytes] = list([])
            byte_data.append(DataType.INT.convert_bytes(len(data)))
            byte_data.append(str(data).encode())
            self.data.append(b''.join(byte_data))
            self.types.append(data_type)
        elif isinstance(data, pathlib.Path):
            file = open(pathlib.Path(data).absolute(), "rb")
            byte_data: bytes = file.read()
            file.close()
            byte_array: List[bytes] = list([])
            byte_array.append(DataType.INT.convert_bytes(len(byte_data)))
            byte_array.append(byte_data)
            self.data.append(b''.join(byte_array))
            self.types.append(data_type)
        elif isinstance(data, list):
            byte_array: List[bytes] = list([])
            byte_array.append(DataType.INT.convert_bytes(len(data)))
            [byte_array.append(data_type.convert_bytes(n)) for n in data]
            self.data.append(b''.join(byte_array))
            self.types.append(data_type)
            [self.elements.append(str(n)) for n in data]
        elif isinstance(data, bytes):
            self.data.append(data)
            self.types.append(data_type)
        else:
            raise ValueError("Unrecognized input values")
        
    def integer_list(self, delimiter: str = " ") -> str:
        """
        returns data set as an integer list
        :param delimiter: Integer delimiter
        :return: Integer List array
        """
        return delimiter.join(self.elements)

    def size(self) -> int:
        """
        Returns record count
        :return: Record Count
        """
        return len(self.data)

    # Override
    def __bytes__(self) -> bytes:
        """
        Renders DataSet Bytes
        :return:
        """
        byte_array: List[bytes] = list()
        index_range: List[int] = list(range(0, self.size()))
        byte_array.append(DataType.INT.convert_bytes(self.size()))
        for index in index_range:
            byte_array.append(DataType.INT.convert_bytes(int(self.types[index])))
            byte_array.append(DataType.INT.convert_bytes(len(self.data[index])))
            byte_array.append(self.data[index])
        return b''.join(byte_array)