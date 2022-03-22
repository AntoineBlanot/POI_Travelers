# import gmplot package
import gmplot
import numpy as np

from queries import POIinCity

PATH = 'api/templates/'

def CreateMap(latitudes, longitudes):

        # zoom = max(np.linalg.norm(latitudes), np.linalg.norm(longitudes))
        zoom = 15 - 100*max(latitudes.std(), longitudes.std())
        print(zoom)
        gmap3 = gmplot.GoogleMapPlotter(latitudes.mean(), longitudes.mean(), zoom, scale_control=True)

        # scatter method of map object
        # scatter points on the google map
        gmap3.scatter(latitudes, longitudes, color='firebrick', size=20, marker=True)

        # Plot method Draw a line in
        # between given coordinates
        # gmap3.plot(latitudes, longitudes, 'cornflowerblue', edge_width=3.0)

        gmap3.draw(PATH + 'map.html')
        return True


data = POIinCity(city="Paris")
print(data.info())
CreateMap(data["poiLatitude"].values, data["poiLongitude"].values)