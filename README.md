# WEB Datamining and Semantics Project

## How to populate our ontology

    - If our dataset is in .csv, convert it to .json [csv-json converter](https://www.convertcsv.com/csv-to-json.htm)
    - Transform the .json in JSON-LD language by adding an @context in the begining
    - Convert the JSON-LD in N-Quads [converter](https://json-ld.org/playground)
    - Copy paste the N-Quads result [here](https://www.easyrdf.org/converter) and choose as input format "N-Triples" and Output format as "RDF/XML"
    - Add in the ontology (.owl file) The RDF/XML result and pay attention to how namespaces are defined (rename it if necessary)

    