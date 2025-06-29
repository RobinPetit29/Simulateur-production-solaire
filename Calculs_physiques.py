import pandas as pd
from API_météo import get_irradiance_data  # Assurez-vous que le nom du fichier correspond exactement (majuscules/accents)

def calcul_puissance_pv(surface, rendement, irradiance, performance_ratio):
    """Calcule la puissance produite par un panneau solaire."""
    return surface * rendement * irradiance * performance_ratio

def calcul_energie_pv(surface, rendement, performance_ratio, df):
    """Calcule l'énergie produite et retourne un DataFrame enrichi."""
    df["date"] = pd.to_datetime(df["date"])  
    df_filtered = df[(df["date"].dt.hour >= 0) & (df["date"].dt.hour <= 23)].copy()
    
    df_filtered["puissance_w"] = df_filtered["shortwave_radiation"].apply(
        lambda x: calcul_puissance_pv(surface, rendement, x, performance_ratio)
    )
    df_filtered["energie_kwh"] = df_filtered["puissance_w"] / 1000
    
    return df_filtered

# --- Partie à supprimer si vous utilisez Streamlit ---
# (Cette partie ne devrait plus être dans ce fichier si vous avez un app.py séparé)
if __name__ == "__main__":
    # Exemple d'utilisation autonome (test)
    from demandes_utilisateur import obtenir_donnees_utilisateur  # Nouveau module où vous avez déplacé cette fonction
    
    print("Mode test autonome - Saisie des paramètres :")
    date_debut, date_fin, latitude, longitude = obtenir_donnees_utilisateur()
    
    if None not in [date_debut, date_fin, latitude, longitude]:
        df_irradiance = get_irradiance_data(
            date_debut=date_debut,
            date_fin=date_fin,
            latitude=latitude,
            longitude=longitude
        )
        
        surface = 1.6              
        rendement = 0.18                  
        performance_ratio = 0.8    
        
        df_resultat = calcul_energie_pv(surface, rendement, performance_ratio, df_irradiance)
        energie_totale = df_resultat["energie_kwh"].sum()
        print(f"\nÉnergie produite sur la période : {energie_totale:.2f} kWh")