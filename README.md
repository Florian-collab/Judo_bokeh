# Judo_bokeh

L'objectif de mon projet a été de me focaliser sur les judokas de la base des Jeux olympiques. Le judo est un art-martial où deux combattants de même poids s'affrontent. Ainsi la ccolone 'Event' dans la base de données correspondent simplement aux différentes catégories de poids par exemple pour Heavyweight, ce sont les poids lourds les +100 Kg.
Pour présenter ces données en 2 cartes et 2 diagrammes, j'ai eu 2 idées : les judokas et les pays avec les médailles.

Graphique 1 :
J'ai voulu représenter les différentes caractéristiques physiologiques que l'on as, c'est-à-dire l'age, la taille et le sexe. Je me sers de la variable Event puisqu'il représente mes différentes catégories de poids. Ainsi, je représente la densité/fréquences de l'âge et de la taille en fonction de la catégorie des personnes.
Tout en pouvant choisir le sexe et/ou l'ensemble des judokas/judokates.

Graphique 2 :
J'ai voulu savoir l'évolution du nombre participant au jeu Olympique, mais aussi l'évolution des catégories. Ainsi, j'ai créé deux diagrammes selon le sexe pour voir les différences d'effectives ou non mais également leur évolution dans le temps.

Carte 1:
J'ai créé une carte pour savoir combien de médaille dans le judo (choisi par l'utilisateur) avait un pays. En prenant les pays qui ont déjà participé aux judo au moins 1 fois.

Carte 2:
J'ai voulu savoir si le lieu des Jeux avait un effet ou non. Donc j'ai représenté par pays combien de médailles ils ont gagné. Par exemple, Est que ce sont les Japonnais qui ont gagné le plus de médailles lors des jeux de 1964 ?

Pour réaliser l'ensemble de mes graphiques, j'ai découpé en deux m'ont code :
Bokeh.Judo.py : qui est l'application bokeh et création de mes graphes
create_dataset_graph.py : ensemble de fonction qui créait mes jeux de donnes pour faire mes graphiques.

Ainsi, pour lancer l'application, il faut lancer cette commande dans Anaconda prompt : bokeh serve --show Bokeh.judo.py
Je m'excuse d'avance pour les couleurs, je suis daltonien.
