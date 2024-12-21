import sys

from pydggrid.Queries import Statistics
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, LongitudeWrap

if __name__ == "__main__":

    print("-> READ QUERY")
    document: Statistics = Statistics()
    document.Meta.save("dggs_type", DGGSType.PLANETRISK)
    document.Meta.save("dggs_res_spec", 20)
    #
    print(f"---QUERY REQUEST---\n{document}")
    document.run()
    print("---QUERY RESPONSE [RECORDS]---\n")
    print(f"COLUMNS: {document.records.get_columns()}\n")
    print(f"---[RECORDS (DataFrame)]---\n{document.records.get_frame()}")
    print(f"---[RECORDS (GeoDataFrame)]---\n{document.records.get_geoframe()}")
    print(f"---[RECORDS (Numpy)]---\n{document.records.get_numpy()}")

# ################################################################################
# #
# # planetRiskTable.meta - example of outputting a table of statistics for the
# #      first 20 resolutions of the PlanetRisk grid.
# #
# # Kevin Sahr, 7/14/19
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation OUTPUT_STATS
#
# # specify the DGG
# dggs_type PLANETRISK
# dggs_res_spec 20