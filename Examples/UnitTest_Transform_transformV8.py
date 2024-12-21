import sys

from pydggrid.Queries import Transform
from pydggrid.Types import ClipType, InputAddress, DGGSType, PointOutput

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Transform = Transform()
    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 9)
    document.input_points("../DGGRID/examples/transformV8/inputfiles/20k.txt")
    document.input_points("../DGGRID/examples/transformV8/inputfiles/50k.txt")
    document.input_points("../DGGRID/examples/transformV8/inputfiles/200k.txt")
    document.input_points("../DGGRID/examples/transformV8/inputfiles/100k.txt")
    document.run()
    print("---QUERY RESPONSE [RECORDS]---\n")
    print(f"COLUMNS: {document.records.get_columns()}\n")
    print(f"---[RECORDS (DataFrame)]---\n{document.records.get_frame()}")
    print(f"---[RECORDS (GeoDataFrame)]---\n{document.records.get_geoframe()}")
    print(f"---[RECORDS (Numpy)]---\n{document.records.get_numpy()}")
    print("---QUERY RESPONSE [CELLS]---\n")
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

# ################################################################################
# ################################################################################
# #
# # transformV8.meta - example of a dggrid meta-file which performs address
# #       conversion with GDAL cell geometry output
# #
# # Transformation from GEO to DGGS cells effectively determines the cell in which
# # each of the input Oregon cities are located in a resolution 8 ISEA3H DGGS.
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation TRANSFORM_POINTS
#
# # specify the DGG
# dggs_type ISEA3H
# dggs_res_spec 9
#
# # specify bin controls
# input_files inputfiles/100k.txt inputfiles/200k.txt inputfiles/20k.txt inputfiles/50k.txt
# input_address_type GEO
# input_delimiter " "
#
# # specify the output
# output_address_type SEQNUM
# output_delimiter ","
#
# # version 7 style text output parameters
# # for backwards compatibility the text file is output by default.
# output_file_name outputfiles/cities3h9.txt
# # Set to NONE for no text output.
# output_file_type TEXT
#
# # specify the output collection file used
# # when GDAL_COLLECTION is specified below
# collection_output_gdal_format GeoJSON
# collection_output_file_name ./outputfiles/cities3h9.geojson
#
# # specify which output you want to put together in a GDAL_COLLECTION
# # this must include cell and/or point output
# cell_output_type GDAL_COLLECTION
# point_output_type GDAL_COLLECTION
