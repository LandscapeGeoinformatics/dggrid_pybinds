import sys

from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, LongitudeWrap, GDALFormat

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.FULLER43H)
    document.Meta.save("dggs_res_spec", 10)
    document.Meta.save("dggs_num_aperture_4_res", 3)
    document.Meta.save("cell_output_type", CellOutput.SHAPEFILE)
    document.Meta.save("shapefile_id_field_length", 5)
    document.Meta.save("densification", 3)
    document.clip_geometry("../DGGRID/examples/gridgenMixedSHP/inputfiles/benton.gen")

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
# # gridgenMixedSHP.meta - example of a DGGRID metafile that generates a
# #     resolution 10 mixed aperture grid using the Fuller projection and clipped
# #     to Benton County, Oregon. The output grid is in ShapeFile format.
# #
# # Kevin Sahr, 01/14/13
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type FULLER43H
# dggs_num_aperture_4_res 3
# dggs_res_spec 10
#
# # control the generation
# clip_subset_type AIGEN
# clip_region_files inputfiles/benton.gen
#
# geodetic_densify 0.0
#
# # specify the output
# cell_output_type SHAPEFILE
# cell_output_file_name outputfiles/benton10
# shapefile_id_field_length 5
# densification 3
