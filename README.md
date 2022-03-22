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


### Flask API

To launch the Flask API, you have to install its package.
```
pip install flask
```

Then in the project folder, run these commands:
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

### RDF for Python

```
pip install rdflib
```