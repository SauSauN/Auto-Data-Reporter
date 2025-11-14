# data_loader.py
# Module pour charger les données.

import pandas as pd

def load_data(file_path):
    """
    Charge le fichier CSV depuis le chemin spécifié.
    
    Args:
        file_path (str): Chemin vers le fichier CSV.
        
    Returns:
        pd.DataFrame: DataFrame chargé ou None si une erreur se produit.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Fichier '{file_path}' chargé avec succès.")
        return df
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{file_path}' n'a pas été trouvé.")
        return None
