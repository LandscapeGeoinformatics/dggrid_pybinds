#include <iostream>
#include "src/library.h"

int main()
{
    const char *shapeFile_test = "/opt/source/ut/libpydggrid/Examples/TestPayload_binvalsV8.hex";
    std::string hexString = pydggrid::Functions::readString(shapeFile_test);
    pydggrid::Bytes bytes(hexString.c_str());
    std::map<std::string, std::string> parameters;
//
    parameters["dggrid_operation"] = "BIN_POINT_VALS";
    parameters["dggs_type"] = "ISEA3H";
    parameters["dggs_res_spec"] = "10";
    parameters["precision"] = "7";
    parameters["bin_coverage"] = "PARTIAL";
    parameters["point_input_file_type"] = "GDAL";
    parameters["input_value_field_name"] = "LENGTH_FT";
    parameters["output_address_type"] = "SEQNUM";

//
//# specify the operation
//dggrid_operation BIN_POINT_VALS
//
//# specify the DGG
//
//dggs_type ISEA3H
//dggs_res_spec 9
//
//# specify bin controls
//
//bin_coverage PARTIAL
//input_files inputfiles/20k.txt inputfiles/50k.txt inputfiles/100k.txt inputfiles/200k.txt
//input_delimiter " "
//
//# specify text file output
//output_file_type TEXT
//output_file_name outputfiles/popval3h9.txt
//output_address_type SEQNUM
//output_delimiter ","
//precision 7
//cell_output_control OUTPUT_OCCUPIED

    std::vector<unsigned char> blocksEmpty{};
//    pydggrid::Query query(parameters, blocksEmpty);
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
    //
    {
        std::vector<unsigned char> blocks = query.getResponse("statistics");
        size_t blockSize = blocks.size();
        for (size_t index = 0; index < blockSize; index++)
        {
            std::cout << (char) blocks[index];
        }
        std::cout << std::endl;
    }
    return 0;
}

// # ################################################################################
//# ################################################################################
//# #
//# # binpres.meta - example of a dggrid meta-file which performs presence/absence
//# #                binning
//# #
//# # Determine the presence/absence of Oregon cities with various populations in
//# # the cells of resolution 7 of an ISEA3H DGGS.
//# #
//# # Created by Kevin Sahr, November 11, 2001
//# # Revised by Kevin Sahr, June 20, 2003
//# # Revised by Kevin Sahr, October 20, 2014
//# # Revised by Kevin Sahr, November 11, 2014
//# #
//# ################################################################################
//#
//# # specify the operation
//# dggrid_operation BIN_POINT_PRESENCE
//#
//# # specify the DGG
//# dggs_type ISEA3H
//# dggs_res_spec 7
//#
//# # specify bin controls
//# bin_coverage PARTIAL
//# input_files inputfiles/20k.txt inputfiles/50k.txt inputfiles/100k.txt inputfiles/200k.txt
//# input_delimiter " "
//#
//# # specify the output
//# output_file_name outputfiles/popclass3h7.txt
//# output_address_type SEQNUM
//# output_delimiter ","
//# output_num_classes TRUE
//# cell_output_control OUTPUT_OCCUPIED