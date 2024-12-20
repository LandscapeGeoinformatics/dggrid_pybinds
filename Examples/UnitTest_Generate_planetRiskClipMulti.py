import sys

from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, LongitudeWrap, GDALFormat

if __name__ == "__main__":

    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.PLANETRISK)
    document.Meta.save("dggs_res_spec", 14)
    document.clip_geometry("../DGGRID/examples/planetRiskClipMulti/inputfiles/WashingtonDC.geojson")
    document.clip_geometry("../DGGRID/examples/planetRiskClipMulti/inputfiles/culmenUSA.geojson")


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
# # planetRiskClipMulti.meta - example of a DGGRID metafile that generates a resolution
# #     14 PlanetRisk grid for a polygons over the Alexandria and Tysons
# #     Corner offices of Culmen International, the White House, the Reflecting
# #     Pool, and the Pentagon.
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
# dggs_res_spec 14
#
# # control grid generation
# clip_subset_type GDAL
# clip_region_files ./inputfiles/WashingtonDC.geojson ./inputfiles/culmenUSA.geojson
#
# # specify the output
# cell_output_type KML
# cell_output_file_name ./outputfiles/culmenCells
# densification 0
#
# # output neighbors and children
# neighbor_output_type TEXT
# neighbor_output_file_name outputfiles/neighbors
# children_output_type TEXT
# children_output_file_name outputfiles/children