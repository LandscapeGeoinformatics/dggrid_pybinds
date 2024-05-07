#include <iostream>
#include "src/library.h"

int main()
{
    const char *shapeFile_test = "/opt/source/ut/libpydggrid/Examples/TestPayload_MixedSHP.hex";
    std::string hexString = pydggrid::Functions::readString(shapeFile_test);
    pydggrid::Bytes bytes(hexString.c_str());
    std::map<std::string, std::string> parameters;
//dggrid_operation=GENERATE_GRID
//clip_subset_type=AIGEN
//clip_cell_densification=1
//clipper_scale_factor=1000000
//clip_using_holes=false
//clip_cell_res=1
//dggs_type=FULLER43H
//dggs_num_aperture_4_res=3
//dggs_res_spec=10
//densification=3
//cell_output_type=SHAPEFILE
//shapefile_id_field_length=5

    parameters["dggrid_operation"] = "GENERATE_GRID";
    parameters["clip_subset_type"] = "AIGEN";
    parameters["dggs_type"] = "FULLER43H";
    parameters["dggs_res_spec"] = "10";
    parameters["dggs_num_aperture_4_res"] = "3";
    parameters["densification"] = "3";
    parameters["cell_output_type"] = "SHAPEFILE";
    parameters["point_output_type"] = "KML";
    parameters["shapefile_id_field_length"] = "5";
    parameters["geodetic_densify"] = "0.0";
    //
    //dggrid_operation=GENERATE_GRID
    //clip_subset_type=GDAL
    //clip_cell_densification=1
    //clipper_scale_factor=1000000
    //clip_using_holes=false
    //clip_cell_res=1
    //dggs_type=ISEA7H
    //dggs_res_spec=9
    //cell_output_type=GDAL_COLLECTION
    //point_output_type=GDAL_COLLECTION
    //cell_output_gdal_format=KML
    //point_output_gdal_format=GEOJSON
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
//    std::cout << "1: " << bytes.getInt() << std::endl;
//    std::cout << "2: " << bytes.getInt() << std::endl;
//    std::cout << "3: " << bytes.getInt() << std::endl;
//    std::cout << bytes.getSize() << std::endl;
    return 0;
}

/**
# ################################################################################
# #
# # gdalExample.meta - example of a DGGRID metafile that generates a resolution
# #     9 ISEA7H grid. The clipping and output files all use GDAL-readable file
# #     formats.
# #
# # Kevin Sahr, 08/29/19
# #
# ################################################################################
#
# # specify the operation
# dggrid_operation GENERATE_GRID
#
# # specify the DGG
# dggs_type ISEA7H
# dggs_res_spec 9
#
# # control grid generation
# clip_subset_type GDAL
# # gdal uses the file extension to determine the file format
# clip_region_files inputfiles/corvallis.shp
#
# # specify the output
# cell_output_type GDAL
# # for output the format needs to be explicit
# cell_output_gdal_format KML
# cell_output_file_name ./outputfiles/corvallisCells.kml
#
# point_output_type GDAL
# point_output_gdal_format GeoJSON
# point_output_file_name ./outputfiles/corvallisPts.geojson
*/