import openmeteo_requests
from datetime import datetime
import pandas as pd
import requests_cache
from retry_requests import retry
import requests
from Demandes_utilisateur import obtenir_donnees_utilisateur


cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_irradiance_data(date_debut, date_fin, latitude, longitude):
    

    if latitude is None or longitude is None:
        print("Erreur : Impossible d'obtenir les coordonnées de la ville.")
        return None

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "shortwave_radiation",
        "start_date": date_debut.strftime("%Y-%m-%d"),
        "end_date": date_fin.strftime("%Y-%m-%d")
    }
    
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

 
    hourly = response.Hourly()
    hourly_shortwave_radiation = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "shortwave_radiation": hourly_shortwave_radiation
    }

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe.to_csv("donnees_irradiation.csv", index=False)

    return hourly_dataframe  


if __name__ == "__main__":
    df = get_irradiance_data()
    if df is not None:
        print(df.head()) 

