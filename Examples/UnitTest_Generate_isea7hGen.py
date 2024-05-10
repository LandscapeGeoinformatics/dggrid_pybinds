from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, ResolutionType

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA7H)
    document.Meta.save("dggs_res_spec", 3)
    document.Meta.save("geodetic_densify", 0.0)
    document.Meta.save("cell_output_type", CellOutput.KML)
    document.Meta.save("point_output_type", CellOutput.KML)
    document.Meta.save("kml_default_color", "ff0000ff")
    document.Meta.save("kml_default_width", 2)
    document.Meta.save("densification", 3)


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
# # isea7hGen.meta - example of a DGGRID metafile that generates a
# #     resolution 3 ISEA aperture 7 grid for the whole earth. Output is in
# #     KML format.
# #
# # Kevin Sahr, 08/28/19
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type ISEA7H
# dggs_res_spec 3
#
# # control the generation
# clip_subset_type WHOLE_EARTH
# geodetic_densify 0.0
#
# # specify the output
# cell_output_type KML
# cell_output_file_name outputfiles/isea7h3
# point_output_type KML
# point_output_file_name outputfiles/isea7h3p
# kml_default_width 2
# kml_default_color ff0000ff
# densification 3
# precision 5