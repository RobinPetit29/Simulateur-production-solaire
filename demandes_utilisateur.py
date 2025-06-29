import streamlit as st  
from datetime import datetime
import requests

def demander_date(prompt):
    """Version adaptée pour Streamlit"""
    date_input = st.date_input(prompt)
    return datetime.combine(date_input, datetime.min.time())  # Convertit en datetime.date

def obtenir_donnees_utilisateur():
    """Version Streamlit qui retourne (date_debut, date_fin, latitude, longitude)"""
    st.subheader("Localisation et période")
    
    # 1. Saisie des dates
    col1, col2 = st.columns(2)
    with col1:
        date_debut = demander_date("Date de début")
    with col2:
        date_fin = demander_date("Date de fin")
    
    # Validation des dates
    if date_fin < date_debut:
        st.error(" La date de fin doit être postérieure à la date de début")
        return None, None, None, None

    # 2. Saisie de la ville
    city_name = st.text_input("Nom de la ville", "Paris")
    
    if st.button("Valider la localisation"):
        # 3. Géocodage
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&format=json"
        response = requests.get(geocode_url).json()
        
        if "results" in response and response["results"]:
            latitude = response["results"][0]["latitude"]
            longitude = response["results"][0]["longitude"]
            st.success(f"Coordonnées trouvées : {latitude:.2f}°N, {longitude:.2f}°E")
            return date_debut, date_fin, latitude, longitude
        else:
            st.error(f"Ville '{city_name}' non trouvée")
            return None, None, None, None
    
    # Retour par défaut (attente validation)
    return None, None, None, None