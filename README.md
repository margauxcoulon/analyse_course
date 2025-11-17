# Analyse interactive de mes séances de course à pied

## Description
Ce projet est une mise en application concrète des deux premiers chapitres du cours [Python pour la data science](https://pythonds.linogaliana.fr/) de Lino Galiana.

En analysant des données de course à pied issues de fichiers `.fit` (téléchargés via Garmin Connect), j'utilise des techniques de **manipulation de données** et de **visualisation** pour explorer et mieux comprendre mes séances.


## Fonctionnalités
Ce projet permet de visualiser et d'explorer, grâce à des widgets interactifs :
- L’évolution temporelle de l’allure, de la fréquence cardiaque et de l’altitude.
- La distribution statistique et la variabilité des paramètres physiologiques.
- Les segments Montée / Plat / Descente et leur impact sur l’allure.
- La relation entre fréquence cardiaque et allure.
- Un tableau interactif résumant les indicateurs de chaque séance.


## Structure du projet
```
analyse_course/
│
├── data_fit/ → dossier contenant les fichiers .fit
│
├── analyse_seances.ipynb → notebook principal d’analyse
│
└── tools.py → fonctions utilitaires (conversion, nettoyage, indicateurs)

```


## Technologies utilisées
- Python 3
- Pandas : manipulation des données
- Matplotlib et Seaborn : visualisations statiques
- Plotly et Altair : visualisations interactives
- GreatTables : tableaux interactifs
- ipywidgets : interface interactive


## Installation et exécution

### 1 - Cloner le dépôt
```bash
git clone https://github.com/margauxcoulon/analyse_course.git
cd analyse_course
```

### 2 - Installer les dépendances
```bash
pip install pandas matplotlib seaborn plotly altair great_tables ipywidgets
```

### 3 - Ouvrir et exécuter le notebook `analyse_seances.ipynb`
Parcours le notebook cellule par cellule.  
- Sélectionne le type de séance (footing, fractionné, tempo, sortie longue, compétition) via un widget.
- Choisis une ou plusieurs séances à analyser.
- Explore les visualisations.


## 
Projet développé par Margaux Coulon, étudiante à Centrale Marseille, en novembre 2025.