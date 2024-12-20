import csv
import json
import os.path
import pathlib
import string
import sys
from typing import List, Dict, Any

import geojson
import geopandas
import pandas
from shapely import Polygon


class Library:

    @staticmethod
    def is_csv_string(csv_string) -> bool:
        """
        returns true if the given string is a csv file
        :param csv_string: String data
        :return: True if string is a csv
        """
        try:
            csv.Sniffer().sniff(csv_string)
            return True if "," in csv_string else False
        except csv.Error:
            return False

    @staticmethod
    def is_csv_file(infile: [str, pathlib.Path]) -> bool:
        """
        Returns true if the file path passed is a csv file.
        :param infile: In file string or pathlib.Path object
        :return:
        """
        if isinstance(infile, str):
            return Library.is_csv_file(pathlib.Path(infile))
        if not os.path.isfile(infile):
            return False
        # noinspection PyBroadException
        try:
            with open(infile.absolute(), newline='') as csvfile:
                start = csvfile.read(4096)
                if not all([c in string.printable or c.isprintable() for c in start]):
                    return False
                dialect = csv.Sniffer().sniff(start)
                return True
        except:
            # Could not get a csv dialect -> probably not a csv.
            return False

    @staticmethod
    def is_json_string(json_string: str) -> bool:
        """
        Returns true if the given string is a geojson string
        :param json_string: JSON String object
        :return: True if the string is a geojson
        """
        # noinspection PyBroadException
        try:
            json.loads(json_string)
            return True
        except:
            return False

    @staticmethod
    def is_json_file(infile: [str, pathlib.Path]) -> bool:
        """
        Returns true if the json file is valid
        :param infile: Json file
        :return: True if the json file is valid
        """
        if isinstance(infile, str):
            return Library.is_json_file(pathlib.Path(infile))
        if not os.path.isfile(infile.absolute()):
            return False
        with open(infile.absolute(), newline='') as json_file:
            return Library.is_json_string(infile.read_text())

    @staticmethod
    def is_geojson(data: [str, dict, geojson.GeoJSON]):
        """
        Returns true if the given dictionary or json is a geojson
        :param data: JSON or dictionary data
        :return: True if geojson
        """
        # noinspection PyBroadException
        if isinstance(data, dict) or isinstance(data, geojson.GeoJSON):
            return Library.is_geojson(json.dumps(data))
        try:
            json_data: dict = json.loads(data) if isinstance(data, str) else data
            geojson.loads(json.dumps(json_data))
            return True
        except Exception as exc:
            return False

    @staticmethod
    def aigen_frame(aigen_data: str, crs: str = 'epsg:4326') -> geopandas.GeoDataFrame:
        """
        Converts aigen data to a geo-dataframe
        :param aigen_data: Aigen String
        :param crs: Geopandas CRS Mode
        :return: Constructed GeoDataframe object
        """
        cell_id: int = 0
        elements: Dict[int, List[List[float]]] = dict({})
        data_lines: List[str] = aigen_data.split(os.linesep)
        for data_line in data_lines:
            if data_line.strip() == "": continue
            if data_line.strip() == "END": continue
            cell_content: List[str] = data_line.split(" ")
            cell_elements: List[str] = [n.strip() for n in cell_content if n.strip() != ""]
            cell_lead: bool = True if len(cell_elements) == 3 and cell_elements[0].isnumeric() else False
            cell_id = int(cell_elements[0]) if cell_lead is True else cell_id
            #
            if cell_id not in elements.keys(): elements[cell_id] = list([[], []])
            x_point: float = float(cell_elements[0]) if cell_lead is False else float(cell_elements[1])
            y_point: float = float(cell_elements[1]) if cell_lead is False else float(cell_elements[2])
            elements[cell_id][0].append(x_point)
            elements[cell_id][1].append(y_point)
        data_records: List[Dict[str, Any]] = list([])
        for index_id in elements:
            data_records.append({"id": index_id,
                                 "geometry": Polygon(zip(elements[index_id][0], elements[index_id][1]))})
        data_frame: pandas.DataFrame = pandas.DataFrame(data_records)
        return geopandas.GeoDataFrame(data_frame)

    @staticmethod
    def is_float(data: str) -> bool:
        """
        Returns true if the given string is Float compatible
        :param data: Data Styring
        :return: True if string is a float
        """
        try:
            float(data)
            return True
        except ValueError:
            return False

