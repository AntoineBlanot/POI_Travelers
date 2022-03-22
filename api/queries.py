import pandas as pd

from rdflib import Graph

# Create a Graph, pare in Internet data
G = Graph().parse("./ontology.owl", format='application/rdf+xml')


def TripsToCity(city="Paris"):
    query = """
        PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
        SELECT ?trip ?poi ?city
        WHERE { ?trip rdf:type ns:Trip .
                ?trip ns:to ?poi .
                ?poi ns:city ?city .
        FILTER (?city=\"""" + city + """\") .}
    """
    results = pd.DataFrame({"trip": [], "poi": [], "city": []})

    # Apply the query to the graph and iterate through results
    for r in G.query(query):
        results.loc[len(results.index)] = [r["trip"], r["poi"], r["city"]]
    
    return results


def POIinCity(city="Paris"):
    results = []
    query = """
        PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
        SELECT ?poi
        WHERE { ?poi rdf:type ns:POI|ns:TGVStation|ns:TrainStation .
                ?poi ns:city ?city .
        FILTER (?city=\"""" + city + """\") .}
    """

    results = pd.DataFrame({"poi": []})

    # Apply the query to the graph and iterate through results
    for r in G.query(query):
        results.loc[len(results.index)] = [r["poi"]]
    
    return results


def GetLocationPOI(name=""):
    results = []
    query = """
        PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
        SELECT ?poi ?name ?latitude ?longitude
        WHERE { ?poi rdfs:subClassOf ns:Transport .
                ?poi ns:latitude ?latitude .
                ?poi ns:longitude ?longitude .
                ?poi ns:name ?name .
        FILTER (?name=\"""" + name + """\") .}
    """

    # Apply the query to the graph and iterate through results
    for r in G.query(query):
        results.append([r["poi"], r["name"], r["latitude"], r["longitude"]])
    
    return results

#print(GetLocationPOI("Paris-Montparnasse"))

print(POIinCity().head())