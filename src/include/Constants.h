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
        static int OPTIONS = 7;
        static int INT64 = 8;
        static int INT32 = 9;
        static int DOUBLE = 10;
        static int BOOLEAN = 11;
        static int NONE = 255;
    }
    static std::vector<std::string> shapefile_extensions = {"shp", "shx", "dbf", "prj", "sbn", "sbx"};
    static std::vector<std::string> data_indexes = {"cell", "point", "collection"};
    static std::vector<std::string> response_indexes = {"cells", "points", "pr_cells", "r_points", "collection"};
}
#endif //SRC_PYDGGRID_CONSTANTS_H
