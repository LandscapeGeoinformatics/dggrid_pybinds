from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, ResolutionType, OrientationType

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 3)
    document.Meta.save("dggs_num_placements", 4)
    document.Meta.save("dggs_orient_specify_type", OrientationType.RANDOM)
    document.Meta.save("dggs_orient_rand_seed", 1013)
    document.Meta.save("cell_output_type", CellOutput.KML)
    document.Meta.save("point_output_type", CellOutput.KML)
    document.Meta.save("kml_default_width", 2)
    document.Meta.save("kml_default_color", "ff0000ff")

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
    print(f"\n\n--META--{document.dgg_meta}")

# ################################################################################
# #
# # multipleOrientations.meta - example of a DGGRID metafile that generates
# #     multiple orientations of a resolution 2 ISEA aperture 3 grid. The whole
# #     earth is output in KML format. Each output file contains a maximum of
# #     50 cells.
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
# # control the generation
# clip_subset_type WHOLE_EARTH
# geodetic_densify 0.0
#
# # create four orientations randomly
# dggs_num_placements 4
# dggs_orient_specify_type RANDOM
# dggs_orient_rand_seed 1013
# dggs_orient_output_file_name outputfiles/isea3h2.meta
#
# # specify the output
# max_cells_per_output_file 50
# cell_output_type KML
# cell_output_file_name outputfiles/isea3h2
# point_output_type KML
# point_output_file_name outputfiles/isea3h2p
# kml_default_width 2
# kml_default_color ff0000ff
# precision 5