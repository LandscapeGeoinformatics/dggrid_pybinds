import sys

from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput, LongitudeWrap, GDALFormat

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.ISEA7H)
    document.Meta.save("dggs_res_spec", 9)
    document.Meta.save("point_output_type", PointOutput.GDAL)
    document.Meta.save("cell_output_type", CellOutput.GDAL)
    document.Meta.save("cell_output_gdal_format", GDALFormat.KML)
    document.set_clip(ClipType.GDAL)
    document.clip.shape_file("../DGGRID/examples/gdalExample/inputfiles/corvallis.shp")


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
# # gdalExample.meta - example of a DGGRID metafile that generates a resolution
# #     9 ISEA7H grid. The clipping and output files all use GDAL-readable file
# #     formats.
# #
# # Kevin Sahr, 08/29/19
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type ISEA7H
# dggs_res_spec 9
#
# # control grid generation
# clip_subset_type GDAL
# # gdal uses the file extension to determine the file format
# clip_region_files inputfiles/corvallis.shp
#
# # specify the output
# cell_output_type GDAL
# # for output the format needs to be explicit
# cell_output_gdal_format KML
# cell_output_file_name ./outputfiles/corvallisCells.kml
#
# point_output_type GDAL
# point_output_gdal_format GeoJSON
# point_output_file_name ./outputfiles/corvallisPts.geojson
