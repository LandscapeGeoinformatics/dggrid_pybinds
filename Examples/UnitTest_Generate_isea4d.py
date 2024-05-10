from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, ResolutionType

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA4D)
    document.Meta.save("dggs_res_spec", 7)
    document.Meta.save("cell_output_type", CellOutput.KML)
    document.set_clip(ClipType.SHAPEFILE, "../DGGRID/examples/isea4d/inputfiles/orbuff.shp")


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

# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify an ISEA4D DGG; override the default resolution
# dggs_type ISEA4D
# dggs_res_spec 7
#
# # control grid generation
# clip_subset_type SHAPEFILE
# clip_region_files ./inputfiles/orbuff.shp
#
# # specify the output
# cell_output_type KML
# cell_output_file_name ./outputfiles/orgrid
# densification 3