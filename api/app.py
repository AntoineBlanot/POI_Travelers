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


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        traveler = request.form.get('select-traveler')
        city = request.form.get('input-location')

        # selectedTrip = None
        # print(traveler)
        # t = TravelerTrips(traveler)
        # print(t)
        # print(len(t))
        # for i in range(len(t)):
        #     print(f'poi-{i}')
        #     print(request.form)
        #     print(t["departName"][i])
        #     print(t["destName"][i])
        #     print(request.form.get(t["departName"][i]))
        #     if request.form.get(t["departName"][i]) == t["destName"][i]:
        #         print('ahah')
        #         selectedTrip = t[i]

        # print(selectedTrip)
        # if selectedTrip is not None:     
        #     CreateMap(
        #         list([selectedTrip["departLatitude"]]) + list([selectedTrip["destLatitude"]]),
        #         list([selectedTrip["departLongitude"]]) + list([selectedTrip["destLongitude"]]),
        #         lines=True
        #     )
        #     return render_template('base.html', voyages=t, content=list(set(list(t["departName"].values) + list(t["destName"].values))), travelers=TRAVELER_LIST, secret_traveler=traveler) 

        
        # length(dataframe )
        # for i in range(length):
        #  if poi-i=value : "tip from to " + trip[i]
        #     trip_real_value = trips[i]
        # (if poi=0 => trip = trips[0]) length(dataframe) 
        print(f'Traveler --> {traveler}, City --> {city}')
        
   
        if traveler != '' and traveler != 'none' and traveler is not None:
            print('travel')
            
            latitudes, longitudes, trips, pois = TravelerData(traveler)

            CreateMap(latitudes, longitudes)
            return render_template('base.html', voyages=trips[COLUMNS_TRIP], content=pois, travelers=TRAVELER_LIST, secret_traveler=traveler)
        
        elif city != '' and city is not None:
            # traveler = 'Choose a traveler...'

            print('city')
            latitudes, longitudes, pois = CityData(city)

            CreateMap(latitudes, longitudes, lines=False, zoom=12)
            return render_template('base.html', voyages=DEFAULT_TRIPS, content=pois, travelers=TRAVELER_LIST)
            # return render_template('base.html', voyages=DEFAULT_TRIPS, content=pois, travelers=TRAVELER_LIST, secret_traveler=traveler)
        
        else:
            print('not travel not city')
            # traveler = 'Choose a traveler...'

            CreateMap(DEFAULT_POIS["poiLatitude"].values, DEFAULT_POIS["poiLongitude"].values, lines=False)
            return render_template('base.html', voyages=DEFAULT_TRIPS, content=DEFAULT_POIS["poiName"], travelers=TRAVELER_LIST)
            # return render_template('base.html', voyages=DEFAULT_TRIPS, content=DEFAULT_POIS["poiName"], travelers=TRAVELER_LIST, secret_traveler=traveler)
    
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

@app.route('/search', methods=['GET'])
def search():
    trip = request.args.get('trip')
    print(trip)
    return render_template('index.html')

@app.route('/test' , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')
    return(str(select)) # just to see what select is


@app.route('/login',methods=["POST","GET"])
def login():
    if request.method =='POST':
        session.permanent = True 
        user = request.form['nm']
        session["user"]=user
        flash("Login Succesfull !")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Login")
            return redirect(url_for("user"))
        return render_template("login.html")
        

@app.route('/user')
def user():
    if "user" in session :
        user = session["user"]
        return render_template('user.html',user=user)
    else : 
        flash('Your are not logged in !')
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop("user",None)
    flash("You have been logged out!","info")
    return redirect(url_for("login"))


@app.route('/info', methods=('GET', 'POST'))
def info():
    if request.method ==  'POST':
        # do stuff here
        # language = request.form.get('language')
        CreateMap()
        return render_template('info.html')
    
# if __name__=="__main__":
#     app.run(debug=True)