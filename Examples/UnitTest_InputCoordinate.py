from typing import List, Dict
import pandas

from pydggrid.Input import Coordinate

if __name__ == "__main__":
    document: Coordinate = Coordinate()
    frame: pandas.DataFrame = pandas.DataFrame({
        "lat": list([4.22, 3.22, 33.22, 21.22]),
        "long": list([5.23, 2.23, 43.22, 12.23])
    })
    records: List[Dict[str, float]] = list([
        {"lat1": 4.14, "lat2": 4.54},
        {"lat1": 4.14, "lat2": 4.54},
        {"lat1": 4.14, "lat2": 4.54}
    ])
    mapping: Dict[str, str] = dict({"lat": "lat1", "long": "lat2"})
    document.insert(3.14, 3.55)
    document.save(records[0], mapping)
    document.save(records, mapping)
    document.save(frame)
    document.read("../DGGRID/examples/z3Transform/inputfiles/geo.txt")
    print(document)