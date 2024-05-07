from pydggrid.Input import ShapeFile

if __name__ == "__main__":
    print("---- UnitTest - Input ShapeFile ----\n")
    document: ShapeFile = ShapeFile()
    document.save("../DGGRID/examples/aigenerate/inputfiles/orbuff.shp")
    print(document)
