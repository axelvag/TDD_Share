import csv

def create_taux_de_dispo_csv(taux_de_dispo):
    with open('taux_de_dispo.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Autoroutes", taux_de_dispo.nb_autoroute, taux_de_dispo.pourcent_autoroute])

def ft_count_nb_pdc_total(line_brut):
    nb = line_brut.count('evse_id')
    return nb

def ft_count_nb_pdc_available(line_brut):
    nb_available = line_brut.count('AVAILABLE')
    nb_charging = line_brut.count('CHARGING')
    if (nb_available + nb_charging == 0):
        res = 0
    else:
        # -1 car il y a un AVAILABLE ecrit a chaque fois
        res = nb_available + nb_charging - 1
    return res

def ft_create_csv(tab, somme_total_pdc, somme_total_pdc_available, pourcent_total_dispo):
    # Write the entries to a CSV file
    with open('charge_station.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write entete
        writer.writerow(["1. Charge Point ID", "2. Nb PDC Theorique par station", "3. Nb PDC Dispo par station", "4. % PDC dispo par station", "5. Tout les PDC prod", "6. Tout les PDC dispo prod", "7. % PDC dispo"])

        # Write each column as a new line in tab the CSV file
        for line in tab:
            writer.writerow([line[0], line[1], line[2], line[3], somme_total_pdc, somme_total_pdc_available, pourcent_total_dispo])
    
    print("CSV content has been written to charge_station_ids.csv")

def create_line_csv(response_text):
    # Split par le mot charge_station_id
    text = response_text.split('charge_station_id')
    
    # tab a mettre en csv
    tab = []
    somme_total_pdc = 0
    somme_total_pdc_available = 0

    # pour chaque ligne
    for line_brut in text:
        # if line_brut.strip() and 'Production' in line_brut:  # Pour enlever les No prod
        if line_brut.strip():  # si elle est pas vide
            # trouve le premier : pour recuperer charge_station_id
            start_index = line_brut.find(':') + 2
            # trouve la fin du char_station_id
            end_index = line_brut.find('"', start_index)
            if start_index != -1 and end_index != -1:
                # 1. Charge Point ID, recupere la val du charge_station_id
                charge_station_id = line_brut[start_index:end_index]

                # 2. Nb PDC Theorique par station, recupere le nb de point de charge total
                nb_pdc_total = ft_count_nb_pdc_total(line_brut)

                # 3. Nb PDC Dispo par station, recupere le nb de point de charge available
                nb_pdc_available = ft_count_nb_pdc_available(line_brut)

                # 4. % PDC dispo par station
                pourcent_pdc_dispo_par_station = int((nb_pdc_available * 100 / nb_pdc_total) if nb_pdc_total > 0 else 0)
                pourcent_pdc_dispo_par_station = f"{pourcent_pdc_dispo_par_station}%"

                # je ne compte que les borne en prod
                if 'Production' in line_brut:
                    # 5. Tout les PDC prod, somme de tout les pdc peut importe le status
                    somme_total_pdc += nb_pdc_total

                    # 6. Tout les PDC dispo prod, somme de tout les pdc available
                    somme_total_pdc_available += nb_pdc_available

                # 7. % PDC dispo
                pourcent_total_dispo = int((somme_total_pdc_available * 100 / somme_total_pdc) if somme_total_pdc > 0 else 0)
                pourcent_total_dispo = f"{pourcent_total_dispo}%"

                tab.append((charge_station_id, nb_pdc_total, nb_pdc_available, pourcent_pdc_dispo_par_station))
    
    # je ne met pas les somme dans append sinon il s'incrémente a chaque ligne
    ft_create_csv(tab, somme_total_pdc, somme_total_pdc_available, pourcent_total_dispo)