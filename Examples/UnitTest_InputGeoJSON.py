from pydggrid.Input import GeoJSON

if __name__ == "__main__":
    print("---- UnitTest - Input GeoJSON ----\n")
    document: GeoJSON = GeoJSON()
    document.save("../DGGRID/examples/planetRiskClipHiRes/inputfiles/AlexandriaOffice.geojson")
    document.save("../DGGRID/examples/planetRiskClipHiRes/inputfiles/culmenUSA.geojson")
    print(document)
