import sys

from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, InputAddress, CellLabel, OutputAddress

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 2)
    document.clip_cells("../DGGRID/examples/z3Collection/inputfiles/seqnums.txt", cell_type=InputAddress.Z3)
    document.cell_type(OutputAddress.Z3)
    document.set_collection(True)
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
    print("\n---QUERY RESPONSE [COLLECTION]---\n")
    print(f"COLUMNS: {document.collection.get_columns()}\n")
    print(f"---[COLLECTION (TEXT)]---\n{document.collection.get_aigen()}")
    print(f"---[COLLECTION (DataFrame)]---\n{document.collection.get_frame()}")
    print(f"---[COLLECTION (GeoDataFrame)]---\n{document.collection.get_geoframe()}")
    print(f"---[COLLECTION (Numpy)]---\n{document.collection.get_numpy()}")


# ################################################################################
# #
# # z3Collection.meta - example of a DGGRID metafile that outputs to a GDAL
# #     collection file using Z3 cell indexes.
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type ISEA3H
# dggs_res_spec 2
#
# # control grid generation
# clip_subset_type SEQNUMS
# clip_region_files inputfiles/seqnums.txt
# longitude_wrap_mode UNWRAP_EAST
# unwrap_points TRUE
#
# # specify output address information
# output_cell_label_type OUTPUT_ADDRESS_TYPE
# output_address_type Z3
#
# # specify the output collection file used
# # when GDAL_COLLECTION is specified below
# collection_output_gdal_format GeoJSON
# collection_output_file_name ./outputfiles/everything.geojson
#
# # specify which output you want to put together in a GDAL_COLLECTION
# # this must include cell and/or point output
# cell_output_type GDAL_COLLECTION
# point_output_type GDAL_COLLECTION
# children_output_type GDAL_COLLECTION
# neighbor_output_type GDAL_COLLECTION