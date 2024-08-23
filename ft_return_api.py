import os
from datetime import datetime

def convert_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Séparer le contenu par "start_date_time"
    entries = content.split("charge_station_id")

    # Enlever les éventuelles entrées vides
    entries = [entry.strip() for entry in entries if entry.strip()]

    # Ajouter "start_date_time" au début de chaque entrée sauf la première
    entries = [f"charge_station_id{entry}" if i != 0 else entry for i, entry in enumerate(entries)]

    # Écrire les entrées dans le fichier CSV
    with open(output_file, 'w', encoding='utf-8') as file:
        for entry in entries:
            file.write(entry + '\n')
        print(f"CSV content has been written to {output_file}")


def create_file_API(response_text):
    # Créer le dossier "resultat" s'il n'existe pas
    if not os.path.exists('resultat'):
        os.makedirs('resultat')

    # Obtenir la date et l'heure actuelles pour le filename
    current_time = datetime.now()
    file_name = "Chargestations_" + current_time.strftime("%d_%m_%Y_%H_%M")

    # Vérifier si le fichier existe déjà avec la même heure
    # sinon incrémenter un compteur à la fin pour le rendre unique
    counter = 1
    base_name = file_name
    while os.path.exists(f"resultat/{file_name}.txt"):
        file_name = f"{base_name}_{counter}"
        counter += 1

    # html récupéré dans soup.prettify
    with open(f"resultat/{file_name}.txt", 'w', encoding='utf-8') as file:
        file.write(response_text)
        print(f"HTML content has been written to resultat/{file_name}.txt")

     # Transformer le fichier texte en CSV
    convert_to_csv(f"resultat/{file_name}.txt", f"resultat/{file_name}.csv")
