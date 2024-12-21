import sys

from pydggrid.Queries import Transform
from pydggrid.Types import ClipType, InputAddress, DGGSType, PointOutput,OutputAddress

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Transform = Transform()
    document.Meta.save("dggs_type", DGGSType.ISEA7H)
    document.Meta.save("dggs_res_spec", 9)
    document.Meta.save("output_address_type", OutputAddress.Z7_STRING)
    document.input_cells("../DGGRID/examples/z7Transform/inputfiles/seqNum.txt")
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
# # z7Transform.meta - example of a dggrid meta-file which performs address
# #                   conversion from SEQNUM to Z7_STRING indexes
# #
# # Note that the inputfiles directory contains GEO, Z7, Z7_STRING, and
# # SEQNUM files, all describing the same set of cells. You can experiment with
# # transforming between these by changing the input_* (and output_*) parameters.
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation TRANSFORM_POINTS
#
# # specify the DGG
# dggs_type ISEA7H
# dggs_res_spec 9
#
# # specify bin controls
# input_file_name inputfiles/seqNum.txt
# input_address_type SEQNUM
# input_delimiter " "
#
# # specify the output
# output_file_name outputfiles/z7str.txt
# output_address_type Z7_STRING
# output_delimiter " "