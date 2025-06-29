import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from demandes_utilisateur import obtenir_donnees_utilisateur
from API_météo import get_irradiance_data
from Calculs_physiques import calcul_energie_pv

# Configuration de la page
st.set_page_config(
    page_title="SunPower Simulator",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gestion de l'état de navigation
if "page" not in st.session_state:
    st.session_state.page = "accueil"

# Page d'accueil
if st.session_state.page == "accueil":
    # Header avec logo et titre
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(".streamlit\solar-panel.png", width=150)
    with col2:
        st.title("Simulateur de production solaire")
        st.subheader("Estimez votre production d'énergie solaire en un rien de temps")
    
    # Section d'explication
    st.markdown("""
    <div style='background-color:#f0f2f6; padding:25px; border-radius:10px;'>
    <h3>🧠 Comment ça marche ?</h3>
    <p>Notre simulateur vous permet d'estimer la production énergétique de vos panneaux solaires sur une période donnée.
    Il peut aussi faire des estimations grâce aux prévisions météo de l'énergie produite dans le futur:</p>
    <ol>
        <li><b>Localisation</b> : Entrez votre ville pour connaître l'ensoleillement local</li>
        <li><b>Période</b> : Choisissez la durée de simulation (1 jour à 1 an)</li>
        <li><b>Configuration</b> : Donnez les caractéristiques de vos panneaux solaires</li>
        <li><b>Résultats</b> : Visualisez votre production potentielle</li>
    </ol>
    <p>➡️ Les calculs s'appuient sur des données météo réelles et des modèles physiques éprouvés.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Avantages
    st.markdown("### 💡 Pourquoi utiliser ce simulateur ?")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("""
        **Économies potentielles**  
        Estimez votre retour sur investissement
        """)
    with col_b:
        st.info("""
        **Écologique**  
        Calculez votre réduction d'émissions CO₂
        """)
    with col_c:
        st.info("""
        **Personnalisable**  
        Adaptez les paramètres à votre installation
        """)
    
    
    # Bouton de démarrage
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚀 Commencer ma simulation", use_container_width=True, type="primary"):
        st.session_state.page = "simulation"
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption("© 2023 SunPower Simulator | Données météo fournies par Open-Meteo")

# Page de simulation
elif st.session_state.page == "simulation":
    # Header avec bouton retour
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Retour à l'accueil"):
            st.session_state.page = "accueil"
            st.rerun()
    with col2:
        st.title("☀️ Simulation de production solaire")
    
    # Sidebar avec paramètres
    with st.sidebar:
        st.header("⚙️ Paramètres techniques")
        surface = st.number_input(
            "Surface des panneaux (m²)", 
            min_value=0.1, 
            value=1.6, 
            step=0.1,
            help="Surface totale des panneaux solaires"
        )
        rendement = st.slider(
            "Rendement (%)", 
            min_value=1, 
            max_value=30, 
            value=18,
            help="Efficacité de conversion énergétique des panneaux"
        )
        performance_ratio = st.slider(
            "Performance Ratio", 
            min_value=0.1, 
            max_value=1.0, 
            value=0.8, 
            step=0.05,
            help="Coefficient incluant les pertes du système"
        )
        st.markdown("---")
        st.info("""
        **Valeurs typiques :**
        - Rendement : 15-22%
        - Performance Ratio : 0.75-0.85
        """)
    
    # Partie principale
    st.header("📍 1. Localisation et période")
    date_debut, date_fin, latitude, longitude = obtenir_donnees_utilisateur()
    
    if latitude and longitude:
        # Simulation avec indicateur de progression
        with st.spinner("Calcul de votre production solaire..."):
            df_irradiance = get_irradiance_data(
                date_debut=date_debut,
                date_fin=date_fin,
                latitude=latitude,
                longitude=longitude
            )
            
            df_energy = calcul_energie_pv(
                surface=surface,
                rendement=rendement/100,
                performance_ratio=performance_ratio,
                df=df_irradiance
            )
        
        # Calcul des résultats
        energie_totale = df_energy["energie_kwh"].sum()
        jours = (date_fin - date_debut).days + 1
        moyenne_journaliere = energie_totale / jours
        
        st.header("📊 2. Résultats de votre simulation")
        
        # KPI principaux
        col1, col2, col3 = st.columns(3)
        col1.metric("Production totale", f"{energie_totale:.2f} kWh")
        col2.metric("Moyenne journalière", f"{moyenne_journaliere:.2f} kWh/j")
        col3.metric("Équivalent ménage", 
                   f"{(energie_totale / 4.5):.1f} jours",
                   help="Consommation moyenne d'un foyer français = 4.5 kWh/j")
        
        # Graphiques
        st.subheader("Production horaire")
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df_energy["date"], df_energy["puissance_w"], color='#ff9900')
        ax.set_xlabel("Date")
        ax.set_ylabel("Puissance (W)")
        ax.grid(alpha=0.2)
        ax.set_title("Production solaire horaire")
        st.pyplot(fig)
        
        # Données détaillées
        st.subheader("Données complètes")
        with st.expander("Voir les données horaires"):
            st.dataframe(df_energy[["date", "shortwave_radiation", "puissance_w", "energie_kwh"]].rename(
                columns={
                    "shortwave_radiation": "Irradiance (W/m²)",
                    "puissance_w": "Puissance (W)",
                    "energie_kwh": "Énergie (kWh)"
                }
            ))
        
        # Export des résultats
        st.subheader("📥 Export des résultats")
        csv = df_energy.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les données CSV",
            data=csv,
            file_name="production_solaire.csv",
            mime="text/csv",
            help="Contient toutes les données horaires de production"
        )
        
        # Conseils personnalisés
        st.header("💡 Conseils pour votre installation")
        if moyenne_journaliere > 14:
            st.success(f"Avec une production moyenne de {moyenne_journaliere:.2f} kWh/j, "
                       "votre installation pourrait couvrir la totalité des besoins énergétiques de votre maison !")
        else:
            st.info(f"Avec une production moyenne de {moyenne_journaliere:.2f} kWh/j, "
                    "vous pourriez envisager d'ajouter des panneaux supplémentaires.")
        
        st.markdown("""
        - **Orientation optimale** : Sud à 30° d'inclinaison
        - **Entretien** : Nettoyage annuel recommandé
        - **Subventions** : Jusqu'à 50% de crédit d'impôt
        """)
        
        
        # Bouton nouvelle simulation
        st.markdown("---")
        if st.button("🔄 Effectuer une nouvelle simulation", use_container_width=True):
            st.session_state.page = "simulation"
            st.rerun()