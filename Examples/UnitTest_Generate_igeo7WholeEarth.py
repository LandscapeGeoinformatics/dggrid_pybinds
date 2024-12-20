from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, ResolutionType

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.IGEO7)
    document.Meta.save("dggs_res_spec", 3)
    document.Meta.save("precision", 6)
    document.Meta.save("densification", 0)


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
# # igeo7WholeEarth.meta - example of generating a whole earth igeo7 DGG res 3.
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type IGEO7
# dggs_res_spec 3
#
# # specify the output
# # igeo7 DGGS preset has Z7 for input and output
# # and sets output_cell_label_type to OUTPUT_ADDRESS_TYPE
# cell_output_type KML
# cell_output_file_name outputfiles/igeo7cells
# point_output_type KML
# point_output_file_name outputfiles/igeo7pts
# densification 0
# precision 6
# kml_default_color ffff0000
# kml_name igeo7 Res 3
# kml_description www.discreteglobalgrids.org
# kml_default_width 3