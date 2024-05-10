#include "library.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

int add(int i, int j)
{
    return i + j;
}

/**
 * Converts python bytes object into unsigned char vector
 * @param bytes Pybinds11 Bytes Object
 * @return unsigned char array vector
 */
std::vector<unsigned char>
PyDGGRID_readBytesToUCVector(const std::vector<unsigned int>& bytes)
{
    std::vector<unsigned char> blocks;
    blocks.resize(bytes.size());
    blocks.assign(bytes.begin(), bytes.end());
    return blocks;
}

/**
 * Converts python bytes object into unsigned char vector
 * @param bytes Pybinds11 Bytes Object
 * @return unsigned char array vector
 */
std::vector<unsigned int>
PyDGGRID_readBytesToInt64Vector(const std::vector<unsigned char>& bytes)
{
    std::vector<unsigned int> blocks;
    blocks.resize(bytes.size());
    blocks.assign(bytes.begin(), bytes.end());
    return blocks;
}

/**
 * Reads python dict into a std::map
 * @param dictionary Pyhbinds11 dict variable
 * @return {string, string} std::map object
 */
std::map<std::string, std::string>
PyDGGRID_readDictionaryToMap(const pybind11::dict &dictionary)
{
    std::map<std::string, std::string> elements;
    for (std::pair<pybind11::handle, pybind11::handle> item : dictionary)
        { elements[item.first.cast<std::string>()] = item.second.cast<std::string>(); }
    return elements;
}
/**
 * Converts pybind bytes to unsigned char array
 * @param bytes Python bytes object
 * @return Bytes Vector
 */
std::vector<unsigned char > DGGrid_ConvertBytes(const pybind11::bytes& bytes)
{
    size_t index = 0;
    size_t byteSize = len(bytes);
    std::vector<unsigned char> elements(byteSize, 0);
    for (pybind11::handle item : bytes) { elements[index] = item.cast<unsigned char>(); }
    return elements;
}

/**
 * Tests payload pass capability
 * @param dictionary Parameter Dictionary
 * @param bytes Byte Data (Inputs, Clips)
 * @return Byte Read Response
 */
std::string UnitTest_ReadPayload(const pybind11::dict& dictionary,
                                 const pybind11::bytes& bytes)
{
    std::stringstream stream;
    stream << "Parameters:" << std::endl;
    for (std::pair<pybind11::handle, pybind11::handle> item : dictionary)
    {
        stream << "\t" << item.first.cast<std::string>() << ": ";
        stream << item.second.cast<std::string>() << std::endl;
    }
    std::vector<unsigned char> byteArray = DGGrid_ConvertBytes(bytes);
    stream << "Payload Data:" << std::endl;
    stream << "\t" << byteArray.size() << " bytes" << std::endl;
    stream << "\t" << pydggrid::Functions::to_hex(byteArray) << std::endl;
    std::string response_string = stream.str();
    return response_string;
}

/**
 * Query parameter read unit test
 * @param dictionary Python Parameter Dictionary
 * @param bytes Payload Bytes
 * @return Unit test response
 */
std::string UnitTest_ReadQuery(const pybind11::dict& dictionary,
                               const std::vector<unsigned int>& bytes)
{
    pydggrid::Query query(PyDGGRID_readDictionaryToMap(dictionary),
                          PyDGGRID_readBytesToUCVector(bytes));
    return query.toString();
}

/**
 * Query parameter read unit test
 * @param dictionary Python Parameter Dictionary
 * @param bytes Payload Bytes
 * @return Unit test response
 */
std::string UnitTest_RunQuery(const pybind11::dict& dictionary,
                               const std::vector<unsigned int>& bytes)
{
    pydggrid::Query query(PyDGGRID_readDictionaryToMap(dictionary),
                          PyDGGRID_readBytesToUCVector(bytes));
    query.run();
    return query.toString();
}

/**
 * Runs the query and compiles response bytes
 * @param dictionary Parameter Dictionary
 * @param bytes Payload Bytes
 * @return Response Bytes
 */
pybind11::dict RunQuery(const pybind11::dict& dictionary,
                                    const std::vector<unsigned int>& bytes)
{
    pydggrid::Query query(PyDGGRID_readDictionaryToMap(dictionary),
                          PyDGGRID_readBytesToUCVector(bytes));
    //
    query.run();
    pybind11::dict dict;
    dict["cells"] = query.getResponse("cells");
    dict["points"] = query.getResponse("points");
    dict["collection"] = query.getResponse("collection");
    dict["meta"] = query.getResponse("meta");
    return dict;
}

PYBIND11_MODULE(libpydggrid, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: cmake_example

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";
    m.def("add", &add);
    m.def("RunQuery", &RunQuery);
    m.def("UnitTest_ReadQuery", &UnitTest_ReadQuery);
    m.def("UnitTest_RunQuery", &UnitTest_RunQuery);
    m.def("UnitTest_ReadPayload", &UnitTest_ReadPayload);

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}

