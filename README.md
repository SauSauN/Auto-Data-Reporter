# Auto-Data-Reporter

## À propos du projet

**Auto-Data-Reporter** est un pipeline d'analyse de données en Python conçu pour automatiser l'ingestion, le nettoyage, l'analyse, la visualisation et le reporting d'un ensemble de données automobiles.

Le script exécute un processus complet :
1.  **Chargement** : Lit les données depuis un fichier `Automobile.csv`.
2.  **Prétraitement** : Nettoie les données, en gérant spécifiquement les valeurs manquantes (comme les '?' dans `horsepower`) et en convertissant les types de données.
3.  **Ingénierie de caractéristiques** : Crée de nouvelles colonnes pertinentes (comme `full_model_year` ou `efficacite_mpg`) en utilisant `pandas` et `numpy`.
4.  **Analyse** : Effectue des analyses statistiques, y compris des statistiques descriptives, des corrélations, et des agrégations avancées (médiane, `idxmax`/`idxmin`).
5.  **Visualisation** : Génère et sauvegarde des graphiques (nuage de points, diagramme en barres) à l'aide de `matplotlib`.
6.  **Rapport** : Compile toutes les analyses et les graphiques dans un rapport PDF final à l'aide de `fpdf`.

---

## Structure du projet et détail des modules

Le projet est divisé en modules distincts pour une meilleure organisation et maintenabilité.

### `main.py`
C'est le point d'entrée principal. Il orchestre l'ensemble du flux de travail en appelant les fonctions des autres modules dans le bon ordre.
1.  Charge les données (via `data_loader`).
2.  Nettoie les données (via `preprocessing`).
3.  Crée des caractéristiques (via `preprocessing`).
4.  Exécute toutes les analyses (via `analysis`).
5.  Génère les visualisations (via `visualization`).
6.  Sauvegarde le DataFrame final en CSV.
7.  Génère le rapport PDF (via `report_generator`).

### `config.py`
Fichier de configuration centralisé. Il ne contient que des constantes (variables globales) qui définissent les chemins d'accès pour les fichiers d'entrée et de sortie.
* `DATA_INPUT_PATH`
* `DATA_OUTPUT_PATH`
* `PLOT_HP_VS_MPG`
* `PLOT_AVG_MPG_ORIGIN`
* `REPORT_PDF_PATH`

### `data_loader.py`
* `load_data(file_path)`: Tente de charger le fichier CSV spécifié à l'aide de `pandas.read_csv`. Il inclut une gestion d'erreur `FileNotFoundError` au cas où le fichier n'existerait pas.

### `preprocessing.py`
Ce module gère toute la préparation des données.
* `clean_data(df)`:
    * Prend en charge la colonne `horsepower`, qui contient des valeurs non numériques (comme '?').
    * Il utilise `pd.to_numeric(..., errors='coerce')` pour convertir les nombres valides et transformer les '?' en `NaN` (Not a Number).
    * Il détecte les `NaN` et les remplace par la **moyenne** de la colonne, calculée avec `np.nanmean` (qui ignore les `NaN` lors du calcul).
* `create_features(df)`:
    * `full_model_year`: Crée une année complète (ex: 70 -> 1970).
    * `weight_per_hp`: Crée un ratio poids/puissance.
    * `efficacite_mpg`: Utilise `np.select` pour catégoriser les véhicules ('faible', 'moyen', 'eleve') en fonction de leur consommation MPG.

### `analysis.py`
Cœur statistique du projet.
* `get_descriptive_stats(df, columns)`: Retourne les statistiques de base (moyenne, std, min, max, quartiles) en utilisant la méthode `.describe()` de pandas.
* `get_avg_mpg_by_origin(df)`: Utilise `.groupby('origin')` pour calculer le MPG moyen pour chaque région d'origine.
* `get_correlation_matrix(df, columns)`: Calcule la matrice de corrélation (méthode de Pearson par défaut) avec `.corr()`.
* `get_numpy_percentile(df, column, percentile)`: Démontre l'utilisation de `numpy` pour un calcul statistique spécifique (`np.percentile`).
* `get_advanced_aggregates(df)`: Fournit des informations clés pour le rapport :
    * `.median()`: Calcule la médiane MPG.
    * `.nunique()`: Compte le nombre d'origines uniques.
    * `.idxmax()`: Trouve l'index (et donc le nom) de la voiture avec le **meilleur** MPG.
    * `.idxmin()`: Trouve l'index de la voiture avec le **pire** MPG.

### `visualization.py`
Responsable de la création des graphiques avec `matplotlib`.
* `plot_mpg_vs_horsepower(df, filename)`: Crée un **nuage de points** (`plt.scatter`) comparant la puissance et la consommation, avec une coloration basée sur l'année du modèle.
* `plot_avg_mpg_by_origin(avg_mpg_series, filename)`: Crée un **diagramme à barres** (`.plot(kind='bar')`) pour visualiser le MPG moyen par origine.

### `report_generator.py`
Assemble le rapport final.
* Utilise la bibliothèque `fpdf` et une classe personnalisée `PDFReport` pour ajouter un en-tête.
* `create_pdf_report(...)`: Fonction principale qui prend tous les résultats des analyses (DataFrames, Séries, valeurs scalaires).
* Il écrit les données textuelles (comme les statistiques descriptives et les agrégats avancés) et utilise `pdf.image()` pour incorporer les fichiers PNG générés par `visualization.py`.

---

## Description des Données (Attendue)

Ce pipeline est conçu pour un ensemble de données automobiles (`Automobile.csv`) contenant (au minimum) les colonnes suivantes, déduites des scripts d'analyse et de prétraitement :

* `mpg`: (Numérique) Consommation en Miles Per Gallon.
* `cylinders`: (Numérique) Nombre de cylindres.
* `horsepower`: (Objet/String) Puissance. Contient des valeurs numériques et des '?'.
* `weight`: (Numérique) Poids du véhicule.
* `acceleration`: (Numérique) Temps d'accélération.
* `model_year`: (Numérique) Année du modèle (format 70, 71, ...).
* `origin`: (Catégorique/Numérique) Code pour la région d'origine (ex: 1, 2, 3).
* `name`: (String) Nom du modèle du véhicule.

---

## Dépendances

Ce projet repose sur les bibliothèques Python suivantes :

* `pandas`: Pour la manipulation et l'analyse des données.
* `numpy`: Pour les opérations numériques (calcul de la moyenne, percentiles).
* `matplotlib`: Pour la génération des graphiques.
* `fpdf`: Pour la création du rapport PDF final.

Vous pouvez les installer via pip :
```bash
pip install pandas numpy matplotlib fpdf
