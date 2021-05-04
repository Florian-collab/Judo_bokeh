

# Package
import numpy as np
import pandas as pd
import json


def coor_wgs84_to_web_mercator(lon, lat):
    """ fonction qui calcul mes coordonner dans le bon format:
     lon : float
     lat : float
     return :tuple """

    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)


def dataset_graphe1(df, var, poid):
    """ fonction qui calcul la densité/fréquence d'une variable
    (je n'ai pas trouver de fonction qui permet de le faire directement) :
     df : Dataframe, dataframe de pandas
     var : str, chaine de caractère
     poid : str, chaine de caractère
     return: dict """

    dt = df.loc[df['Event'] == poid]
    l_var = list(dt[var].sort_values().dropna().unique()) # valeur possible de la variables
    # Initialisation de notre dict de sortie
    dico = {'Var': l_var, 'Density_H': [], 'Density_F': [], 'Density': []}

    # on compte la fréquence pour chaque valeur possibles
    for a in l_var:
        dt = df.loc[df[var] == a]
        dico['Density'].append(dt.shape[0])
        dth = df.loc[(df[var] == a) & (df['Sex'] == 'M')]
        dico['Density_H'].append(dth.shape[0])
        dtf = df.loc[(df[var] == a) & (df['Sex'] == 'F')]
        dico['Density_F'].append(dtf.shape[0])

    tt = sum(dico['Density'])
    th = sum(dico['Density_H'])
    tf = sum(dico['Density_F'])
    for i in range(len(l_var)):
        dico['Density'][i] = dico['Density'][i]/tt
        dico['Density_H'][i] = dico['Density_H'][i]/th
        dico['Density_F'][i] = dico['Density_F'][i]/tf

    return dico


def dataset_graphe2(df):
    """ fonction qui calcul l'effectif par catégorie de poids :
     df : Dataframe, dataframe de pandas
     return: dict """

    # les valeurs possibles des catégorie de poid et des années
    l_poid = list(df.Event.sort_values().unique())
    l_ann = list(df.Year.sort_values().unique())

    # création de notre dict de sortie
    dico = {'year': l_ann}
    for p in l_poid:
        dico[p] = []
    for p in l_poid:
        for y in l_ann:
            dt = df.loc[(df['Year'] == y) & (df['Event'] == p)]
            dico[p].append(dt.shape[0])
    dico["year"] = [str(elt) for elt in l_ann]

    return dico


def dataset_carte1(df, li1, li2, li3):
    """ fonction qui permet de recuperer les polygone de chaque pays
     et de compter le nombre de medaille selon les conditions:
     df : dataframe, dataframe de pandas
     li1 : list
     li2 : list
     li3 : list
     return: dataframe, dataframe de pandas """

    # Nos fichier avec nos données : iso3/iso2/polygon/coordonnée
    fp = open("countries.geojson", "r", encoding='utf-8')
    countries = json.load(fp)
    fp2 = open("capitals.geojson", "r", encoding='utf-8')
    caps = json.load(fp2)

    # Initialisation de notre dict de sortie
    dico = {"Pays": [], "nb_medals": [], "coordx": [], "coordy": []}

    for pays, noc in zip(list(df.Team.unique()), list(df.NOC.unique())):

        # les conditions médailles, catégorie de poids et sexe
        dt_p = df.loc[(df['Team'] == pays) & (df['Sex'].isin(li2))]
        dt = dt_p.loc[(dt_p['Medal'].isin(li1)) & (dt_p['Event'].isin(li3))]
        # print(dt) pour vérifier

        # on récupère le iso2 du pays
        code = None
        for p in caps["features"]:
            # on compare iso3 mais également le nom du pays car dans la base de données jeux Olympiques on a des anciens
            # iso3/noc qui ne sont pas forcement les même qu'aujourd'hui, exemple Allemagne, Curacao
            if p["properties"]["country"] == pays or p["properties"]["iso3"] == noc:
                code = p["properties"]["iso2"]

        # on recupere le polygone du pays
        for c in countries["features"]:
            if c["properties"]["cca2"].upper() == code:
                zones = c["geometry"]["coordinates"]
                # les pays n'ont pas la même structure de zones exemple Suisse,
                # print(len(zones))
                if len(zones) == 1:
                    coord = [coor_wgs84_to_web_mercator(point[0], point[1]) for point in zones[0]]
                    dico["coordx"].append([point[0] for point in coord])
                    dico["coordy"].append([point[1] for point in coord])
                    dico["Pays"].append(pays)
                    dico["nb_medals"].append(dt.shape[0])

                elif len(zones) == 2 and len(zones[0][0]) == 2:
                    for liste in zones:
                        coord = [coor_wgs84_to_web_mercator(point[0], point[1]) for point in liste]
                        dico["coordx"].append([point[0] for point in coord])
                        dico["coordy"].append([point[1] for point in coord])
                        dico["Pays"].append(pays)
                        dico["nb_medals"].append(dt.shape[0])
                else:
                    for poly in zones:
                        for liste in poly:
                            coord = [coor_wgs84_to_web_mercator(point[0], point[1]) for point in liste]
                            dico["coordx"].append([point[0] for point in coord])
                            dico["coordy"].append([point[1] for point in coord])
                            dico["Pays"].append(pays)
                            dico["nb_medals"].append(dt.shape[0])

    df_finale = pd.DataFrame(dico)
    # Affectation d'une couleur en fonction du nombre de médailles,
    # donc j'ai effectué un trie avant pour correspondre dans le même ordre/groupe
    df_finale = df_finale.sort_values(by='nb_medals')
    q = [0, 5, 10]
    my_palette = ['#E0FBF9' for i in range(df_finale.loc[df_finale["nb_medals"] == q[0]].shape[0])] + \
                 ['#9CCAFB' for i in range(df_finale.loc[(df_finale["nb_medals"] > q[0]) & (df_finale["nb_medals"] <= q[1])].shape[0])] + \
                 ['#93F97B' for i in range(df_finale.loc[(df_finale["nb_medals"] > q[1]) & (df_finale["nb_medals"] <= q[2])].shape[0])] + \
                 ['#FAF904' for i in range(df_finale.loc[df_finale["nb_medals"] > q[2]].shape[0])]
    df_finale["couleur"] = my_palette

    return df_finale


def dataset_carte2(df1, Team):
    """ fonction qui permet de récupérer les coordonnées de chaque villes des jeux olympiques
     et de compter le nombre de medaille pour le pays:
     df1 : dataframe, dataframe de pandas
     Team : str, chaine de caractère
     return: dict """
    # fichier de mes villes avec leur coordonnées, je l'ai créer avant avec le module graphh :
    # https://graphh.readthedocs.io/en/latest/
    df_villes = pd.read_csv('position_villes.txt', sep=";")

    # Initialisation de notre dict de sortie
    dico = {"Ville": list(df1.City.unique()), "nb_medals": [], "coordx": [], "coordy": [], "couleur": [], "taille": []}

    for v in dico["Ville"]:
        dt = df1.loc[(df1['Team'] == Team) & (df1['City'] == v)]
        dico["nb_medals"].append(dt.shape[0])
        xy = coor_wgs84_to_web_mercator(float(df_villes.loc[df_villes["City"] == v, "lon"]),
                                        float(df_villes.loc[df_villes["City"] == v, "lat"]))
        dico["coordx"].append(xy[0])
        dico["coordy"].append(xy[1])
        dico["couleur"].append("red")

        # pour la taille de nos points sur la carte plus ou moins important
        dico["taille"].append(dt.shape[0]*0.8+13 if dt.shape[0] > 0 else 0)

    return dico


