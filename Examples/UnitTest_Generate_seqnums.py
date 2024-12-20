from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, DGGSType, PointOutput

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()

    document.Meta.save("dggs_type", DGGSType.ISEA7H)
    document.Meta.save("dggs_res_spec", 5)
    document.Meta.save("update_frequency", 10000000)
    document.clip_cells(list([4, 3, 4, 3, 3]))  # inputfiles/nums1.txt
    document.clip_cells(list([5, 3, 3, 7, 4, 8]))  # inputfiles/nums2.txt

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
# # seqnums.meta - example of a DGGRID metafile that generates kml cells for a
# #     resolution 5 ISEA7H grid for sequence numbers specified in a text file.
# #
# # Kevin Sahr, 01/10/24
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify a ISEA3H; override the default resolution
# dggs_type ISEA7H
# dggs_res_spec 5
#
# # control grid generation
# clip_subset_type SEQNUMS
# clip_region_files inputfiles/nums1.txt inputfiles/nums2.txt inputfiles/nums3.txt
#
# # specify the output
# cell_output_type KML
# cell_output_file_name ./outputfiles/seqcells
# point_output_type KML
# point_output_file_name ./outputfiles/seqpts
# densification 3
