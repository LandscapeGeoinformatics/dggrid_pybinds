import sys

from pydggrid.Queries import Generate
from pydggrid.Types import CellOutput, DGGSType, Topology, DGGSProjection, ClipType, Aperture

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", DGGSType.CUSTOM)
    document.Meta.save("dggs_topology", Topology.HEXAGON)
    document.Meta.save("dggs_proj", DGGSProjection.ISEA)
    document.Meta.save("dggs_aperture_type", Aperture.SEQUENCE)
    document.Meta.save("dggs_aperture_sequence", 434747)
    document.Meta.save("geodetic_densify", 0.0)
    document.Meta.save("dggs_res_spec", 5)
    document.run()
    print("\n---QUERY RESPONSE [CELLS]---\n")
    print(f"COLUMNS: {document.cells.get_columns()}\n")
    print(f"---[CELLS (TEXT)]---\n{document.cells.get_aigen()}")
    print(f"---[CELLS (DataFrame)]---\n{document.cells.get_frame()}")
    print(f"---[CELLS (GeoDataFrame)]---\n{document.cells.get_geoframe()}")
    print(f"---[CELLS (Numpy)]---\n{document.cells.get_numpy()}")
    print(f"---[CELLS (XML)]---\n{document.cells.get_kml()}")

# ################################################################################
# #
# # mixedAperture.meta - example of generating a grid with a mixed aperture
# #      sequence, neighbors, and children.
# #
# # Kevin Sahr, 7/14/19
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type CUSTOM
# dggs_topology HEXAGON
# dggs_proj ISEA
# dggs_aperture_type SEQUENCE
# dggs_aperture_sequence 434747
# dggs_res_spec 5
#
# # control the generation
# clip_subset_type WHOLE_EARTH
# geodetic_densify 0.0
#
# # specify the output
# cell_output_type NONE
# point_output_type KML
# point_output_file_name outputfiles/mixedPts
# neighbor_output_type TEXT
# neighbor_output_file_name outputfiles/mixed
# children_output_type TEXT
# children_output_file_name outputfiles/mixed
# densification 0
# precision 5
# verbosity 0