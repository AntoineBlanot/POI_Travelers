import pandas as pd
from rdflib import Graph


# List of classes inside POI class (because wa can not query with a reasonner)
POI_LIST = ['Building', 'Historical', 'Museum', 'Transport', 'TGVStation', 'TrainStation']

# Create a Graph, pare in Internet data
G = Graph().parse("./ontology.owl", format='application/rdf+xml')


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
        results.loc[len(results.index)] = [r["trip"], r["poi"], r["city"]]

    return results


def POIinCity(city="Paris"):
    results = pd.DataFrame({"poi": [], "city": []})

    for poi in POI_LIST:
        query = """
            PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
            SELECT ?poi ?city
            WHERE { ?poi rdf:type ns:""" + poi + """ .
                    ?poi ns:city ?city .
            FILTER (?city=\"""" + city + """\") .}
        """

        # Apply the query to the graph and iterate through results
        for r in G.query(query):
            results.loc[len(results.index)] = [r["poi"], r["city"]]
    
    return results


def GetLocationPOI(name=""):
    results = pd.DataFrame({"poi": [], "name": [], "latitude": [], "longitude": []})
    
    for poi in POI_LIST:
        query = """
            PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
            SELECT ?poi ?name ?latitude ?longitude
            WHERE { ?poi rdf:type ns:""" + poi + """ .
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

print(POIinCity("Paris").iloc[10].poi)