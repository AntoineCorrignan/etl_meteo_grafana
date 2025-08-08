import streamlit as st
import streamlit.components.v1 as components

# --- Titre et description de l'application ---
st.set_page_config(
    page_title="Dashboard Météo",
    page_icon="☀️",
    layout="wide"
)

st.title("Dashboard Météo de Nantes")
st.write("""
Bienvenue sur le tableau de bord météo. Ce dashboard affiche les données extraites
de l'API OpenWeatherMap et stockées dans une base de données Neon.
""")

# --- Intégration du dashboard Grafana ---
grafana_url = "https://antoinecorrignan.grafana.net/dashboard/snapshot/SINQ3An0NrBMO0ZW7Xq598dzEbiyTlyB"


# Le code HTML de l'iframe
grafana_iframe_html = f"""
<iframe 
    src="{grafana_url}"
    width="100%"
    height="600"
    frameborder="0"
></iframe>
"""

# Affichage de l'iframe dans l'application Streamlit
# On utilise la fonction 'html' pour interpréter le code HTML
components.html(grafana_iframe_html, height=620)

# --- Section d'information supplémentaire ---
st.markdown("---")
st.header("À propos des données")
st.write("Les données sont collectées toutes les 30 minutes via un pipeline ETL automatisé avec GitHub Actions.")