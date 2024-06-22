import sys

from pydggrid.Queries import PointPresence
from pydggrid.Types import CellOutput, DGGSType, BinCoverage, PointDataType, OutputAddress, OutputControl

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: PointPresence = PointPresence()

    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 7)
    document.Meta.save("bin_coverage", BinCoverage.PARTIAL)
    document.Meta.save("output_address_type", OutputAddress.SEQNUM)
    document.Meta.save("cell_output_control", OutputControl.OUTPUT_OCCUPIED)
    document.set_input(PointDataType.TEXT, "../DGGRID/examples/binpres/inputfiles/20k.txt")
    document.input.read("../DGGRID/examples/binpres/inputfiles/50k.txt")
    document.input.read("../DGGRID/examples/binpres/inputfiles/100k.txt")
    document.input.read("../DGGRID/examples/binpres/inputfiles/200k.txt")

    print(f"---QUERY REQUEST---\n{document}")
    document.run()
    print("\n---QUERY RESPONSE [POINTS]---\n")
    print(f"COLUMNS: {document.points.get_columns()}\n")
    print(f"---[POINTS (TEXT)]---\n{document.points.get_text()}")
    print(f"---[POINTS (DataFrame)]---\n{document.points.get_frame()}")
    print(f"---[POINTS (GeoDataFrame)]---\n{document.points.get_geoframe()}")
    print(f"---[POINTS (Numpy)]---\n{document.points.get_numpy()}")
    print(f"---[POINTS (XML)]---\n{document.points.get_xml()}")

# ################################################################################
# ################################################################################
# #
# # binpres.meta - example of a dggrid meta-file which performs presence/absence
# #                binning
# #
# # Determine the presence/absence of Oregon cities with various populations in
# # the cells of resolution 7 of an ISEA3H DGGS.
# #
# # Created by Kevin Sahr, November 11, 2001
# # Revised by Kevin Sahr, June 20, 2003
# # Revised by Kevin Sahr, October 20, 2014
# # Revised by Kevin Sahr, November 11, 2014
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation BIN_POINT_PRESENCE
#
# # specify the DGG
# dggs_type ISEA3H
# dggs_res_spec 7
#
# # specify bin controls
# bin_coverage PARTIAL
# input_files inputfiles/20k.txt inputfiles/50k.txt inputfiles/100k.txt inputfiles/200k.txt
# input_delimiter " "
#
# # specify the output
# output_file_name outputfiles/popclass3h7.txt
# output_address_type SEQNUM
# output_delimiter ","
# output_num_classes TRUE
# cell_output_control OUTPUT_OCCUPIED