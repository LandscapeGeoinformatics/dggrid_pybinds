from pydggrid.Queries import Generate

if __name__ == "__main__":
    print("---- UnitTest - Meta ----\n")
    query: Generate = Generate()
    query.Meta.save("precision", 8)
    query.Meta.print()
