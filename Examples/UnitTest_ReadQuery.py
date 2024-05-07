from pydggrid.Queries import Generate
from pydggrid.Types import ClipType

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", "ISEA3H")
    document.Meta.save("dggs_res_spec", 6)
    document.Meta.save("update_frequency", 10000000)
    document.set_clip(ClipType.SHAPEFILE, "../DGGRID/examples/aigenerate/inputfiles/orbuff.shp")
    # # specify the operation
    # dggrid_operation GENERATE_GRID
    #
    # # specify a ISEA3H; override the default resolution
    # dggs_type ISEA3H
    # dggs_res_spec 6
    #
    # # control grid generation
    # clip_subset_type SHAPEFILE
    # clip_region_files ./inputfiles/orbuff.shp
    # update_frequency 10000000
    #
    # # specify the output
    # cell_output_type AIGEN
    # cell_output_file_name ./outputfiles/orCells
    # densification 5
    #
    # point_output_type AIGEN
    # point_output_file_name ./outputfiles/orPts
    print(f"---QUERY REQUEST---\n{document}")
    print(f"\n--PYBINDS TEST RESPONSE--\n{document.UnitTest_ReadQuery()}")
