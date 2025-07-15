Simulateur de Production Solaire


Ce projet a été développé pour estimer la production d’énergie d’un panneau solaire, en fonction de la localisation, de la période choisie, et des données météorologiques réelles.

L’utilisateur entre une ville, une date de début et une date de fin. Le programme récupère les données d’irradiation solaire via l’API Open-Meteo, puis calcule l’énergie produite sur la période, en appliquant la formule physique : surface * rendement * irradiance * ratio de performance

Une interface simple est proposée grâce à Streamlit, permettant d’utiliser l’application depuis le navigateur.


Fonctionnalités:

-Choix libre de la ville 

-Sélection de la période de simulation (dates de début et fin)

-Récupération automatique des données d’irradiation solaire

-Calcul de l’énergie produite heure par heure

-Affichage graphique des résultats


Lancer l’application:

Installer les dépendances nécessaires (Python requis) :
pip install -r requirements.txt

Démarrer l’interface Streamlit :
python -m streamlit run App.py


Structure du projet:

App.py : contient l’interface Streamlit (là où l’utilisateur interagit)

API_météo.py : gère les appels à l’API Open-Meteo (géolocalisation + météo)

Calculs_physiques.py : contient les formules physiques pour estimer la production

Demande_utilisateur.py : récupère les paramètres entrés par l’utilisateur

requirements.txt : liste des bibliothèques nécessaires

README.md : fichier de présentation du projet


Technologies utilisées:

Python 3

Streamlit

Open-Meteo API

Pandas

Matplotlib



Ce projet a été conçu par Robin Petit, étudiant en 4e année à l’ECE Paris, dans le cadre d’un projet personnel visant à approfondir la manipulation d’API, les calculs physiques simples et l’interaction utilisateur via une interface web.

