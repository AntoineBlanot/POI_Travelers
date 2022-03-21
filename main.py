import pandas as pd

IDF = ['75', '77', '78', '91', '92', '93', '94', '95']
COLUMN_TO_KEEP = [
    "Identifiant Museofile",
    "Adresse",
    "Commune",
    "Departement",
    "Latitude",
    "Longitude",
    "Nom officiel du musee",
    "Code Postal",
    "Region administrative",
    "Type"
]

def IDF_only(file):

    data = pd.read_csv(file, sep=';')
    idf = data.loc[data["code_departement"].isin(IDF)]
    print(data["code_departement"].isin(IDF).value_counts())

    idf["code_departement"].astype(int)
    lat_long = [str(x).split(',') for x in idf["coordonnees_finales"]]

    idf["lat"] = list(map(lambda x: x[0] if len(x) == 2 else 0, lat_long))
    idf["long"] = list(map(lambda x: x[1] if len(x) == 2 else 0, lat_long))

    idf.reset_index().to_csv(file + '_idf.csv', sep=';')

    print("over")

#IDF_only('data/monuments-historiques.csv')

data = pd.read_csv('data/csv/museum.csv', sep=";")
keep = data[COLUMN_TO_KEEP]
keep["Latitude"] = keep["Latitude"].apply(lambda x: float(x.replace(',', '.')))
keep["Longitude"] = keep["Longitude"].apply(lambda x: float(x.replace(',', '.')))
print(keep.info())
keep.to_csv('keep.csv', sep=";")
