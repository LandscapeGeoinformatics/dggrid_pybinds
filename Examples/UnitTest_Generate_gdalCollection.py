from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, LongitudeWrap, ChildrenOutput, NeighborOutput

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 2)
    document.Meta.save("unwrap_points", True)
    document.Meta.save("longitude_wrap_mode", LongitudeWrap.UNWRAP_EAST)
    document.Meta.save("point_output_type", PointOutput.GDAL_COLLECTION)
    document.Meta.save("cell_output_type", CellOutput.GDAL_COLLECTION)
    document.set_clip(ClipType.SEQNUMS)
    document.clip.read("../DGGRID/examples/gdalCollection/inputfiles/seqnums.txt")

    # parameters["dggrid_operation"] = "GENERATE_GRID";
    #     parameters["dggs_type"] = "ISEA3H";
    #     parameters["dggs_res_spec"] = "2";
    #     parameters["unwrap_points"] = "true";
    #     parameters["clip_subset_type"] = "SEQNUMS";
    #     parameters["longitude_wrap_mode"] = "UNWRAP_EAST";
    #     parameters["point_output_type"] = "GDAL_COLLECTION";
    #     parameters["cell_output_type"] = "GDAL_COLLECTION";
    #     parameters["children_output_type"] = "GDAL_COLLECTION";
    #     parameters["neighbor_output_type"] = "GDAL_COLLECTION";
    #     parameters["collection_output_gdal_format"] = "geojson";


    print(f"---QUERY REQUEST---\n{document}")
    document.run()
    print("---QUERY RESPONSE [CELLS]---\n")
    print(f"COLUMNS: {document.cells.get_columns()}\n")
    print(f"---[CELLS (TEXT)]---\n{document.cells.get_text()}")
    print(f"---[CELLS (DataFrame)]---\n{document.cells.get_frame()}")
    print(f"---[CELLS (GeoDataFrame)]---\n{document.cells.get_geoframe()}")
    print(f"---[CELLS (Numpy)]---\n{document.cells.get_numpy()}")
    print("\n---QUERY RESPONSE [POINTS]---\n")
    print(f"COLUMNS: {document.points.get_columns()}\n")
    print(f"---[POINTS (TEXT)]---\n{document.points.get_text()}")
    print(f"---[POINTS (DataFrame)]---\n{document.points.get_frame()}")
    print(f"---[POINTS (GeoDataFrame)]---\n{document.points.get_geoframe()}")
    print(f"---[POINTS (Numpy)]---\n{document.points.get_numpy()}")
    print("\n---QUERY RESPONSE [COLLECTION]---\n")
    print(f"COLUMNS: {document.collection.get_columns()}\n")
    print(f"---[COLLECTION (TEXT)]---\n{document.collection.get_text()}")
    print(f"---[COLLECTION (DataFrame)]---\n{document.collection.get_frame()}")
    print(f"---[COLLECTION (GeoDataFrame)]---\n{document.collection.get_geoframe()}")
    print(f"---[COLLECTION (Numpy)]---\n{document.collection.get_numpy()}")

# ################################################################################
# #
# # gdalCollection.meta - example of a DGGRID metafile that combines all data for
# #     each cell into a single file.
# #
# # Kevin Sahr, 02/08/22
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
