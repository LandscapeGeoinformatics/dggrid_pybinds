from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, InputAddress, CellLabel, OutputAddress

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA7H)
    document.Meta.save("dggs_res_spec", 5)
    document.clip_cells("/opt/source/ut/DGGRID/examples/z7Nums/inputfiles/z7a.txt", cell_type=InputAddress.Z7)
    document.clip_cells("/opt/source/ut/DGGRID/examples/z7Nums/inputfiles/z7b.txt", cell_type=InputAddress.Z7)
    document.cell_type(OutputAddress.Z7_STRING)

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
# # z7Nums.meta - example of a DGGRID metafile that generates kml cells for a
# #     resolution 5 ISEA7H grid for Z7 indexes specified in text files.
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify a ISEA7H; override the default resolution
# dggs_type ISEA7H
# dggs_res_spec 5
#
# # control grid generation
# clip_subset_type INPUT_ADDRESS_TYPE
# input_address_type Z7
# clip_region_files inputfiles/z7a.txt inputfiles/z7b.txt
#
# # specify output address information
# output_cell_label_type OUTPUT_ADDRESS_TYPE
# output_address_type Z7_STRING
#
# # specify the output
# cell_output_type KML
# cell_output_file_name ./outputfiles/zcells
# point_output_type KML
# point_output_file_name ./outputfiles/zpoints
