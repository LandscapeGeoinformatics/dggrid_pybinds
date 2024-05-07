from pydggrid.Queries import Generate

if __name__ == "__main__":
    #
    document: Generate = Generate()
    print("-> READ PAYLOAD")
    print(f"---QUERY REQUEST---\n{document}")
    print(f"\n--PYBINDS TEST RESPONSE--\n{document.UnitTest_ReadPayload()}")
