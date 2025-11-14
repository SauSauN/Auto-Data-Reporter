# visualization.py
# Module pour générer et sauvegarder les graphiques.

import matplotlib.pyplot as plt

def plot_mpg_vs_horsepower(df, filename):
    """
    Crée un nuage de points de MPG vs Horsepower.
    """
    plt.style.use('ggplot')
    plt.figure(figsize=(10, 6))
    plt.scatter(df['horsepower'], df['mpg'], alpha=0.6, c=df['full_model_year'])
    plt.title('Consommation (MPG) en fonction de la Puissance (Horsepower)')
    plt.xlabel('Puissance (Horsepower)')
    plt.ylabel('Consommation (Miles Per Gallon)')
    plt.colorbar(label='Année Modèle')
    plt.grid(True)
    plt.savefig(filename)
    print(f"Graphique sauvegardé dans '{filename}'")
    plt.clf() # Nettoie la figure

def plot_avg_mpg_by_origin(avg_mpg_series, filename):
    """
    Crée un diagramme à barres du MPG moyen par origine.
    """
    plt.figure(figsize=(8, 5))
    avg_mpg_series.plot(kind='bar', color=['#4CAF50', '#2196F3', '#FFC107'])
    plt.title('MPG Moyen par Origine du Véhicule')
    plt.xlabel('Origine')
    plt.ylabel('MPG Moyen')
    plt.xticks(rotation=0)
    plt.savefig(filename)
    print(f"Graphique sauvegardé dans '{filename}'")
    plt.clf()
