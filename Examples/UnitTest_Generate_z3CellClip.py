import sys

from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, InputAddress, CellLabel, OutputAddress

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 5)
    document.Meta.save("clip_cell_res", 1)
    document.Meta.save("geodetic_densify", 0.0)
    document.clip_cells(list([2000000000000000, 3800000000000000, 1800000000000000]), cell_type=InputAddress.Z3)
    document.cell_type(OutputAddress.Z3)

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
# # z3CellClip.meta - example of generating part of an ISEA3H grid using
# #      coarser resolution cells specified as Z3 indexes as the
# #      clipping polygons
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type ISEA3H
# dggs_res_spec 5
#
# # control the generation
# clip_subset_type COARSE_CELLS
# input_address_type Z3
# clip_cell_res 1
# clip_cell_addresses 2000000000000000 3800000000000000 1800000000000000
#
# clip_cell_densification 1
# geodetic_densify 0.0
#
# # specify the output
#
# output_cell_label_type OUTPUT_ADDRESS_TYPE
# output_address_type Z3
#
# cell_output_type KML
# cell_output_file_name outputfiles/cells
# point_output_type KML
# point_output_file_name outputfiles/points
# densification 0
# precision 6