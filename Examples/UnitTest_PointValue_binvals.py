import sys

from pydggrid.Queries import PointValue
from pydggrid.Types import CellOutput, DGGSType, BinCoverage, PointDataType, OutputAddress, OutputControl

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: PointValue = PointValue()
    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 9)
    document.Meta.save("bin_coverage", BinCoverage.PARTIAL)
    document.Meta.save("output_address_type", OutputAddress.SEQNUM)
    document.Meta.save("cell_output_control", OutputControl.OUTPUT_OCCUPIED)
    document.input.points("../DGGRID/examples/binvals/inputfiles/20k.txt")
    document.input.points("../DGGRID/examples/binvals/inputfiles/50k.txt")
    document.input.points("../DGGRID/examples/binvals/inputfiles/100k.txt")
    document.input.points("../DGGRID/examples/binvals/inputfiles/200k.txt")

    print(f"---QUERY REQUEST---\n{document}")
    document.run()
    print("\n---QUERY RESPONSE [RECORDS]---\n")
    print(f"COLUMNS: {document.records.get_columns()}\n")
    print(f"---[RECORDS (DataFrame)]---\n{document.records.get_frame()}")
    print(f"---[RECORDS (GeoDataFrame)]---\n{document.records.get_geoframe()}")
    print(f"---[RECORDS (Numpy)]---\n{document.records.get_numpy()}")

# ################################################################################
# ################################################################################
# #
# # binvals.meta - example of a dggrid meta-file which performs point value
# #                binning
# #
# # Determine the average population of large Oregon cities in the cells of
# # resolution 9 of an ISEA3H DGGS.
# #
# # Created by Kevin Sahr, November 11, 2001
# # Revised by Kevin Sahr, June 20, 2003
# # Revised by Kevin Sahr, October 20, 2014
# # Revised by Kevin Sahr, November 11, 2014
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation BIN_POINT_VALS
#
# # specify the DGG
#
# dggs_type ISEA3H
# dggs_res_spec 9
#
# # specify bin controls
#
# bin_coverage PARTIAL
# input_files inputfiles/20k.txt inputfiles/50k.txt inputfiles/100k.txt inputfiles/200k.txt
# input_delimiter " "
#
# # specify text file output
# output_file_type TEXT
# output_file_name outputfiles/popval3h9.txt
# output_address_type SEQNUM
# output_delimiter ","
# precision 7
# cell_output_control OUTPUT_OCCUPIED