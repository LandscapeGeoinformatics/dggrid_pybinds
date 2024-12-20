# Version 0.0.7
# Change Log

- **0.0.7**
  - Memory leak fixes with original DGGRID library.
  - Implement and test Bin Points Query types
  - Implement and test Transform Query types
  - Implement and test Statistics Query types
  - Moved main operation object to unique pointer
  - Fixes to input handler object AIGen
  - Fixes to input handler object AIGen
  - Fixes to input handler object GDAL
  - Fixes to input handler object Location
  - Fixes to input handler object Sequence
  - Fixes to input handler object Shapefile
  - Added ZORDER types
  - Implemented Table output to handle statistics table
  - Created Statistics Query Module
  - Created Transform Query Module
  - Implemented GeoArrow for Location type output
  - Migration of DGGRID source updates
  - AIgen support for geometries

- **0.0.6**
  - Location data type
  - PointPresence Query
  - Location input empty line fix
  - Location inputs multi-location update
  - Sequence output object
  - Output Template Object
  - Input objects inheritance fixes
  
- **0.0.5**
  - UnitTests - planetRiskClipHiRes, planetRiskClipMulti
  - GDAL driver geojson fix
  - Docker and setup fixes by alex

- **0.0.4**
  - UnitTests - isea4d, isea4t, isea7hGen, multipleOrientations
  - dgg_meta patch access as <query>.dgg_meta 

- **0.0.3**
  - UnitTests - hiRes, holes, icosahedron
  - GDAL GeoJSON File fix

- **0.0.2**
    - gridgenCellClip, gridgenDiamond, gridgenPureKML unit tests
    - Cells input object
    - geojson and kml postamble fixes
    - various bugfixes


- **0.0.1** 
  - Initial Release


# Installation

To install take the following steps:

#### 1. Install GDAL
For linux -> https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html

For Mac -> https://medium.com/@vascofernandes_13322/how-to-install-gdal-on-macos-6a76fb5e24a4

#### 2. Other requirements

- python 3.9 
- python dev packages
- pybinds11
- glibc
- pip3

#### 3. Pull and Install
Pull or clone the repository and install with pip3 install /installation dir


Currently Available Queries

- GENERATE_GRID

Supported File Formats
- ShapeFile
- KML
- GeoJSON
- AIGen
- Raw Sequences
- Raw Coordinate Sets
- DGGS meta format

Tested Meta Files
- gdalCollection
- gdalExample
- MixedSHP
- aigenerate
- grigenGeoJSON
- seqnums
- z3Nums
- gridgenCellClip
- gridgenDiamond
- gridgenPureKML
- hiRes
- holes
- icosahedron
- isea4d
- isea4t
- isea7hGen
- multipleOrientations

** This library has not been tested with MacOS systems