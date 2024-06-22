#include <iostream>
#include "src/library.h"

int main()
{
    const char *shapeFile_test = "/opt/source/ut/libpydggrid/Examples/TestPayload_binvalsV8.hex";
    std::string hexString = pydggrid::Functions::readString(shapeFile_test);
    pydggrid::Bytes bytes(hexString.c_str());
    std::map<std::string, std::string> parameters;
//################################################################################
//################################################################################
//#
//# binvalsV8.meta - example of a dggrid meta-file which performs point value
//#      binning that uses GDAL Shapefiles for input and output.
//#
//# Determine the number of Oregon bridges and their total and mean lengths in the
//# cells of resolution 10 of an ISEA3H DGGS.
//#
//################################################################################
//
//# specify the operation
//dggrid_operation BIN_POINT_VALS
//
//# specify the DGG
//
//dggs_type ISEA3H
//dggs_res_spec 10
//
//# specify bin controls
//
//# indicate that we're only using a small part of the globe
//# this helps DGGRID use memory more efficiently
//bin_coverage PARTIAL
//
//# specify the input
//input_files inputfiles/bridges_2020_WGS84/bridges_2020_WGS84.shp
//point_input_file_type GDAL
//input_value_field_name LENGTH_FT
//
//# specify the output
//cell_output_control OUTPUT_OCCUPIED
//output_cell_label_type OUTPUT_ADDRESS_TYPE
//output_address_type SEQNUM
//precision 7
//
//# what data to output for each cell?
//# note Shapefile field names must be 10 characters or less
//output_count TRUE
//output_count_field_name numBridges
//output_total TRUE
//output_total_field_name totLenFt
//output_mean TRUE
//output_mean_field_name meanLenFt
//
//# specify the per-cell output using GDAL-supported file formats
//# output cell boundaries
//cell_output_type GDAL
//cell_output_gdal_format "ESRI Shapefile"
//cell_output_file_name outputfiles/cells
//
//# output the points to a seperate file
//point_output_type GDAL
//point_output_gdal_format "ESRI Shapefile"
//point_output_file_name outputfiles/points
//
//# version 7 style text output parameters
//# for backwards compatibility the text file is output by default.
//output_file_name outputfiles/textOutput.txt
//# Set to NONE for no text output.
//output_file_type TEXT
//output_delimiter ","

    parameters["dggrid_operation"] = "BIN_POINT_VALS";
    parameters["dggs_type"] = "ISEA3H";
    parameters["dggs_res_spec"] = "7";
    parameters["bin_coverage"] = "PARTIAL";
    parameters["input_delimiter"] = "\"|\"";
    parameters["point_input_file_type"] = "GDAL";
    parameters["input_value_field_name"] = "LENGTH_FT";
//    parameters["output_count"] = "TRUE";
//    parameters["output_mean"] = "TRUE";
//    parameters["output_num_classes"] = "TRUE";
//    parameters["output_num_classes_field_name"] = "numClass";
//    parameters["point_input_file_type"] = "GDAL";
//    parameters["geodetic_densify"] = "0.00";
//    parameters["dggs_num_placements"] = "4";
//    parameters["dggs_orient_specify_type"] = "RANDOM";
//    parameters["dggs_orient_rand_seed"] = "1013";
//    parameters["max_cells_per_output_file"] = "50";
//    parameters["cell_output_type"] = "KML";
//    parameters["point_output_type"] = "KML";
//    parameters["dggs_orient_output_file_name"] = "dmd";



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