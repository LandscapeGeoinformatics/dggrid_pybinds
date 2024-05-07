cmake_minimum_required (VERSION 3.9)

add_library(pydgaplib SHARED
        lib/DgApParamList.cpp
        lib/DgApSubOperation.cpp
)

if(GDAL_FOUND)
  target_compile_definitions(pydgaplib PRIVATE USE_GDAL)
endif()

# If GDAL isn't present than ${GDAL_INCLUDE_DIRS} and ${GDAL_LIBRARIES} give
# empty strings
target_include_directories(pydgaplib PUBLIC include ../../DGGRID/src/lib/dglib/include ${GDAL_INCLUDE_DIRS})
target_link_libraries(pydgaplib PRIVATE ${GDAL_LIBRARIES} shapelib proj4lib pydglib)
target_compile_features(pydgaplib PRIVATE cxx_std_11)
