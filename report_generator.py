# report_generator.py
# Module pour générer le rapport PDF final.

from fpdf import FPDF
import config
import pandas as pd # Importé pour le type hinting (optionnel)

# Définition de notre "palette de couleurs"
COLOR_PRIMARY_BG = (22, 54, 93)  # Bleu nuit (pour les en-têtes)
COLOR_PRIMARY_FG = (255, 255, 255) # Blanc (pour le texte sur fond bleu)
COLOR_SECTION_BG = (240, 240, 240) # Gris clair (pour les titres de section)
COLOR_SECTION_FG = (0, 0, 0)     # Noir (pour le texte des titres)
COLOR_TEXT = (30, 30, 30)       # Gris foncé (pour le corps du texte)

class PDFReport(FPDF):
    """Classe personnalisée pour inclure un en-tête et un pied de page."""
    
    def header(self):
        """
        En-tête amélioré avec fond coloré
        """
        self.set_fill_color(*COLOR_PRIMARY_BG)
        self.set_text_color(*COLOR_PRIMARY_FG)
        self.set_font('Arial', 'B', 16)
        # Cell(largeur, hauteur, texte, bordure, retour à la ligne, alignement, remplissage)
        self.cell(0, 14, "Rapport d'Analyse Automobile", 0, 1, 'C', fill=True)
        # Réinitialiser les couleurs et la police pour le reste du document
        self.set_fill_color(255, 255, 255) # Fond blanc
        self.set_text_color(*COLOR_TEXT)
        self.set_font('Arial', '', 10)
        self.ln(8) # Ajoute un espace après l'en-tête

    def footer(self):
        """
        Pied de page simple avec numéro de page
        """
        self.set_y(-15) # Position à 1.5 cm du bas
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128) # Gris
        # Affiche "Page X / {nb}"
        self.cell(0, 10, f'Page {self.page_no()} / {{nb}}', 0, 0, 'C')

    def section_title(self, title_text):
        """
        Crée un titre de section stylisé
        """
        self.ln(6) # Espace avant le titre
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(*COLOR_SECTION_BG)
        self.set_text_color(*COLOR_SECTION_FG)
        # Cellule de la largeur de la page
        self.cell(0, 8, f"  {title_text}", 0, 1, 'L', fill=True)
        self.set_font('Arial', '', 10)
        self.set_text_color(*COLOR_TEXT)
        self.ln(4) # Espace après le titre

    def key_value_line(self, key_text, value_text):
        """
        Formate une ligne de type Clé: Valeur
        """
        self.set_font('Arial', 'B', 10)
        # Calcule approximativement la largeur de la clé pour l'alignement
        key_width = self.get_string_width(key_text) + 2
        self.cell(key_width, 6, key_text, 0, 0, 'L')
        
        self.set_font('Arial', '', 10)

        self.multi_cell(0, 6, f": {value_text}", 0, 'L')

def create_pdf_report(stats_df, avg_mpg_series, corr_mpg_series, p95_accel, adv_aggs):
    """
    Génère le rapport PDF complet avec les analyses et les graphiques.
    """
    print("--- Démarrage de la génération du PDF (Version améliorée) ---")
    
    pdf = PDFReport(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages() # Active l'alias {nb} pour le nombre total de pages
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20) # Marge de 2cm en bas
    pdf.set_text_color(*COLOR_TEXT)
    pdf.set_font('Arial', '', 10)

    # --- Section 1: Analyse Statistique ---
    pdf.section_title('1. Statistiques Descriptives Clés')
    
    pdf.set_font('Courier', '', 8) 
    stats_string = stats_df.to_string()
    pdf.multi_cell(0, 5, stats_string)
    pdf.set_font('Arial', '', 10) # Retour à la police standard
    pdf.set_text_color(*COLOR_TEXT)
    pdf.ln(5)

    # --- Section 2: Analyses Spécifiques ---
    pdf.section_title('2. Analyses Spécifiques (Pandas & NumPy)')
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, "MPG Moyen par Origine :", 0, 1, 'L')
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 5, avg_mpg_series.to_string())
    pdf.ln(4)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, "Corrélation avec 'mpg' :", 0, 1, 'L')
    pdf.set_font('Courier', '', 10)
    pdf.multi_cell(0, 5, corr_mpg_series.to_string())
    pdf.ln(4)
    
    # Utilisation de la nouvelle fonction key_value
    pdf.key_value_line("95ème Percentile (Accélération)", f"{p95_accel:.2f} sec")
    pdf.ln(5)


    # --- Section 3: Analyses Agrégées Avancées ---
    pdf.section_title('3. Analyses Agrégées Avancées')
    
    pdf.key_value_line("Consommation (MPG) médiane", f"{adv_aggs['median_mpg']:.2f} MPG")
    pdf.ln(5)
    pdf.key_value_line("Nombre d'origines uniques", f"{adv_aggs['unique_origins']}")
    pdf.ln(5)
    pdf.key_value_line("Meilleure consommation", f"{adv_aggs['best_car_name']} ({adv_aggs['best_car_mpg']} MPG)")
    pdf.ln(5)
    pdf.key_value_line("Pire consommation", f"{adv_aggs['worst_car_name']} ({adv_aggs['worst_car_mpg']} MPG)")
    pdf.ln(10)
    
    # --- Section 4: Visualisations ---
    pdf.section_title('4. Visualisations')
    
    try:
        # Largeur max de 190mm (210mm - 10mm marge G - 10mm marge D)
        pdf.image(config.PLOT_HP_VS_MPG, x=10, y=None, w=190)
        pdf.ln(5)
        pdf.image(config.PLOT_AVG_MPG_ORIGIN, x=10, y=None, w=190)
    except FileNotFoundError as e:
        pdf.set_font('Arial', 'I', 10)
        pdf.set_text_color(255, 0, 0) # Rouge pour l'erreur
        pdf.cell(0, 10, f"Erreur: Image non trouvee - {e.filename}", 0, 1)
    except RuntimeError as e:
        # Gère le cas où l'image n'est pas lisible ou autre erreur fpdf
        pdf.set_font('Arial', 'I', 10)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 10, f"Erreur PDF lors de l'ajout de l'image: {e}", 0, 1)

    # Sauvegarder le fichier
    try:
        pdf.output(config.REPORT_PDF_PATH)
        print(f"Rapport PDF amélioré sauvegardé avec succès dans '{config.REPORT_PDF_PATH}'")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du PDF : {e}")