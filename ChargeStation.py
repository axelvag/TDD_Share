import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from ft_return_api import create_file_API
from ft_create_taux_de_dispo import create_taux_de_dispo_csv, create_line_csv

# supprimer les warning ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# INFO sur cette API
# https://developer.greenflux.com/ChargeStation
# l'url doit avoir version=1.0
# je les passent soit par params soit direct dans l'url

load_dotenv()
YOUR_API_KEY = os.getenv('YOUR_API_KEY')

class TauxDeDispo:
    def __init__(self):
        self.nb_autoroute = 0
        self.pourcent_autoroute = 0

def count_taux_de_dispo_autoroute(response_text, taux_de_dispo):
    # Compter le nombre d'occurrences de 'charge_point_model:"SICHARGE D"'
    # count = response_text.count('SICHARGE D')

    count_sicharge_d = 0
    count_available_charging = 0
    
    # Split the text by 'charge_station_id' to get individual charge station entries
    entries = response_text.split('charge_station_id')
    
    # Iterate through each entry to check for conditions
    for entry in entries:
        # Check if 'production' and 'SICHARGE D' sont dans la meme ligne
        if 'Production' in entry and 'SICHARGE D' in entry:
            count_sicharge_d += 1
            if 'AVAILABLE' in entry or 'CHARGING' in entry:
                count_available_charging += 1

    # Met le nombre de borne autoroute AVAILABLE en pourcent
    pourcent_autoroute = (count_available_charging * 100 / count_sicharge_d) if count_sicharge_d > 0 else 0

    # Afficher le résultat
    # print(f"Le nombre d'occurrences de 'charge_point_model:\"SICHARGE D\"' est : {count_sicharge_d}")
    # print(f"Le pourcentage sur autoroute est : {pourcent_autoroute}%")
    taux_de_dispo.nb_autoroute = count_sicharge_d
    taux_de_dispo.pourcent_autoroute = pourcent_autoroute

if __name__ == '__main__':
    # print(YOUR_API_KEY)

    url = "https://platform.greenflux.com/api/1.0/ChargeStations"

    headers = {
        "accept": "application/json",
        "Authorization": YOUR_API_KEY
        }

    # Define date_from and date_to
    date_to = datetime.utcnow()
    date_from = date_to - timedelta(hours=72)
    
    params = {
        "date_from": date_from.isoformat() + "Z",  # heure actuel -72h
        "date_to": date_to.isoformat() + "Z" # heure actuel
    }
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        # print(response.text)
        
        create_file_API(response.text)  # creer le fichier brut dans /resultat

        # taux_de_dispo = TauxDeDispo()
        # count_taux_de_dispo_autoroute(response.text, taux_de_dispo)
        # create_taux_de_dispo_csv(taux_de_dispo)    # creer le fichier abandonne taux_de_dispo
        
        create_line_csv(response.text)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)
