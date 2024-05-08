#include <iostream>
#include "src/library.h"

int main()
{
    const char *shapeFile_test = "/opt/source/ut/libpydggrid/Examples/TestPayload_z3Nums.hex";
    std::string hexString = pydggrid::Functions::readString(shapeFile_test);
    pydggrid::Bytes bytes(hexString.c_str());
    std::map<std::string, std::string> parameters;
    //
    parameters["dggrid_operation"] = "GENERATE_GRID";
    parameters["dggs_type"] = "ISEA3H";
    parameters["dggs_res_spec"] = "9";
    parameters["clip_subset_type"] = "INPUT_ADDRESS_TYPE";
    parameters["input_address_type"] = "Z3";
    parameters["output_cell_label_type"] = "OUTPUT_ADDRESS_TYPE";
    parameters["output_address_type"] = "Z3";
    parameters["cell_output_type"] = "KML";
    parameters["point_output_type"] = "KML";



    //
    pydggrid::Query query(parameters, bytes.toVector());
    query.run();
    std::cout << query.toString() << std::endl;
    //
    {
        std::vector<unsigned char> blocks = query.getResponse("cells");
        size_t blockSize = blocks.size();
        for (size_t index = 0; index < blockSize; index++)
        {
            std::cout << (char) blocks[index];
        }
    }
    //
    {
        std::vector<unsigned char> blocks = query.getResponse("points");
        size_t blockSize = blocks.size();
        for (size_t index = 0; index < blockSize; index++)
        {
            std::cout << (char) blocks[index];
        }
        std::cout << std::endl;
    }
    return 0;
}