from rdflib import Graph

# Create a Graph, pare in Internet data
g = Graph().parse("./ontology.owl", format='application/rdf+xml')

# Query the data in g using SPARQL
# This query returns the 'name' of all ``foaf:Person`` instances
q = """
    PREFIX ns: <http://www.semanticweb.org/antoineblanot/ontologies/web-data-semantics/project#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
 
    SELECT ?trip ?poi ?city
    WHERE { ?trip rdf:type ns:Trip .
    	    ?trip ns:to ?poi .
     	    ?poi ns:city ?city .
    FILTER (?city="Paris") .}

"""
print("ici")
# Apply the query to the graph and iterate through results
for r in g.query(q):
    print(r["trip"])

# prints: Timothy Berners-Lee