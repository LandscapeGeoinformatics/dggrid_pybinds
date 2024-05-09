from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, ResolutionType

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA43H)
    document.Meta.save("dggs_res_spec", 27)
    document.Meta.save("dggs_num_aperture_4_res", 20)
    document.Meta.save("geodetic_densify", 0.0)
    document.Meta.save("clipper_scale_factor", 1000000000)
    document.Meta.save("cell_output_type", CellOutput.SHAPEFILE)
    document.Meta.save("densification", 3)
    document.Meta.save("shapefile_id_field_length", 21)
    document.Meta.save("precision", 12)
    document.set_clip(ClipType.SHAPEFILE)
    document.clip.read("../DGGRID/examples/hiRes/inputfiles/littleTri.shp")


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
# # hiRes.meta - example of a DGGRID metafile that generates a very high
# #     resolution grid (cell area of less than 3 square cm) using a mixed
# #     aperture ISEA projection and clipped to a small triangle in Ashland, Oregon.
# #
# # NOTES:
# #
# #   - this metafile causes DGGRID to generate a warning indicating that the
# #     number of cells may cause an integer overflow for some operations; this
# #     message should not stop DGGRID from generating portions of the grid
# #
# # Kevin Sahr, 09/01/18
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type ISEA43H
# dggs_num_aperture_4_res 20
# dggs_res_spec 27
#
# # control the generation
# clip_subset_type SHAPEFILE
# clip_region_files inputfiles/littleTri
# geodetic_densify 0.0
# clipper_scale_factor 1000000000
#
# # specify the output
# cell_output_type SHAPEFILE
# cell_output_file_name outputfiles/littleTri31
# densification 3
# shapefile_id_field_length 21
# precision 12