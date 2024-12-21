from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, InputAddress, CellLabel, OutputAddress

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 9)
    document.Meta.save("geodetic_densify", 0.0)
    document.Meta.save("input_address_type", InputAddress.Z3)
    document.clip_cells(list(["1260240000000000",
                              "1216840000000000",
                              "1216840000000000",
                              "1216840000000000",
                              "1214680000000000",
                              "1216500000000000",
                              "1260a40000000000"]),
                        address_type=InputAddress.Z3)
    document.clip_cells(list(["1100000000000000",
                              "1010000000000000",
                              "1010000000000000",
                              "1120000000000000",
                              "1020000000000000",
                              "1200000000000000"]),
                        address_type=InputAddress.Z3)
    document.address_type(OutputAddress.Z3)

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

###############################################################################
# # z3Nums.meta - example of a DGGRID metafile that generates kml cells for a
# #     resolution 4 ISEA3H grid for Z3 indexes specified in text files.
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify a ISEA3H; override the default resolution
# dggs_type ISEA3H
# dggs_res_spec 9
#
# # control grid generation
# clip_subset_type INPUT_ADDRESS_TYPE
# input_address_type Z3
# clip_region_files inputfiles/z3a.txt inputfiles/z3b.txt
#
# # specify output address information
# output_cell_label_type OUTPUT_ADDRESS_TYPE
# output_address_type Z3
#
# # specify the output
# cell_output_type KML
# cell_output_file_name ./outputfiles/zcells
# point_output_type KML
# point_output_file_name ./outputfiles/zpoints
