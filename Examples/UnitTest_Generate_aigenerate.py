from pydggrid.Queries import Generate
from pydggrid.Types import ClipType, CellOutput, PointOutput

if __name__ == "__main__":
    #
    print("-> READ QUERY")
    document: Generate = Generate()
    document.Meta.save("dggs_type", "ISEA3H")
    document.Meta.save("dggs_res_spec", 6)
    document.Meta.save("update_frequency", 10000000)
    document.clip_geometry("../DGGRID/examples/aigenerate/inputfiles/orbuff.shp")

    print(f"---QUERY REQUEST---\n{document}")
    document.run()
    print("---QUERY RESPONSE [CELLS]---\n")
    print(f"COLUMNS: {document.cells.get_columns()}\n")
    print(f"---[CELLS (TEXT)]---\n{document.cells.get_aigen()}")
    print(f"---[CELLS (DataFrame)]---\n{document.cells.get_frame()}")
    print(f"---[CELLS (GeoDataFrame)]---\n{document.cells.get_geoframe()}")
    print(f"---[CELLS (GeoArrow)]---\n{document.cells.get_arrow()}")
    print(f"---[CELLS (Numpy)]---\n{document.cells.get_numpy()}")
    print(f"---[CELLS (XML)]---\n{document.cells.get_kml()}")
    print("\n---QUERY RESPONSE [POINTS]---\n")
    print(f"COLUMNS: {document.points.get_columns()}\n")
    print(f"---[POINTS (TEXT)]---\n{document.points.get_aigen()}")
    print(f"---[POINTS (DataFrame)]---\n{document.points.get_frame()}")
    print(f"---[POINTS (GeoDataFrame)]---\n{document.points.get_geoframe()}")
    print(f"---[POINTS (GeoArrow)]---\n{document.points.get_arrow()}")
    print(f"---[POINTS (Numpy)]---\n{document.points.get_numpy()}")
    print(f"---[POINTS (XML)]---\n{document.points.get_kml()}")

