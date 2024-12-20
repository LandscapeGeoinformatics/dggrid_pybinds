import sys

from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, LongitudeWrap, GDALFormat

if __name__ == "__main__":

    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.PLANETRISK)
    document.Meta.save("dggs_res_spec", 5)
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
# # planetRiskGridGen.meta - example of generating a PlanetRisk grid with
# #      neighbors and children.
# #
# # Kevin Sahr, 7/14/19
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type PLANETRISK
# dggs_res_spec 5
#
# # control the generation
# clip_subset_type WHOLE_EARTH
# geodetic_densify 0.0
#
# # specify the output using GDAL-supported file formats
# cell_output_type GDAL
# cell_output_gdal_format GeoJSON
# cell_output_file_name outputfiles/cells.geojson
# point_output_type GDAL
# point_output_gdal_format GeoJSON
# point_output_file_name outputfiles/points.geojson
# neighbor_output_type TEXT
# neighbor_output_file_name outputfiles/neighbors
# children_output_type TEXT
# children_output_file_name outputfiles/children
# densification 0
# precision 6