import sys

from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()

    document.Meta.save("dggs_type", DGGSType.ISEA3H)
    document.Meta.save("dggs_res_spec", 5)
    document.Meta.save("clip_cell_densification", 1)
    document.Meta.save("precision", 6)
    document.Meta.save("densification", 0)
    document.Meta.save("clip_cell_res", 1)
    document.Meta.save("geodetic_densify", 0.0)
    document.Meta.save("update_frequency", 10000000)
    document.Meta.save("point_output_type", PointOutput.KML)
    document.Meta.save("cell_output_type", CellOutput.KML)

    document.set_clip(ClipType.COARSE_CELLS)
    document.clip.save(list([1, 13, 22]))  # inputfiles/nums1.txt

    print(f"---QUERY REQUEST---\n{document}")
    document.run()
    print("---QUERY RESPONSE [CELLS]---\n")
    print(f"COLUMNS: {document.cells.get_columns()}\n")
    print(f"---[CELLS (TEXT)]---\n{document.cells.get_text()}")
    print(f"---[CELLS (DataFrame)]---\n{document.cells.get_frame()}")
    print(f"---[CELLS (GeoDataFrame)]---\n{document.cells.get_geoframe()}")
    print(f"---[CELLS (Numpy)]---\n{document.cells.get_numpy()}")
    print(f"---[CELLS (XML)]---\n{document.cells.get_xml()}")
    print("\n---QUERY RESPONSE [POINTS]---\n")
    print(f"COLUMNS: {document.points.get_columns()}\n")
    print(f"---[POINTS (TEXT)]---\n{document.points.get_text()}")
    print(f"---[POINTS (DataFrame)]---\n{document.points.get_frame()}")
    print(f"---[POINTS (GeoDataFrame)]---\n{document.points.get_geoframe()}")
    print(f"---[POINTS (Numpy)]---\n{document.points.get_numpy()}")
    print(f"---[POINTS (XML)]---\n{document.points.get_xml()}")

# ################################################################################
# #
# # gridgenCellClip.meta - example of generating part of an ISEA3H grid using
# #      coarser resolution cells as the clipping polygons
# #
# # Kevin Sahr, 1/18/22
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type ISEA3H
# dggs_res_spec 5
#
# # control the generation
# clip_subset_type COARSE_CELLS
# input_address_type SEQNUM
# clip_cell_res 1
# clip_cell_addresses 1 13 22
# clip_cell_densification 1
# geodetic_densify 0.0
#
# # specify the output
# cell_output_type KML
# cell_output_file_name outputfiles/cells
# point_output_type KML
# point_output_file_name outputfiles/points
# densification 0
# precision 6