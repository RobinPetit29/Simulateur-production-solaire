import streamlit as st  
from datetime import datetime
import requests

def demander_date(prompt):
 
    date_input = st.date_input(prompt)
    return datetime.combine(date_input, datetime.min.time()) 

def obtenir_donnees_utilisateur():

    st.subheader("Localisation et période")
    

    col1, col2 = st.columns(2)
    with col1:
        date_debut = demander_date("Date de début")
    with col2:
        date_fin = demander_date("Date de fin")
    

    if date_fin < date_debut:
        st.error(" La date de fin doit être postérieure à la date de début")
        return None, None, None, None

  
    city_name = st.text_input("Nom de la ville", "Paris")
    
    if st.button("Valider la localisation"):
       
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
    
    return None, None, None, None