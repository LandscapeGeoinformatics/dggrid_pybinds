import numpy
import pandas

from pydggrid.Input import Sequence

if __name__ == "__main__":
    frame: pandas.DataFrame = pandas.DataFrame({
        "column1": list(range(1, 20, 1)),
        "column2": list(range(21, 40, 1)),
    })
    array: numpy.ndarray = numpy.array([[44, 45, 46], [54, 55, 56]])

    document: Sequence = Sequence()
    document.save(list([1, 2, 3, 4, 5]))
    document.save(tuple((1, 10, 1)))
    document.save(frame, "column2")
    document.save(array, 1)
    document.read("../DGGRID/examples/gdalCollection/inputfiles/seqnums.txt")
    print(document)