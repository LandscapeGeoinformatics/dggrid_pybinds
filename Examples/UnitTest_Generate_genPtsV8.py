import sys

from pydggrid.Queries import PointGen
from pydggrid.Types import CellOutput, DGGSType, BinCoverage, PointDataType, OutputAddress, OutputControl

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: PointGen = PointGen()
    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 10)
    document.set_coverage(BinCoverage.PARTIAL)
    document.set_output(OutputControl.OUTPUT_OCCUPIED)
    document.input.geometry("../DGGRID/examples/genPtsV8/inputfiles/airport_point.geojson")
    document.run()

    print("\n---QUERY RESPONSE [CELLS]---\n")
    print(f"COLUMNS: {document.cells.get_columns()}\n")
    print(f"---[CELLS (TEXT)]---\n{document.cells.get_aigen()}")
    print(f"---[CELLS (DataFrame)]---\n{document.cells.get_frame()}")
    print(f"---[CELLS (GeoDataFrame)]---\n{document.cells.get_geoframe()}")
    print(f"---[CELLS (Numpy)]---\n{document.cells.get_numpy()}")
    print(f"---[CELLS (XML)]---\n{document.cells.get_kml()}")
    print("\n---QUERY RESPONSE [POINTS]---\n")
    print(f"COLUMNS: {document.points.get_columns()}\n")
    print(f"---[POINTS (TEXT)]---\n{document.points.get_aigen()}")
    print(f"---[POINTS (DataFrame)]---\n{document.points.get_frame()}")
    print(f"---[POINTS (GeoDataFrame)]---\n{document.points.get_geoframe()}")
    print(f"---[POINTS (Numpy)]---\n{document.points.get_numpy()}")
    print(f"---[POINTS (XML)]---\n{document.points.get_kml()}")
    print("\n---QUERY RESPONSE [INDEXES]---\n")
    print(f"COLUMNS: {document.indexes.get_columns()}\n")
    print(f"---[INDEXES (DataFrame)]---\n{document.indexes.get_frame()}")
    print(f"---[POINTS (GeoDataFrame)]---\n{document.indexes.get_geoframe()}")
    print(f"---[POINTS (Numpy)]---\n{document.indexes.get_numpy()}")
    print(f"---[POINTS (XML)]---\n{document.indexes.get_xml()}")

# ################################################################################
# ################################################################################
# #
# # genPtsV8.meta - example of a dggrid meta-file which outputs all cells which
# #      contain one or more input points, using GDAL Shapefiles for input and
# #      output.
# #
# # Determine the cells that contain Oregon airports in resolution 10 of the
# # ISEA3H DGGS.
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID_FROM_POINTS
#
# # specify the DGG
#
# dggs_type ISEA3H
# dggs_res_spec 10
#
# # specify bin controls
#
# # indicate that we're only using a small part of the globe
# # this helps DGGRID use memory more efficiently
# bin_coverage PARTIAL
#
# # specify the input
# input_files inputfiles/airport_point.geojson
# point_input_file_type GDAL
#
# # specify the output
# cell_output_control OUTPUT_OCCUPIED
# output_cell_label_type OUTPUT_ADDRESS_TYPE
# output_address_type SEQNUM
#
# output_delimiter ","
# precision 7
#
# # output the count of contained input points for each cell?
# # note Shapefile field names must be 10 characters or less
# output_count TRUE
# output_count_field_name numAirports
#
# # version 7 style text output parameters
# # for backwards compatibility the text file is output by default.
# output_file_name outputfiles/textOutput.txt
# # Set to NONE for no text output.
# output_file_type TEXT
#
# # specify the per-cell output using GDAL-supported file formats
#
# # output the cells
# cell_output_type GDAL
# cell_output_gdal_format GeoJSON
# cell_output_file_name outputfiles/airportCells.geojson
#
# # other output parameters
# densification 0
# precision 7