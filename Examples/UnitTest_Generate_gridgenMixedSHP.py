import sys

from pydggrid.Queries import Generate
from pydggrid.Types import CellOutput, DGGSType, BinCoverage, PointDataType, ClipType, OutputControl

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.FULLER43H)
    document.Meta.save("dggs_num_aperture_4_res", 3)
    document.Meta.save("dggs_res_spec", 10)
    document.Meta.save("cell_output_type", CellOutput.GDAL)
    document.clip_geometry("../DGGRID/examples/gridgenMixedSHP/inputfiles/benton.gen")
    #
    document.run()
    print("\n---QUERY RESPONSE [CELLS]---\n")
    print(f"COLUMNS: {document.cells.get_columns()}\n")
    print(f"---[CELLS (TEXT)]---\n{document.cells.get_aigen()}")
    print(f"---[CELLS (DataFrame)]---\n{document.cells.get_frame()}")
    print(f"---[CELLS (GeoDataFrame)]---\n{document.cells.get_geoframe()}")
    print(f"---[CELLS (Numpy)]---\n{document.cells.get_numpy()}")
    print(f"---[CELLS (XML)]---\n{document.cells.get_kml()}")

#
# specify the operation
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
