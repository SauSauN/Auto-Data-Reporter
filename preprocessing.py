# preprocessing.py
# Module pour le nettoyage et l'ingénierie de caractéristiques.

import pandas as pd
import numpy as np

def clean_data(df):
    """
    Nettoie le DataFrame. Gère 'horsepower' et d'autres problèmes potentiels.
    
    Args:
        df (pd.DataFrame): DataFrame brut.
        
    Returns:
        pd.DataFrame: DataFrame nettoyé.
    """
    print("--- Démarrage du nettoyage ---")
    
    # 1. Gérer 'horsepower' (convertir en numérique, gérer les '?' qui deviennent NaN)
    df_clean = df.copy()
    df_clean['horsepower'] = pd.to_numeric(df_clean['horsepower'], errors='coerce')

    # 2. Remplir les NaN (valeurs manquantes) avec la moyenne (calculée par NumPy)
    if df_clean['horsepower'].isnull().any():
        print(f"  {df_clean['horsepower'].isnull().sum()} valeurs manquantes trouvées dans 'horsepower'.")
        # Utilisation de np.nanmean pour ignorer les NaN existants lors du calcul
        mean_hp = np.nanmean(df_clean['horsepower'])
        print(f"  Remplacement par la moyenne : {mean_hp:.2f}")
        df_clean['horsepower'] = df_clean['horsepower'].fillna(mean_hp)
    
    print("--- Nettoyage terminé ---")
    return df_clean

def create_features(df):
    """
    Crée de nouvelles colonnes (caractéristiques) pour l'analyse.
    
    Args:
        df (pd.DataFrame): DataFrame nettoyé.
        
    Returns:
        pd.DataFrame: DataFrame avec de nouvelles caractéristiques.
    """
    print("--- Création de caractéristiques ---")
    df_feat = df.copy()
    
    # 1. Année modèle complète
    df_feat['full_model_year'] = df_feat['model_year'] + 1900
    
    # 2. Ratio poids/puissance
    df_feat['weight_per_hp'] = df_feat['weight'] / df_feat['horsepower']
    
    # 3. Catégories d'efficacité (exemple parfait pour np.select)
    conditions = [
        (df_feat['mpg'] <= 15),
        (df_feat['mpg'] > 15) & (df_feat['mpg'] <= 25),
        (df_feat['mpg'] > 25)
    ]
    choices = ['faible', 'moyen', 'eleve']
    df_feat['efficacite_mpg'] = np.select(conditions, choices, default='inconnu')
    
    print("  Colonnes 'full_model_year', 'weight_per_hp', 'efficacite_mpg' créées.")
    print("--- Fin de la création de caractéristiques ---")
    return df_feat
