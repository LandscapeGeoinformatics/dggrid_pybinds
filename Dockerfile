# ubuntu base image
FROM ubuntu:22.04

ENV TZ=Europe/Tallinn
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install python3, gdal cmake build-essential and python dev
RUN apt-get update && apt-get install -y python3 python3-pip python3-gdal cmake build-essential python3-dev git pybind11-dev ninja-build libgdal-dev libproj-dev libgeos-dev libspatialindex-dev python3-gdal python3-geopandas python3-fiona python3-shapely python3-geojson python3-pandas

# clone repo
# RUN git clone https://github.com/LandscapeGeoinformatics/dggrid_pybinds.git /dggrid_pybinds && cd /dggrid_pybinds && pip3 install .
RUN mkdir -p /dggrid_pybinds
# COPY CMakeLists.txt DGGRID build Examples main.cpp pybind11 pydggrid  setup.py  src /dggrid_pybinds/
COPY CMakeLists.txt /dggrid_pybinds/
COPY src /dggrid_pybinds/src
COPY DGGRID /dggrid_pybinds/DGGRID
COPY build /dggrid_pybinds/build
COPY Examples /dggrid_pybinds/Examples
COPY main.cpp /dggrid_pybinds/
COPY pybind11 /dggrid_pybinds/pybind11
COPY pydggrid /dggrid_pybinds/pydggrid
COPY setup.py /dggrid_pybinds/


RUN cd /dggrid_pybinds && pip3 install .

CMD ["/bin/bash"]



