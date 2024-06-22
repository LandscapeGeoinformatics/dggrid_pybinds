cmake_minimum_required (VERSION 3.9)
project(src VERSION 0.8.1 LANGUAGES C CXX)
# PYBIND 11
add_subdirectory(pybind11)
add_executable(pydggrid_test
        main.cpp
        src/library.cpp
        src/pydggrid/OpBasic.cpp
        src/pydggrid/SubOpMain.cpp
        src/pydggrid/SubOpDGG.cpp
        src/pydggrid/SubOpIn.cpp
        src/pydggrid/SubOpOut.cpp
        src/pydggrid/SubOpGen.cpp
        src/pydggrid/SubOpBinPts.cpp
        src/pydggrid/SubOpBasic.cpp
        src/pydggrid/SubOpBasicMulti.cpp
        src/pydggrid/SubOpGenHelper.cpp
        src/pydggrid/clipper.cpp
        src/pydggrid/DgHexSF.cpp)
pybind11_add_module(libpydggrid
        main.cpp
        src/library.cpp
        src/pydggrid/OpBasic.cpp
        src/pydggrid/SubOpMain.cpp
        src/pydggrid/SubOpDGG.cpp
        src/pydggrid/SubOpIn.cpp
        src/pydggrid/SubOpOut.cpp
        src/pydggrid/SubOpGen.cpp
        src/pydggrid/SubOpBinPts.cpp
        src/pydggrid/SubOpBasic.cpp
        src/pydggrid/SubOpBasicMulti.cpp
        src/pydggrid/SubOpGenHelper.cpp
        src/pydggrid/clipper.cpp
        src/pydggrid/DgHexSF.cpp)
#
target_compile_definitions(libpydggrid PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})
## DGGRID
find_package(GDAL REQUIRED)
add_subdirectory(DGGRID/src/lib/shapelib)
add_subdirectory(DGGRID/src/lib/proj4lib)
# add_subdirectory(DGGRID/src/lib/dglib)
add_subdirectory(src/pydgaplib)
add_subdirectory(src/pydglib)
#add_subdirectory(DGGRID/src/lib/dglib)
#add_subdirectory(DGGRID/src/apps/dggrid)
#add_subdirectory(DGGRID/src/lib/dgaplib)
target_include_directories(libpydggrid PUBLIC include DGGRID/src/lib/pydgaplib ${GDAL_INCLUDE_DIRS})
target_include_directories(pydggrid_test PUBLIC include src/pydgaplib ${GDAL_INCLUDE_DIRS})
target_compile_features(libpydggrid PRIVATE cxx_std_17)
target_compile_features(pydggrid_test PRIVATE cxx_std_17)
target_compile_definitions(libpydggrid PRIVATE USE_GDAL)
target_compile_definitions(pydggrid_test PRIVATE USE_GDAL)
## link libs
file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/pydggrid DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/pydggrid)
target_link_libraries(libpydggrid PRIVATE ${GDAL_LIBRARIES} shapelib proj4lib pydglib pydgaplib)
target_link_libraries(pydggrid_test PRIVATE ${GDAL_LIBRARIES} shapelib proj4lib pydglib pydgaplib pybind11::embed)