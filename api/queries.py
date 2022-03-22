import pandas as pd
from rdflib import Graph


# List of classes inside POI class (because we can not query with a reasonner)
POI_LIST = ['Building', 'Historical', 'Museum', 'Transport', 'TGVStation', 'TrainStation']

# Create a Graph, pare in Internet data
G = Graph().parse("./ontology.owl", format='application/rdf+xml')


def ExtractIndividual(individual):
    entity = individual.split("/")[-1]
    return entity if "project#" not in entity else entity[8:]


def TripsToCity(city="Paris"):
    results = pd.DataFrame({"trip": [], "poi": [], "city": []})

    query = """
        PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
        SELECT ?trip ?poi ?city
        WHERE { ?trip rdf:type ns:Trip .
                ?trip ns:to ?poi .
                ?poi ns:city ?city .
        FILTER (?city=\"""" + city + """\") .}
    """

    # Apply the query to the graph and iterate through results
    for r in G.query(query):
        results.loc[len(results.index)] = [ExtractIndividual(r["trip"]), ExtractIndividual(r["poi"]), r["city"]]

    return results


def TripsFromCity(city="Paris"):
    results = pd.DataFrame({"trip": [], "poi": [], "city": []})

    query = """
        PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
        SELECT ?trip ?poi ?city
        WHERE { ?trip rdf:type ns:Trip .
                ?trip ns:from ?poi .
                ?poi ns:city ?city .
        FILTER (?city=\"""" + city + """\") .}
    """

    # Apply the query to the graph and iterate through results
    for r in G.query(query):
        results.loc[len(results.index)] = [ExtractIndividual(r["trip"]), ExtractIndividual(r["poi"]), r["city"]]

    return results


def TravelerTrips(traveler="Alice"):
    results = pd.DataFrame({
        "trip": [], "departPOI": [], "destPOI": [],
        "departName": [], "destName": [],
        "departLatitude": [], "departLongitude": [],
        "destLatitude": [], "destLongitude": []
    })

    query = """
        PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
        SELECT ?trip ?departPOI ?destPOI ?departName ?destName ?departLatitude ?departLongitude ?destLatitude ?destLongitude
        WHERE { ns:""" + traveler + """ ns:hasTravelled ?trip .
                ?trip ns:from ?departPOI . ?departPOI ns:name ?departName . ?departPOI ns:latitude ?departLatitude . ?departPOI ns:longitude ?departLongitude .
                ?trip ns:to ?destPOI .  ?destPOI ns:name ?destName . ?destPOI ns:latitude ?destLatitude . ?destPOI ns:longitude ?destLongitude .}
    """
    # Apply the query to the graph and iterate through results
    for r in G.query(query):
        results.loc[len(results.index)] = [
            ExtractIndividual(r["trip"]), ExtractIndividual(r["departPOI"]), ExtractIndividual(r["destPOI"]),
            r["departName"], r["destName"],
            r["departLatitude"], r["departLongitude"],
            r["destLatitude"], r["destLongitude"]
        ]

    return results


def POIinCity(city="Paris"):
    results = pd.DataFrame({
        "poi": [], "city": [],
        "poiName": [], "poiLatitude": [], "poiLongitude": []
    })

    for poi in POI_LIST:
        query = """
            PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
            SELECT ?poi ?city ?poiName ?poiLatitude ?poiLongitude
            WHERE { ?poi rdf:type ns:""" + poi + """ .
                    ?poi ns:city ?city . ?poi ns:name ?poiName . ?poi ns:latitude ?poiLatitude . ?poi ns:longitude ?poiLongitude .
            FILTER (?city=\"""" + city + """\") .}
        """

        # Apply the query to the graph and iterate through results
        for r in G.query(query):
            results.loc[len(results.index)] = [
                ExtractIndividual(r["poi"]), r["city"], r["poiName"], r["poiLatitude"], r["poiLongitude"]
            ]
    results[["poiLatitude", "poiLongitude"]] = results[["poiLatitude", "poiLongitude"]].astype(float)
    
    return results


def GetLocationPOI(poi=""):
    results = pd.DataFrame({"poi": [], "name": [], "latitude": [], "longitude": []})
    
    # for poi in POI_LIST:
    #     query = """
    #         PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
    #         PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
    #         SELECT ?poi ?name ?latitude ?longitude
    #         WHERE { ?poi rdf:type ns:""" + poi + """ .
    #                 ?poi ns:latitude ?latitude .
    #                 ?poi ns:longitude ?longitude .
    #                 ?poi ns:name ?name .
    #         FILTER (?name=\"""" + name + """\") .}
    #     """

    query = """
        PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
        SELECT ?name ?latitude ?longitude
        WHERE { ns:""" + poi + """ ns:name ?name .
                ns:""" + poi + """ ns:latitude ?latitude .
                ns:""" + poi + """ ns:longitude ?longitude . }
    """
    print(query)
    # Apply the query to the graph and iterate through results
    for r in G.query(query):
        results.append([poi, r["name"], r["latitude"], r["longitude"]])

    return results


#region test

# print(TripsFromCity())
# print(TripsToCity())
# print(TravelerTrips(traveler="Alice"))
print(POIinCity("Paris"))
# print(GetLocationPOI("HIST1250"))

#endregion