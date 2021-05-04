#!/usr/bin/python3
# -*- coding:utf8 -*-
"""Bokeh Visualisation des données : le Judo aux Jeux Olympique"""

# mon fichier create_dataset_graph.py
from create_dataset_graph import dataset_graphe1, dataset_graphe2, dataset_carte2, dataset_carte1

# Package
import pandas as pd
from bokeh.palettes import Set1
from bokeh.models import Legend, HoverTool, ColumnDataSource, WMTSTileSource
from bokeh.models.widgets import RadioGroup, Panel, Tabs, Select, MultiChoice, Button, Div
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors


########################################################################################################################
# Importation des données
df_all = pd.read_csv('athlete_events.csv')
df_judo = df_all[df_all.Sport == 'Judo'].copy()

# Petite modification pour avoir les catégories de poids et le sexe est définie dans une colone
df_judo.Event = df_judo.Event.replace("Judo Men's ", "", regex=True)
df_judo.Event = df_judo.Event.replace("Judo Women's ", "", regex=True)
# print(df_judo.Event.unique()) pour verifier

########################################################################################################################
# Graphe densité/fréquence

# Les Widgets
radio_var = RadioGroup(name="Variable :", labels=["Age", "Taille"], active=0)
radio_poid = RadioGroup(name="Catégorie :", labels=['Extra-Lightweight', 'Half-Middleweight', 'Lightweight',
                                                    'Heavyweight', 'Half-Heavyweight', 'Middleweight',
                                                    'Half-Lightweight'], active=5)


def callback_radio(new):
    vars = ['Age', 'Height']
    ps = ['Extra-Lightweight', 'Half-Middleweight', 'Lightweight', 'Heavyweight', 'Half-Heavyweight',
          'Middleweight', 'Half-Lightweight']
    var = vars[radio_var.active]
    p = ps[radio_poid.active]
    data1.data.update(dataset_graphe1(df_judo, var, p))


radio_var.on_click(callback_radio)
radio_poid.on_click(callback_radio)

# Création du jeu de données pour le graphe
df_graphe1 = dataset_graphe1(df_judo, "Age", "Middleweight")
data1 = ColumnDataSource(data=df_graphe1)

# Graphique 1
p1 = figure(title="Fréquence", y_axis_label="Count", x_axis_label="Variable")

p1.title.text_color = "Blue"
p1.title.border_line_color = "green"

l0 = p1.line(x='Var', y='Density', source=data1, color='black')
l1 = p1.line(x='Var', y='Density_H', source=data1, color='blue')
l2 = p1.line(x='Var', y='Density_F', source=data1, color='red')

# Création de la légedne intéractive
legend1 = Legend(items=[("All", [l0]), ("Men", [l1]), ("Women", [l2])], location="top_center", click_policy="hide")
p1.add_layout(legend1, 'right')


########################################################################################################################
# Graphique 2 évolution des poids

# Homme
# Création du jeu de données pour le graphe
df_graphe2 = df_judo.loc[df_judo['Sex'].isin(['M'])]
dataset2 = dataset_graphe2(df_graphe2)
data2 = ColumnDataSource(data=dataset2)

# Création du graphe, je me suis servie de la documenation de bokeh car demande une structure particulière:
# https://docs.bokeh.org/en/latest/docs/gallery/bar_stacked.html

p2 = figure(x_range=data2.data["year"], title="Catégorie de poids chez les Hommes", toolbar_location=None,
            plot_width=900, plot_height=300,  sizing_mode="scale_both", tools="hover",
            tooltips="$name: @$name")

p2.title.text_color = "blue"
p2.title.border_line_color = "green"

r0 = p2.vbar_stack(list(data2.data.keys())[1:], x='year', color=Set1[len(list(data2.data.keys())[1:])],
                   source=data2, width=0.8)

# ajout de la légende
legend = Legend(items=[(list(data2.data.keys())[1:][i], [r0[i]]) for i in range(len(list(data2.data.keys())[1:]))],
                location="center", click_policy="hide")
p2.add_layout(legend, 'right')

# Femme
# Création du jeu de données pour le graphe
df_graphe21 = df_judo.loc[df_judo['Sex'].isin(['F'])]
dataset2 = dataset_graphe2(df_graphe21)
data21 = ColumnDataSource(data=dataset2)

# Création du graphe
p21 = figure(x_range=data21.data["year"], title="Catégorie de poids chez les Femmes", toolbar_location=None,
            plot_width=900, plot_height=300, sizing_mode="scale_both", tools="hover",
             tooltips="$name: @$name")
p21.title.text_color = "pink"
p21.title.border_line_color = "green"
r0 = p21.vbar_stack(list(data21.data.keys())[1:], x='year', color=Set1[len(list(data21.data.keys())[1:])],
                    source=data21, width=0.8)
# ajout de la légende
legend = Legend(items=[(list(data21.data.keys())[1:][i], [r0[i]]) for i in range(len(list(data21.data.keys())[1:]))],
                location="center", click_policy="hide")
p21.add_layout(legend, 'right')


########################################################################################################################
#  Carte 1 les médailles en fonction des pays


# Les Widgets
multi_choice1 = MultiChoice(title="Choisir les medaille :",
                           value=["Gold", "Silver", "Bronze"], options=["Gold", "Silver", "Bronze"])
multi_choice2 = MultiChoice(title="Choisir le sexe:",
                           value=["M", "F"], options=["M", "F"])
multi_choice3 = MultiChoice(title="Choisir les catégories de poids:",
                           value=['Extra-Lightweight', 'Half-Middleweight', 'Lightweight', 'Open Class',
                                  'Heavyweight', 'Half-Heavyweight', 'Middleweight', 'Half-Lightweight', ],
                            options=['Extra-Lightweight', 'Half-Middleweight', 'Lightweight', 'Open Class',
                                     'Heavyweight', 'Half-Heavyweight', 'Middleweight', 'Half-Lightweight'])
bouton = Button(label="Update !")
para = Div(text="""Petite texte pour dire d'éviter de mettre zero valeur dans les chox possible, la mise à jour 
peut prendre un peu de temp et que la couleur correspond aux pays ayant:<br> plus de 10 médaille -> jaune,
 <br> entre  5 et 10 -> vert, <br> entre 0 et 5 -> blue,<br> 0 -> blanc.""", width=200, height=100)


def callback_button():
    data3.data = dataset_carte1(df_judo, multi_choice1.value, multi_choice2.value, multi_choice3.value)


bouton.on_click(callback_button)

# Création du jeux de données pour la carte
Medals = ["Gold", "Silver", "Bronze"]
Sex = ["M", "F"]
Poid=['Extra-Lightweight', 'Half-Middleweight', 'Lightweight', 'Open Class',
      'Heavyweight', 'Half-Heavyweight', 'Middleweight', 'Half-Lightweight']
data3 = ColumnDataSource(dataset_carte1(df_judo, Medals, Sex, Poid))

# Création de la carte
c1 = figure(title="Carte des Médailles", x_axis_type=None, y_axis_type=None, active_scroll="wheel_zoom", height=250,
            width=500, sizing_mode="scale_both")
c1.title.text_color = "cornflowerblue"
c1.title.border_line_color = "yellow"

# Fond de carte issue d'openstreetmap
tile_provider = WMTSTileSource(url="https://b.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png")
c1.add_tile(tile_provider)

c1.patches("coordx", "coordy", source=data3, color='couleur', alpha=0.9)

# Intéraction
hover_tool = HoverTool(tooltips=[('Pays', '@Pays'), ('Nombre de médailles', '@nb_medals')])
c1.add_tools(hover_tool)


########################################################################################################################
#  Carte Villes
# Le Widget
select = Select(title="Pays:", value="France", options=sorted(list(df_judo.Team.unique())))


def update_carte(attr, old, new):
    source.data = dataset_carte2(df_judo, new)


select.on_change('value', update_carte)

# Création du jeux de données pour la carte
source = ColumnDataSource(data=dataset_carte2(df_judo, "France"))

# Création de la carte
c2 = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom", title="Medaille par ville",
            height=250, width=500, sizing_mode="scale_both")

# fond de carte issue de Bokeh
tile_provider = get_provider(Vendors.CARTODBPOSITRON)
c2.add_tile(tile_provider)

c2.hex('coordx', 'coordy', size='taille', source=source, color="couleur", alpha=0.9)

# Interaction
hover_tool = HoverTool(tooltips=[('Nombre de médailles', '@nb_medals'), ('Ville', '@Ville')])
c2.add_tools(hover_tool)


########################################################################################################################
#  Organisation de l'application
layout1 = row(column(radio_var, radio_poid), p1)
layout2 = column(p2, p21)
layout3 = row(column(multi_choice1, multi_choice2, multi_choice3, bouton, para), c1)
layout4 = row(select, c2)
tab1 = Panel(child=layout1, title="Age & Taille")
tab2 = Panel(child=layout2, title="Poids")
tab3 = Panel(child=layout3, title="Carte Medaille")
tab4 = Panel(child=layout4, title="Carte Ville")
tabs = Tabs(tabs=[tab1, tab2, tab3, tab4])
curdoc().add_root(tabs)

