# analysis.py
# Module pour l'analyse statistique des données.

import pandas as pd
import numpy as np

def get_descriptive_stats(df, columns):
    """
    Calcule et retourne les statistiques descriptives de base.
    """
    print("\n--- Statistiques Descriptives ---")
    stats_df = df[columns].describe() 
    print(stats_df)                  
    return stats_df               

def get_avg_mpg_by_origin(df):
    """
    Calcule et affiche le MPG moyen par origine.
    Retourne la série pour le graphique.
    """
    print("--- MPG Moyen par Origine ---")
    avg_mpg = df.groupby('origin')['mpg'].mean().sort_values(ascending=False)
    print(avg_mpg)
    return avg_mpg

def get_correlation_matrix(df, columns):
    """
    Calcule et affiche la matrice de corrélation.
    """
    print("--- Matrice de Corrélation ---")
    correlation_matrix = df[columns].corr()
    print("Corrélation avec 'mpg' :")
    print(correlation_matrix['mpg'].sort_values(ascending=False))
    return correlation_matrix

def get_numpy_percentile(df, column, percentile=95):
    """
    Utilise NumPy pour calculer un percentile spécifique.
    """
    value = np.percentile(df[column], percentile)
    print(f"--- Calcul NumPy ---")
    print(f"{percentile}ème percentile pour '{column}' : {value:.2f}")
    return value

def get_advanced_aggregates(df):
    """
    Calcule des agrégats avancés pour le rapport.
    Utilise .median(), .nunique(), .idxmax(), .idxmin()
    """
    print("\n--- Analyses Aggrégées Avancées ---")
    
    # 1. Utilisation de .median()
    median_mpg = df['mpg'].median()
    print(f"Consommation (MPG) médiane : {median_mpg:.2f}")
    
    # 2. Utilisation de .nunique()
    unique_origins = df['origin'].nunique()
    print(f"Nombre d'origines uniques : {unique_origins}")
    
    # 3. Utilisation de .idxmax() (pour trouver l'index du meilleur MPG)
    best_mpg_idx = df['mpg'].idxmax()
    best_mpg_car = df.loc[best_mpg_idx]
    print(f"Meilleure consommation (max) : {best_mpg_car['name']} ({best_mpg_car['mpg']} MPG)")
    
    # 4. Utilisation de .idxmin() (pour trouver l'index du pire MPG)
    worst_mpg_idx = df['mpg'].idxmin()
    worst_mpg_car = df.loc[worst_mpg_idx]
    print(f"Pire consommation (min) : {worst_mpg_car['name']} ({worst_mpg_car['mpg']} MPG)")
    
    # Retourner un dictionnaire pour le rapport PDF
    results = {
        'median_mpg': median_mpg,
        'unique_origins': unique_origins,
        'best_car_name': best_mpg_car['name'],
        'best_car_mpg': best_mpg_car['mpg'],
        'worst_car_name': worst_mpg_car['name'],
        'worst_car_mpg': worst_mpg_car['mpg']
    }
    return results