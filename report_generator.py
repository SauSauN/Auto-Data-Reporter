# report_generator.py
# Module pour générer le rapport PDF final.

from fpdf import FPDF
import config

class PDFReport(FPDF):
    """Classe personnalisée pour inclure un en-tête simple."""
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, "Rapport d'Analyse Automobile", 0, 1, 'C')
        self.ln(5)

def create_pdf_report(stats_df, avg_mpg_series, corr_mpg_series, p95_accel, adv_aggs):
    """
    Génère le rapport PDF complet avec les analyses et les graphiques.
    """
    print("--- Démarrage de la génération du PDF ---")
    
    pdf = PDFReport(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # --- Section 1: Analyse Statistique ---
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '1. Statistiques Descriptives Cles', 0, 1, 'L')
    
    # --- DÉBUT DE LA MODIFICATION ---
    # Nous passons à une police plus petite (taille 8) pour cette table large
    pdf.set_font('Courier', '', 8) 
    stats_string = stats_df.to_string()
    pdf.multi_cell(0, 5, stats_string)
    # Nous revenons à la police par défaut (taille 10) pour le reste
    pdf.set_font('Courier', '', 10) 
    # --- FIN DE LA MODIFICATION ---
    pdf.ln(5)

    # --- Section 2: Analyses Spécifiques ---
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '2. Analyses Specifiques (Pandas & NumPy)', 0, 1, 'L')
    
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 5, "MPG Moyen par Origine:\n" + avg_mpg_series.to_string())
    pdf.ln(5)
    pdf.multi_cell(0, 5, "Correlation avec 'mpg':\n" + corr_mpg_series.to_string())
    pdf.ln(5)
    pdf.multi_cell(0, 5, f"95eme Percentile (Acceleration): {p95_accel:.2f} sec")
    pdf.ln(5)

    # --- Section 3: Analyses Aggregées Avancées ---
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '3. Analyses Aggregees Avancees', 0, 1, 'L')
   
    print("------------------------------")
    print("------------------------------")
    print(adv_aggs)
    print("------------------------------")
    print("------------------------------")
    
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 5, f"Consommation (MPG) mediane : {adv_aggs['median_mpg']:.2f}")
    pdf.ln(5)
    pdf.multi_cell(0, 5, f"Nombre d'origines uniques : {adv_aggs['unique_origins']}")
    pdf.ln(5)
    pdf.multi_cell(0, 5, f"Meilleure consommation : {adv_aggs['best_car_name']} ({adv_aggs['best_car_mpg']} MPG)")
    pdf.ln(5)
    pdf.multi_cell(0, 5, f"Pire consommation : {adv_aggs['worst_car_name']} ({adv_aggs['worst_car_mpg']} MPG)")
    pdf.ln(10)
    
    # --- Section 4: Visualisations ---
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '4. Visualisations', 0, 1, 'L')
    
    try:
        # Note : config.PLOT_HP_VS_MPG doit contenir "img/mpg_vs_horsepower.png"
        pdf.image(config.PLOT_HP_VS_MPG, x=10, y=None, w=190)
        pdf.ln(5)
        # Note : config.PLOT_AVG_MPG_ORIGIN doit contenir "img/avg_mpg_by_origin.png"
        pdf.image(config.PLOT_AVG_MPG_ORIGIN, x=10, y=None, w=190)
    except FileNotFoundError as e:
        pdf.set_font('Arial', 'I', 10)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 10, f"Erreur: Image non trouvee - {e.filename}", 0, 1)

    # Sauvegarder le fichier
    try:
        pdf.output(config.REPORT_PDF_PATH)
        print(f"Rapport PDF sauvegardé avec succès dans '{config.REPORT_PDF_PATH}'")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du PDF : {e}")