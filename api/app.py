from flask import Flask, render_template, request, flash, url_for, redirect, session 
from datetime import timedelta 
import pandas as pd

from map import CreateMap
from queries import AllTravelers, TravelerTrips, POIinCity

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'


SHOWN_POI = []
TRAVELER_LIST = list(AllTravelers().traveler)


@app.route('/', methods=['GET', 'POST'])
def index(poi=[], trips=pd.DataFrame({})):
    if request.method == 'POST':
        traveler = request.form.get('select-traveler')
        flash("people was selected !")
        city = request.form.get('input-location')
        print(traveler, city)

        if traveler != '' or traveler != 'none':
            data = TravelerTrips(traveler)
            # trips = ['\t'.join(list(map(lambda x: str(x), list(line[1])))) for line in data.iterrows()]
            trips = data.copy()
            print(data)
            poi = list(set(list(data["departName"].values) + list(data["destName"].values)))

            latitudes, longitudes = [], []

            for i in range(len(data["departLatitude"].values)):
                latitudes = latitudes + list([data["departLatitude"].values[i]]) + list([data["destLatitude"].values[i]])
                longitudes = longitudes + list([data["departLongitude"].values[i]]) + list([data["destLongitude"].values[i]])
            
            CreateMap(latitudes, longitudes)
            
        if city != '':
            data = POIinCity(city)
            poi = data["poiName"]
            latitudes, longitudes = data["poiLatitude"], data["poiLongitude"]

            CreateMap(latitudes, longitudes, lines=False, zoom=12)

    return render_template('base.html', voyages=trips, content=poi, travelers=TRAVELER_LIST)


@app.route('/map')
def map():
    return render_template('map.html')


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