import sys

from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, LongitudeWrap, GDALFormat

if __name__ == "__main__":
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.PLANETRISK)
    document.Meta.save("dggs_res_spec", 19)
    document.clip_geometry("../DGGRID/examples/planetRiskClipHiRes/inputfiles/AlexandriaOffice.geojson")


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
# # planetRiskClipHiRes.meta - example of a DGGRID metafile that generates a
# #     resolution 19 PlanetRisk grid for a polygon over the Alexandria HQ
# #     of Culmen International.
# #
# # Kevin Sahr, 07/15/19
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify a PLANETRISK grid and resolution (11 is ~1.0 km^2)
# dggs_type PLANETRISK
# # res 19 is ~0.2 m^2 cells
# dggs_res_spec 19
#
# # control grid generation
# clip_subset_type GDAL
# clip_region_files ./inputfiles/AlexandriaOffice.geojson
# # increase granularity of the clipping algorithm for high res
# clipper_scale_factor 1000000000
#
# # specify the output
# cell_output_type KML
# cell_output_file_name ./outputfiles/AlexandriaOfficeCells
# densification 0