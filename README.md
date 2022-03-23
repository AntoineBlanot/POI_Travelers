# WEB Datamining and Semantics Project

## Introduction

This project is about implementing a knowledge model (an ontology) on POI (Points Of Interests), Travelers and their related Trips. In this project, a Trip is caracterized by a departure (POI from which the Traveler start his journey) and a destination (POI where he ends it); there is no transit between this departure and destination.

## Ontology

The POI we selected for this project are:
- TGV Station in France (of class TGVStation and subclass Transport)
- Train stations (regional lines and not high-speed lines) in Ile-de-France (of class TrainStation and subclass Transport)
- Museums in France (of class Museum and subclass Building)
- Historical places in France (of class Historical and subclass Building)


### How to populate our ontology

- If our dataset is in .csv, convert it to .json [csv-json converter](https://www.convertcsv.com/csv-to-json.htm)
- Transform the .json in JSON-LD language by adding an @context in the begining
- Convert the JSON-LD in N-Quads [converter](https://json-ld.org/playground)
- Copy paste the N-Quads result [here](https://www.easyrdf.org/converter) and choose as input format "N-Triples" and Output format as "RDF/XML"
- Add in the ontology (.owl file) The RDF/XML result and pay attention to how namespaces are defined (rename it if necessary)


## How to install

### Flask API

To launch the Flask API, you have to install its package.
```
pip install flask
```

### RDF for Python

```
pip install rdflib
```

## How to use

In the project folder, run these commands:
```
export FLASK_APP=api/app
export FLASK_ENV=development
flask run
```
or for Windows users
```
set FLASK_APP=api/app
set FLASK_ENV=development
flask run
```
[Link to the Flask API](http://127.0.0.1:5000/)

Then, on the Flask API you can:
- See on the left the **map with POIs and Trips**
- Use the top-left search bar to **filter POIs by a city** (ex:Paris, Marseille, etc.) be **sure** that the select traveler is set to "Choose a traveler..." if not it will take this input over the city.
- Click on the POI right panel to show **one specific POI within the city**
- Use the top-right select bar to **choose a Traveler and see on the map its related Trips** 
- See on the bottom-left the **history of the Trips** done by the choosed Traveler (if no Traveler is choosed, nothing will be displayed)
- **Click on a specific trip** (in the history of the Traveler's trips) to only show this trip on the map
- See on the right the **POIs that are shown on the map**
- **Click on a specific POI** in the list to get only that POI shown
- Click on Default in the POI panel to show all the poi of the current Traveler

NB: There are some properties not integrated, for instance you can't get the POI within a city if you have previously selected a traveler (*set it Choose a traveler... or reset/reload*).If you run into a bug, please come back to the previous page and try another query, or try to restart the flask interface. 

The API will look like this:
![paris-api-screen](https://github.com/AntoineBlanot/POI_Travelers/blob/master/images/paris-pois.png?raw=true)


![bruno-api-screen](https://github.com/AntoineBlanot/POI_Travelers/blob/master/images/bruno-trips.png?raw=true)
