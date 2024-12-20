import sys

from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, LongitudeWrap, DGGSType, PointOutput, InputAddress, CellLabel, OutputAddress

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 4)
    document.Meta.save("longitude_wrap_mode", LongitudeWrap.UNWRAP_EAST)
    document.clip_cells("../DGGRID/examples/zNums/inputfiles/zorder1.txt", cell_type=InputAddress.ZORDER)
    document.clip_cells("../DGGRID/examples/zNums/inputfiles/zorder2.txt", cell_type=InputAddress.ZORDER)
    document.cell_type(OutputAddress.ZORDER)
    #
    print(f"---QUERY REQUEST---\n{document}")
    document.run()
    print("---QUERY RESPONSE [CELLS]---\n")
    print(f"COLUMNS: {document.cells.get_columns()}\n")
    print(f"---[CELLS (TEXT)]---\n{document.cells.get_aigen()}")
    print(f"---[CELLS (DataFrame)]---\n{document.cells.get_frame()}")
    print(f"---[CELLS (GeoDataFrame)]---\n{document.cells.get_geoframe()}")
    print(f"---[CELLS (Numpy)]---\n{document.cells.get_numpy()}")
    print("\n---QUERY RESPONSE [POINTS]---\n")
    print(f"COLUMNS: {document.points.get_columns()}\n")
    print(f"---[POINTS (TEXT)]---\n{document.points.get_aigen()}")
    print(f"---[POINTS (DataFrame)]---\n{document.points.get_frame()}")
    print(f"---[POINTS (GeoDataFrame)]---\n{document.points.get_geoframe()}")
    print(f"---[POINTS (Numpy)]---\n{document.points.get_numpy()}")


# ################################################################################
# #
# # zNums.meta - example of a DGGRID metafile that generates kml cells for a
# #     resolution 4 ISEA3H grid for zorder indexes specified in text files.
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify a ISEA3H; override the default resolution
# dggs_type ISEA3H
# dggs_res_spec 4
#
# # control grid generation
# clip_subset_type INPUT_ADDRESS_TYPE
# input_address_type ZORDER
# clip_region_files inputfiles/zorder1.txt inputfiles/zorder2.txt
#
# # specify output address information
# output_cell_label_type OUTPUT_ADDRESS_TYPE
# output_address_type ZORDER
#
# # specify the output
# cell_output_type KML
# cell_output_file_name ./outputfiles/zcells
# densification 3