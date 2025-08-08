import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# ---------------------------
# CONFIGURATION
# ---------------------------
API_KEY = "6f62597e27bae77a79b8343334ae9745"
CITY = "Nantes,FR"
DB_USER = 'neondb_owner'    
DB_PASS = 'npg_Pwbo7y0GxZUc'
DB_HOST = 'ep-autumn-glitter-a2ojjm12-pooler.eu-central-1.aws.neon.tech'
DB_NAME = 'etl_project_test'
DB_PORT = 5432

# Connexion à Neon avec SSL
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
)

# ---------------------------
# EXTRACTION
# ---------------------------
print(f"📡 Récupération des données météo pour {CITY} depuis OpenWeatherMap...")
url = "https://api.openweathermap.org/data/2.5/forecast"
params = {
    "q": CITY,
    "appid": API_KEY,
    "units": "metric",  # température en °C
    "lang": "fr"
}
response = requests.get(url, params=params)
data = response.json()

# On transforme la liste des prévisions en DataFrame
records = []
for item in data["list"]:
    records.append({
        "time_utc": item["dt_txt"],
        "temperature_c": item["main"]["temp"],
        "humidity": item["main"]["humidity"],
        "weather": item["weather"][0]["description"],
        "wind_speed": item["wind"]["speed"]
    })

df = pd.DataFrame(records)
df["loaded_at"] = datetime.now()

print(f"✅ {len(df)} lignes récupérées.")

# ---------------------------
# CHARGEMENT
# ---------------------------
print("💾 Chargement dans PostgreSQL (table raw_weather)...")
df.to_sql("raw_weather", engine, if_exists="replace", index=False)
print("✅ Données chargées avec succès.")
