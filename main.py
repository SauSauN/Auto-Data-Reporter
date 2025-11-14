# main.py
# Script principal pour orchestrer l'ensemble du projet d'analyse.

# Importation des modules personnalisés
import config
import data_loader
import preprocessing
import analysis
import visualization
import report_generator

def main():
    """
    Fonction principale du projet.
    """
    print("=== DÉBUT DU PROJET D'ANALYSE AUTOMOBILE ===")
    
    # Étape 1: Charger les données
    df = data_loader.load_data(config.DATA_INPUT_PATH)
    if df is None:
        print("Échec du chargement des données. Arrêt du script.")
        print(f"Veuillez vous assurer que '{config.DATA_INPUT_PATH}' est dans le même dossier.")
        return

    # Étape 2: Nettoyer les données
    df_clean = preprocessing.clean_data(df)
    
    # Étape 3: Créer des caractéristiques
    df_features = preprocessing.create_features(df_clean)

    # Étape 4: Analyse
    print("\nExécution de l'analyse...")
    stats = analysis.get_descriptive_stats(df_features, ['mpg', 'horsepower', 'weight'])
    avg_mpg_series = analysis.get_avg_mpg_by_origin(df_features)
    corr_matrix = analysis.get_correlation_matrix(df_features, ['mpg', 'cylinders', 'horsepower', 'weight', 'acceleration'])
    p95_accel = analysis.get_numpy_percentile(df_features, 'acceleration', 95)
    
    # --- NOUVELLE LIGNE ---
    # Appel de notre nouvelle fonction d'agrégation
    adv_aggs = analysis.get_advanced_aggregates(df_features)
    
    print("Analyse terminée.")
    
    # Étape 5: Visualisation
    print("\nGénération des graphiques...")
    visualization.plot_mpg_vs_horsepower(df_features, config.PLOT_HP_VS_MPG)
    visualization.plot_avg_mpg_by_origin(avg_mpg_series, config.PLOT_AVG_MPG_ORIGIN)
    print("Graphiques terminés.")

    # Étape 6: Sauvegarde CSV
    try:
        df_features.to_csv(config.DATA_OUTPUT_PATH, index=False)
        print(f"\nDonnées finales sauvegardées dans '{config.DATA_OUTPUT_PATH}'")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier : {e}")
        
    # Étape 7: Génération du Rapport PDF
    try:
        # --- MODIFICATION ---
        # Ajoutez le nouvel argument adv_aggs=adv_aggs
        report_generator.create_pdf_report(
            stats_df=stats,
            avg_mpg_series=avg_mpg_series,
            corr_mpg_series=corr_matrix['mpg'],
            p95_accel=p95_accel,
            adv_aggs=adv_aggs 
        )
    except Exception as e:
        print(f"Erreur lors de la génération du PDF : {e}")

    print("=== FIN DU PROJET ===")

if __name__ == "__main__":
    main()