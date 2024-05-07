from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA43H)
    document.Meta.save("dggs_num_aperture_4_res", 6)
    document.Meta.save("dggs_res_spec", 16)
    document.Meta.save("point_output_type", PointOutput.GEOJSON)
    document.Meta.save("cell_output_type", CellOutput.GEOJSON)
    document.Meta.save("geodetic_densify", 0.0)
    document.set_clip(ClipType.SHAPEFILE, "../DGGRID/examples/gridgenGeoJSON/inputfiles/corvallis.shp")


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

# ################################################################################
# #
# # gridgenGeoJSON.meta - example of a DGGRID metafile that generates a high
# #     resolution grid for testing using a mixed aperture ISEA
# #     projection and clipped to a small area in Corvallis, Oregon. The output
# #     grid is in GeoJSON format.
# #
# # Matt Gregory, 11/4/13
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type ISEA43H
# dggs_num_aperture_4_res 6
# dggs_res_spec 16
#
# # control the generation
# clip_subset_type SHAPEFILE
# clip_region_files inputfiles/corvallis
# geodetic_densify 0.0
#
# # specify the output
# cell_output_type GEOJSON
# cell_output_file_name outputfiles/corvallis_cell
# point_output_type GEOJSON
# point_output_file_name outputfiles/corvallis_point
# densification 3
