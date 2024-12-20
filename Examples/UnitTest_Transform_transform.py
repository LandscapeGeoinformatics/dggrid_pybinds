import sys

from pydggrid.Queries import Transform
from pydggrid.Types import ClipType, InputAddress, DGGSType, PointOutput

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Transform = Transform()
    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 9)
    document.input.points("../DGGRID/examples/transform/inputfiles/20k.txt")
    #
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
# # transform.meta - example of a dggrid meta-file which performs address
# #                  conversion
# #
# # Determine the cells in which some Oregon cities are located in resolution 8
# # an ISEA3H DGGS.
# #
# # Created by Kevin Sahr, November 11, 2001
# # Revised by Kevin Sahr, June 20, 2003
# # Revised by Kevin Sahr, October 20, 2014
# # Revised by Kevin Sahr, November 11, 2014
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
# input_file_name inputfiles/20k.txt
# input_address_type GEO
# input_delimiter " "
#
# # specify the output
# output_file_name outputfiles/cities3h9.txt
# output_address_type SEQNUM
# output_delimiter ","
