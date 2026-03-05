"""
============================================================
ESPERTO 3 - PERSISTENZA DATI (csv / gestione file)
Progetto: Simulatore Mercato Azionario
Studente: [Nome Cognome]
============================================================
Questo modulo gestisce il salvataggio e il caricamento dei
dati su file CSV. Usa open(), il metodo split() e dizionari
come mostrato nel manuale Python cap.4 sez.4 e sez.5.
"""

import csv
import os


def salva_dati_csv(nome_file, titolo, prezzi):
    """
    Salva i prezzi simulati in un file CSV.

    Usa open() in modalità scrittura 'w' (manuale cap.4 sez.4)
    e il modulo csv per scrivere dati tabulari.

    Parametri:
        nome_file -- stringa con il percorso del file da creare
        titolo    -- stringa con il nome del titolo azionario
        prezzi    -- lista di float con i prezzi giornalieri

    Restituisce:
        True se il salvataggio è riuscito, False altrimenti
    """

    try:
        # open() con 'w' apre il file in scrittura (manuale cap.4 sez.4)
        # newline='' è necessario per csv su Windows (evita righe vuote)
        with open(nome_file, "w", newline="", encoding="utf-8") as f:

            # csv.writer scrive righe CSV automaticamente separando con virgole
            writer = csv.writer(f)

            # Prima riga: intestazione delle colonne
            writer.writerow(["giorno", "titolo", "prezzo"])

            # Ciclo for per scrivere ogni giorno (manuale cap.4 sez.2)
            for giorno, prezzo in enumerate(prezzi, start=1):
                writer.writerow([giorno, titolo, prezzo])

        return True

    except Exception as errore:
        print(f"Errore durante il salvataggio: {errore}")
        return False


def carica_dati_csv(nome_file):
    """
    Carica i dati da un file CSV e li organizza in un dizionario.

    Usa open() in modalità lettura 'r', split() per processare
    le stringhe e un dizionario per organizzare i dati tabulari
    (manuale Python cap.4 sez.4 e sez.5, cap.9 contenitori).

    Parametri:
        nome_file -- stringa con il percorso del file da leggere

    Restituisce:
        dati -- dizionario con chiavi 'giorni', 'titolo', 'prezzi'
        oppure None se il file non esiste o è vuoto
    """

    # Verifica che il file esista prima di aprirlo
    if not os.path.exists(nome_file):
        return None

    # Inizializziamo il dizionario che conterrà i dati letti
    # (struttura analoga all'esempio marziani.csv del manuale cap.5)
    dati = {
        "giorni":  [],    # lista dei numeri di giorno
        "titolo":  [],    # lista dei nomi del titolo
        "prezzi":  []     # lista dei prezzi
    }

    try:
        # open() con 'r' apre in lettura (manuale cap.4 sez.4)
        with open(nome_file, "r", newline="", encoding="utf-8") as f:

            reader = csv.reader(f)
            intestazione = next(reader)   # salta la prima riga (intestazione)

            # Ciclo for su ogni riga del file (manuale cap.4 sez.2)
            for riga in reader:

                # Verifica che la riga non sia vuota (manuale cap.5)
                if len(riga) < 3 or "" in riga:
                    continue  # salta le righe incomplete

                # Estraiamo i campi dalla riga
                # La conversione da stringa a int/float è fondamentale
                # (manuale cap.10 sez. conversioni di tipo)
                giorno = int(riga[0])
                titolo = riga[1]
                prezzo = float(riga[2])    # float() converte la stringa

                # Aggiungiamo i valori alle liste del dizionario
                dati["giorni"].append(giorno)
                dati["titolo"].append(titolo)
                dati["prezzi"].append(prezzo)

        # Se il file era vuoto restituiamo None
        if len(dati["prezzi"]) == 0:
            return None

        return dati

    except Exception as errore:
        print(f"Errore durante il caricamento: {errore}")
        return None


def formatta_dati_per_output(dati):
    """
    Converte il dizionario caricato in una stringa leggibile.

    Usa un ciclo for e f-string (manuale cap.7) per costruire
    la rappresentazione testuale dei dati.

    Parametri:
        dati -- dizionario restituito da carica_dati_csv()

    Restituisce:
        testo -- stringa formattata pronta per la GUI
    """

    titolo = dati["titolo"][0] if dati["titolo"] else "N/D"
    righe = [f"📂 Dati caricati per il titolo: {titolo}",
             f"{'─' * 38}",
             f"{'Giorno':<10} {'Prezzo (€)':>12}"]

    # Scorrimento parallelo di giorni e prezzi con zip
    for giorno, prezzo in zip(dati["giorni"], dati["prezzi"]):
        righe.append(f"{giorno:<10} {prezzo:>12.2f}")

    return "\n".join(righe)