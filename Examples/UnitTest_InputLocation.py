from typing import List, Dict, Any

import numpy
import pandas

from pydggrid.Input import Location

if __name__ == "__main__":
    document: Location = Location()
    frame: pandas.DataFrame = pandas.DataFrame({
        "lat": list([4.22, 3.22, 33.22, 21.22]),
        "long": list([5.23, 2.23, 43.22, 12.23]),
        "id": list(range(1, 5)),
        "label": list(["loc1", "loc2", "loc3", "loc4"])
    })
    records: List[Dict[str, Any]] = list([
        {"lat1": 4.14, "lat2": 4.54, "index": 22222, "name": "Void2"},
        {"lat1": 4.14, "lat2": 4.54, "index": 22222, "name": "Void2"},
        {"lat1": 4.14, "lat2": 4.54, "index": 22222, "name": "Void2"}
    ])
    mapping: Dict[str, str] = dict({"lat": "lat1", "long": "lat2", "id": "index", "label": "name" })
    document.insert(3.14, 3.55, 344433, "Void")
    document.save(records[0], mapping)
    document.save(records, mapping)
    document.save(frame)
    document.read("../DGGRID/examples/binpres/inputfiles/20k.txt")
    print(document)