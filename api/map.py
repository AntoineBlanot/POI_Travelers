# import gmplot package
import gmplot
import numpy as np

# from queries import POIinCity

PATH = 'api/templates/'
APIKEY = 'AIzaSyCeHfnEmIV64MKItgqYGCiidf37Zu05Sak'

def CreateMap(latitudes=np.array([0]), longitudes=np.array([0]), lines=True, zoom=5):
        latitudes = np.array(latitudes)
        longitudes = np.array(longitudes)

        # zoom = max(np.linalg.norm(latitudes), np.linalg.norm(longitudes))
        # zoom = 15 - 100*max(latitudes.std(), longitudes.std())
        # print(zoom)
        gmap3 = gmplot.GoogleMapPlotter(latitudes.mean(), longitudes.mean(), zoom, scale_control=True)
        gmap3.apikey = APIKEY

        # scatter method of map object
        # scatter points on the google map
        gmap3.scatter(latitudes, longitudes, color='firebrick', size=20, marker=True)

        # Plot method Draw a line in
        # between given coordinates
        if lines:
                for i in range(0, len(latitudes) - 1, 2):
                        gmap3.plot(latitudes[i:i+2], longitudes[i:i+2], 'cornflowerblue', edge_width=3.0)

        gmap3.draw(PATH + 'map.html')
        return True


# data = POIinCity(city="Paris")
# print(data.info())
# CreateMap(data["poiLatitude"].values, data["poiLongitude"].values)