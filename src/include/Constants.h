#ifndef SRC_PYDGGRID_CONSTANTS_H
#define SRC_PYDGGRID_CONSTANTS_H

namespace pydggrid::Constants
{
    namespace DataTypes
    {
        static int INT = 1;
        static int FLOAT = 2;
        static int SHORT = 3;
        static int BINARY = 4;
        static int STRING = 5;
        static int SHAPE_BINARY = 6;
        static int GDAL_GEOJSON = 7;
        static int OPTIONS = 8;
        static int INT64 = 9;
        static int INT32 = 10;
        static int DOUBLE = 11;
        static int BOOLEAN = 12;
        static int LOCATION = 13;
        static int NONE = 255;
    }
    static std::vector<std::string> shapefile_extensions = {"shp", "shx", "dbf", "prj", "sbn", "sbx"};
    static std::vector<std::string> data_indexes = {"cell", "point", "collection"};
    static std::vector<std::string> response_indexes = {"cells", "points", "pr_cells", "r_points", "collection"};
}
#endif //SRC_PYDGGRID_CONSTANTS_H
