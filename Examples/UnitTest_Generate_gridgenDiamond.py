from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA4D)
    document.Meta.save("dggs_res_spec", 3)
    document.Meta.save("geodetic_densify", 0.0)

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
# # gridgenDiamond.meta - example of a DGGRID metafile that generates resolution 3
# #     of a diamond grid in KML format.
# #
# # Kevin Sahr, 03/15/21
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type ISEA4D
# dggs_res_spec 3
#
# # control the generation
# clip_subset_type WHOLE_EARTH
# geodetic_densify 0.0
#
# # specify the output
# cell_output_type KML
# cell_output_file_name outputfiles/dmd
# kml_default_color ffff0000
# kml_default_width 6
# kml_name ISEA4D
# kml_description www.discreteglobalgrids.org
# kml_default_width 6
# densification 0
# precision 6
