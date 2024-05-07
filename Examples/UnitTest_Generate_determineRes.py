from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, ResolutionType

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA43H)
    document.Meta.save("dggs_num_aperture_4_res", 2)
    document.Meta.save("dggs_res_specify_type", ResolutionType.CELL_AREA)
    document.Meta.save("dggs_res_specify_area", 120000.0)
    document.Meta.save("dggs_res_specify_rnd_down", True)
    document.Meta.save("cell_output_type", CellOutput.KML)
    document.Meta.save("densification", 1)


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
# # gridgenMixed.meta - example of a DGGRID metafile that generates a grid for
# #     the entire earth with a cell area of approximately 120,000km^2.
# #
# # Kevin Sahr, 01/14/13
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type ISEA43H
# dggs_num_aperture_4_res 2
# dggs_res_specify_type CELL_AREA
# dggs_res_specify_area 120000.0
# dggs_res_specify_rnd_down TRUE
#
# # control the generation
# clip_subset_type WHOLE_EARTH
#
# # specify the output
# cell_output_type KML
# cell_output_file_name outputfiles/earth120k
# densification 1
# precision 6
