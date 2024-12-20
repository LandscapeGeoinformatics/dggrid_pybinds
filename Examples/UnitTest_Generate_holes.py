from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, ResolutionType

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 17)
    document.Meta.save("clip_using_holes", True)
    document.Meta.save("geodetic_densify", 0.01)
    document.Meta.save("clipper_scale_factor", 1000000000)
    document.clip_geometry("../DGGRID/examples/holes/inputfiles/holes00.geojson")


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
# # holes.meta - example of a DGGRID metafile that generates a ISEA3H
# #     resolution 17 grid using an input clipping polygon with holes.
# #
# # Kevin Sahr, 06/20/22
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type ISEA3H
# dggs_res_spec 17
#
# # control the generation
# clip_subset_type GDAL
# clip_region_files ./inputfiles/holes00.geojson
# clip_using_holes TRUE
# geodetic_densify 0.01
#
# # specify the output
# cell_output_type KML
# cell_output_file_name ./outputfiles/res17
# densification 1