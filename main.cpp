#include <iostream>
#include "src/library.h"

int main()
{
    const char *shapeFile_test = "/opt/source/ut/libpydggrid/Examples/TestPayload_holes.hex";
    std::string hexString = pydggrid::Functions::readString(shapeFile_test);
    pydggrid::Bytes bytes(hexString.c_str());
    std::map<std::string, std::string> parameters;
    // # ################################################################################
    //# #
    //# # holes.meta - example of a DGGRID metafile that generates a ISEA3H
    //# #     resolution 17 grid using an input clipping polygon with holes.
    //# #
    //# # Kevin Sahr, 06/20/22
    //# #
    //# ################################################################################
    //#
    //# # specify the operation
    //# dggrid_operation GENERATE_GRID
    //#
    //# # specify the DGG
    //# dggs_type ISEA3H
    //# dggs_res_spec 17
    //#
    //# # control the generation
    //# clip_subset_type GDAL
    //# clip_region_files ./inputfiles/holes00.geojson
    //# clip_using_holes TRUE
    //# geodetic_densify 0.01
    //#
    //# # specify the output
    //# cell_output_type KML
    //# cell_output_file_name ./outputfiles/res17
    //# densification 1
    //
    parameters["dggrid_operation"] = "GENERATE_GRID";
    parameters["dggs_type"] = "ISEA3H";
    parameters["dggs_res_spec"] = "17";
    parameters["clip_subset_type"] = "GDAL";
    parameters["clip_using_holes"] = "TRUE";
    parameters["geodetic_densify"] = "0.01";    
    parameters["cell_output_type"] = "KML";



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