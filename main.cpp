#include <iostream>
#include "src/library.h"

int main()
{
    const char *shapeFile_test = "/opt/source/ut/libpydggrid/Examples/TestPayload_holes.hex";
    std::string hexString = pydggrid::Functions::readString(shapeFile_test);
    pydggrid::Bytes bytes(hexString.c_str());
    std::map<std::string, std::string> parameters;
    // #
    //# # specify the operation
    //# dggrid_operation GENERATE_GRID
    //#
    //# # specify the DGG
    //# dggs_type ISEA3H
    //# dggs_res_spec 2
    //#
    //# # control the generation
    //# clip_subset_type WHOLE_EARTH
    //# geodetic_densify 0.0
    //#
    //# # create four orientations randomly
    //# dggs_num_placements 4
    //# dggs_orient_specify_type RANDOM
    //# dggs_orient_rand_seed 1013
    //# dggs_orient_output_file_name outputfiles/isea3h2.meta
    //#
    //# # specify the output
    //# max_cells_per_output_file 50
    //# cell_output_type KML
    //# cell_output_file_name outputfiles/isea3h2
    //# point_output_type KML
    //# point_output_file_name outputfiles/isea3h2p
    //# kml_default_width 2
    //# kml_default_color ff0000ff
    //# precision 5
    parameters["dggrid_operation"] = "GENERATE_GRID";
    parameters["dggs_type"] = "ISEA3H";
    parameters["dggs_res_spec"] = "2";
    parameters["clip_subset_type"] = "WHOLE_EARTH";
    parameters["geodetic_densify"] = "0.00";
    parameters["dggs_num_placements"] = "4";
    parameters["dggs_orient_specify_type"] = "RANDOM";
    parameters["dggs_orient_rand_seed"] = "1013";
    parameters["max_cells_per_output_file"] = "50";
    parameters["cell_output_type"] = "KML";
    parameters["point_output_type"] = "KML";
    parameters["dggs_orient_output_file_name"] = "dmd";



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