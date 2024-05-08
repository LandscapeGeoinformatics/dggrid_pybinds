import geopandas
import fiona

if __name__ == "__main__":
    fiona.drvsupport.supported_drivers['kml'] = 'rw' # enable KML support which is disabled by default
    fiona.drvsupport.supported_drivers['KML'] = 'rw' # enable KML support which is disabled by default
    frame = geopandas.GeoDataFrame.from_file("/tmp/KMLTEST.kml")
    print(frame)