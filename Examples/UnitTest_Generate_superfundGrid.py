from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.SUPERFUND)
    document.Meta.save("dggs_res_spec", 5)
    document.clip_geometry("../DGGRID/examples/superfundGrid/inputfiles/orbuff.shp")

    print(f"---QUERY REQUEST---\n{document}")
    document.run()
    print("---QUERY RESPONSE [CELLS]---\n")
    print(f"COLUMNS: {document.cells.get_columns()}\n")
    print(f"---[CELLS (TEXT)]---\n{document.cells.get_aigen()}")
    print(f"---[CELLS (DataFrame)]---\n{document.cells.get_frame()}")
    print(f"---[CELLS (GeoDataFrame)]---\n{document.cells.get_geoframe()}")
    print(f"---[CELLS (Numpy)]---\n{document.cells.get_numpy()}")
    print(f"---[CELLS (XML)]---\n{document.cells.get_kml()}")
    print("\n---QUERY RESPONSE [POINTS]---\n")
    print(f"COLUMNS: {document.points.get_columns()}\n")
    print(f"---[POINTS (TEXT)]---\n{document.points.get_aigen()}")
    print(f"---[POINTS (DataFrame)]---\n{document.points.get_frame()}")
    print(f"---[POINTS (GeoDataFrame)]---\n{document.points.get_geoframe()}")
    print(f"---[POINTS (Numpy)]---\n{document.points.get_numpy()}")
    print(f"---[POINTS (XML)]---\n{document.points.get_kml()}")

# ################################################################################
# #
# # superfundGrid.meta - example of a DGGRID metafile that generates a resolution
# #     5 Superfund_500m grid for the state of Oregon (with a 100 mile buffer);
# #     also demonstrates breaking up output into multiple files
# #
# # Kevin Sahr, 01/14/13
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify a Superfund_500m DGG; override the default resolution
# dggs_type SUPERFUND
# dggs_res_spec 5
#
# # control grid generation
# clip_subset_type SHAPEFILE
# clip_region_files ./inputfiles/orbuff.shp
# update_frequency 10000000
#
# # specify the output
# cell_output_type SHAPEFILE
# cell_output_file_name ./outputfiles/orgrid
# densification 3
# max_cells_per_output_file 500