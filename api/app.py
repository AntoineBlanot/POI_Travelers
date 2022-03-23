from flask import Flask, render_template, request, flash, url_for, redirect, session 
from datetime import timedelta 
import pandas as pd

from map import CreateMap
from queries import AllTravelers, TravelerTrips, POIinCity, AllPOI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

COLUMNS_TRIP = ['trip', 'departPOI', 'destPOI', 'departName', 'destName']

DEFAULT_POIS = AllPOI()
DEFAULT_TRIPS = pd.DataFrame({x : ["Default"] for x in COLUMNS_TRIP})
TRAVELER_LIST = list(AllTravelers().traveler)
select_traveler ='Choose a traveler'

@app.route('/', methods=['GET', 'POST'])
def index():

   
    if request.method == 'POST':
        traveler = request.form.get('select-traveler')
        city = request.form.get('input-location')
        
        
        if traveler != '' and  traveler != 'Choose a traveler...' and traveler is not None and traveler !="none":
            print('travel')

            selectedTrip = None
            t = TravelerTrips(traveler)
            for i in range(len(t)):
                if request.form.get(t["departName"][i]) ==f'Trip from {t["departName"][i]} to {t["destName"][i]}':
                    selectedTrip = t.iloc[[i]]

                print(selectedTrip)
                if selectedTrip is not None:     
                    CreateMap(
                        list([selectedTrip["departLatitude"]]) + list([selectedTrip["destLatitude"]]),
                        list([selectedTrip["departLongitude"]]) + list([selectedTrip["destLongitude"]]),
                        lines=True
                    )
                    return render_template('base.html', voyages=t, content=list(set(list(t["departName"].values) + list(t["destName"].values))), site=city, travelers=TRAVELER_LIST, secret_traveler=traveler ) 
            
            latitudes, longitudes, trips, pois = TravelerData(traveler) # point poi traveler.
            
            for i in range(len(pois)):
                if request.form.get(pois[i])==pois[i]:
                    new_pois=pois[i]
                    latitudes=[latitudes[i]]
                    longitudes=[longitudes[i]]
                
                    
            CreateMap(latitudes, longitudes)
            return render_template('base.html', voyages=trips[COLUMNS_TRIP], content=pois, travelers=TRAVELER_LIST, secret_traveler=traveler if traveler else'Choose a traveler' )
        
        elif city != '' and city is not None:
            traveler = 'Choose a traveler...'

            print('city')
            latitudes, longitudes, pois = CityData(city)

            for i in range(len(pois)):
                if request.form.get(pois[i])==pois[i]:
                    new_pois=pois[i]
                    latitudes=[latitudes[i]]
                    longitudes=[longitudes[i]]

            CreateMap(latitudes, longitudes, lines=False, zoom=12)
            # return render_template('base.html', voyages=DEFAULT_TRIPS, content=pois, travelers=TRAVELER_LIST)
            return render_template('base.html', voyages=DEFAULT_TRIPS, content=pois, travelers=TRAVELER_LIST, site=city, secret_traveler=traveler if traveler else'Choose a traveler')
        
        else:
            print('not travel not city')
            traveler = 'Choose a traveler...'

            CreateMap(DEFAULT_POIS["poiLatitude"].values, DEFAULT_POIS["poiLongitude"].values, lines=False)
            # return render_template('base.html', voyages=DEFAULT_TRIPS, content=DEFAULT_POIS["poiName"], travelers=TRAVELER_LIST)
            return render_template('base.html', voyages=DEFAULT_TRIPS, content=DEFAULT_POIS["poiName"], travelers=TRAVELER_LIST, secret_traveler=traveler, site=city)
    
    return render_template('base.html', voyages=DEFAULT_TRIPS, content=DEFAULT_POIS["poiName"], travelers=TRAVELER_LIST) 


def TravelerData(traveler):
    trips = TravelerTrips(traveler)
    pois = list(set(list(trips["departName"].values) + list(trips["destName"].values)))

    latitudes, longitudes = [], []
    for i in range(len(trips["departLatitude"].values)):
        latitudes = latitudes + list([trips["departLatitude"].values[i]]) + list([trips["destLatitude"].values[i]])
        longitudes = longitudes + list([trips["departLongitude"].values[i]]) + list([trips["destLongitude"].values[i]])
        
    return latitudes, longitudes, trips, pois


def CityData(city):
    data = POIinCity(city)
    pois = data["poiName"]
    
    latitudes, longitudes = data["poiLatitude"], data["poiLongitude"]

    return latitudes, longitudes, pois

@app.route('/map')
def map():
    return render_template('map.html')