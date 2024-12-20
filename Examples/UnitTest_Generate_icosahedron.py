from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, ResolutionType

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.FULLER4T)
    document.Meta.save("dggs_res_spec", 0)
    document.Meta.save("geodetic_densify", 0.0)
    document.Meta.save("kml_default_color", "ffff0000")
    document.Meta.save("kml_default_width", 6)
    document.Meta.save("kml_name", "Spherical Icosahedron")
    document.Meta.save("kml_description", "www.discreteglobalgrids.org")


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
# # icosahedron.meta - example of a DGGRID metafile that generates a spherical
# #     icosahedron (a resolution 0 triangle grid) in KML format.
# #
# # Kevin Sahr, 10/23/14
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type FULLER4T
# dggs_res_spec 0
#
# # control the generation
# clip_subset_type WHOLE_EARTH
# geodetic_densify 0.0
#
# # specify the output
# cell_output_type KML
# cell_output_file_name outputfiles/icosa
# kml_default_color ffff0000
# kml_default_width 6
# kml_name Spherical Icosahedron
# kml_description www.discreteglobalgrids.org
# kml_default_width 6
# densification 0