"""
============================================================
ESPERTO 2 - SIMULAZIONE E LOGICA (random)
Progetto: Simulatore Mercato Azionario
Studente: [Nome Cognome]
============================================================
Questo modulo genera simulazioni casuali di prezzi azionari.
Usa il modulo 'random' per creare variazioni di prezzo e
il costrutto if...elif...else per classificare i segnali.
"""

import random as rnd


def genera_prezzi(prezzo_iniziale, num_giorni):
    """
    Genera una lista di prezzi simulati per un titolo azionario.

    Usa una list comprehension (manuale Python cap.8) per creare
    in modo rapido la lista delle variazioni giornaliere.

    Parametri:
        prezzo_iniziale -- float, prezzo di partenza del titolo
        num_giorni      -- int, quanti giorni simulare

    Restituisce:
        prezzi -- lista di float con i prezzi giorno per giorno
    """

    # Usiamo il ciclo for (manuale Python cap.4 sez.2) per costruire
    # la lista: ogni giorno il prezzo cambia di una % casuale tra -5% e +5%
    prezzi = []                       # lista vuota da riempire
    prezzo_corrente = prezzo_iniziale

    for _ in range(num_giorni):       # _ perché l'indice non ci serve
        # rnd.uniform genera un float casuale tra due valori (estremi inclusi)
        variazione_percentuale = rnd.uniform(-5.0, 5.0)
        prezzo_corrente = prezzo_corrente * (1 + variazione_percentuale / 100)
        prezzo_corrente = round(prezzo_corrente, 2)   # arrotondiamo a 2 decimali
        prezzi.append(prezzo_corrente)

    return prezzi


def classifica_segnale(prezzo_iniziale, prezzo_finale):
    """
    Classifica l'andamento del titolo con un segnale di trading.

    Usa il costrutto if...elif...else (manuale Python cap.4 sez.1)
    per valutare la variazione percentuale totale.

    Parametri:
        prezzo_iniziale -- float, prezzo del primo giorno
        prezzo_finale   -- float, prezzo dell'ultimo giorno

    Restituisce:
        segnale -- stringa con la classificazione
    """

    # Calcoliamo la variazione percentuale totale
    variazione = ((prezzo_finale - prezzo_iniziale) / prezzo_iniziale) * 100

    # Classificazione con if...elif...else
    if variazione > 10:
        segnale = "🚀 FORTE RIALZO  (variazione > +10%)"
    elif variazione > 3:
        segnale = "📈 RIALZO         (variazione > +3%)"
    elif variazione > -3:
        segnale = "➡️  STABILE        (variazione tra -3% e +3%)"
    elif variazione > -10:
        segnale = "📉 RIBASSO        (variazione < -3%)"
    else:
        segnale = "💥 FORTE RIBASSO  (variazione < -10%)"

    return segnale, round(variazione, 2)


def calcola_variazioni_giornaliere(prezzi):
    """
    Calcola la variazione percentuale tra ogni giorno consecutivo.

    Usa una list comprehension con zip per scorrere coppie
    di giorni adiacenti.

    Parametri:
        prezzi -- lista di float

    Restituisce:
        variazioni -- lista di float (variazioni %)
    """

    # zip(prezzi, prezzi[1:]) crea coppie (giorno_i, giorno_i+1)
    # È un uso avanzato della list comprehension (manuale cap.8)
    variazioni = [
        round(((p2 - p1) / p1) * 100, 2)
        for p1, p2 in zip(prezzi, prezzi[1:])
    ]
    return variazioni


def valida_input(prezzo_str, giorni_str):
    """
    Valida gli input dell'utente convertendoli nei tipi corretti.

    Applica la conversione stringa -> float/int (manuale cap.10)
    e usa if...else per gestire valori non validi.

    Parametri:
        prezzo_str -- stringa inserita dall'utente (prezzo)
        giorni_str -- stringa inserita dall'utente (giorni)

    Restituisce:
        (prezzo, giorni) -- tupla con i valori convertiti
        oppure solleva ValueError se i dati non sono validi
    """

    # float() converte stringa in numero decimale (manuale cap.10)
    try:
        prezzo = float(prezzo_str)
        giorni = int(giorni_str)
    except ValueError:
        raise ValueError("Prezzo e giorni devono essere numeri validi!")

    # Controllo range con if...elif...else
    if prezzo <= 0:
        raise ValueError("Il prezzo iniziale deve essere maggiore di zero!")
    elif giorni < 2:
        raise ValueError("Servono almeno 2 giorni di simulazione!")
    elif giorni > 365:
        raise ValueError("Il massimo consentito è 365 giorni!")
    else:
        return prezzo, giorni