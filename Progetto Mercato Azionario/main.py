"""
============================================================
MAIN - APP PRINCIPALE (integrazione dei 4 moduli)
Progetto: Simulatore Mercato Azionario
Gruppo: [Nome del gruppo]
============================================================
Questo file assembla i contributi dei 4 esperti in un'unica
applicazione funzionante. Rappresenta la Fase 2 del Jigsaw.

Struttura dell'app:
  1. esperto1_gui        --> finestra e widget tkinter
  2. esperto2_simulazione --> generazione prezzi casuali
  3. esperto3_csv         --> salvataggio e caricamento file
  4. esperto4_calcolo     --> classe DataAnalyzer (OOP + math)
"""

import tkinter as tk

# Importiamo i moduli sviluppati dai 4 esperti
import esperto1_gui        as gui
import esperto2_simulazione as sim
import esperto3_csv        as csv_mod
import esperto4_calcolo    as calc


# ── Variabili globali condivise tra le funzioni callback ──────────────────────
# Le variabili globali (manuale cap.4 sez.3 scope) sono visibili
# a tutte le funzioni di questo modulo.
prezzi_correnti = []    # lista dei prezzi generati
titolo_corrente = ""    # nome del titolo corrente
nome_file_csv   = "mercato_azionario.csv"


# ── Funzioni callback (collegate ai bottoni dalla GUI) ────────────────────────

def callback_genera():
    """
    Chiamata quando l'utente clicca su 'Genera Prezzi'.
    Legge gli input, valida, genera i prezzi e li mostra.
    """
    global prezzi_correnti, titolo_corrente

    # Leggiamo i valori dalle Entry della GUI
    # .get() è il metodo dei widget Entry per leggere il testo inserito
    titolo_str = entry_titolo.get().strip().upper()
    giorni_str = entry_giorni.get().strip()

    # Validazione degli input (delegata all'esperto 2)
    try:
        prezzo_iniziale, num_giorni = sim.valida_input("100.0", giorni_str)
    except ValueError as errore:
        gui.mostra_errore("Input non valido", str(errore))
        return

    # Se il titolo è vuoto usiamo un nome di default
    if not titolo_str:
        titolo_str = "TITOLO"

    # Generiamo i prezzi con il modulo dell'esperto 2
    prezzi_correnti = sim.genera_prezzi(prezzo_iniziale=100.0, num_giorni=num_giorni)
    titolo_corrente = titolo_str

    # Costruiamo il testo da mostrare nella GUI
    # Ciclo for con enumerate (manuale cap.4 sez.2) per numerare i giorni
    righe = [f"🎲 Prezzi simulati per {titolo_corrente}",
             f"{'─' * 38}",
             f"{'Giorno':<10} {'Prezzo (€)':>12}"]

    for giorno, prezzo in enumerate(prezzi_correnti, start=1):
        righe.append(f"{giorno:<10} {prezzo:>12.2f}")

    # Classifichiamo il segnale (esperto 2)
    segnale, variaz = sim.classifica_segnale(prezzi_correnti[0], prezzi_correnti[-1])
    righe.append(f"\n{'─' * 38}")
    righe.append(f"Segnale finale: {segnale}")
    righe.append(f"Variazione tot: {variaz:+.2f}%")

    # Aggiorniamo la GUI con il risultato (esperto 1)
    gui.aggiorna_output(testo_output, "\n".join(righe))


def callback_analizza():
    """
    Chiamata quando l'utente clicca su 'Analizza'.
    Usa la classe DataAnalyzer (esperto 4) per calcolare le statistiche.
    """
    global prezzi_correnti, titolo_corrente

    # Verifichiamo che ci siano dati da analizzare
    if not prezzi_correnti:
        gui.mostra_errore("Nessun dato", "Prima genera i prezzi con il bottone 'Genera Prezzi'!")
        return

    # Creiamo un oggetto DataAnalyzer (istanziamo la classe, manuale cap.6)
    analizzatore = calc.DataAnalyzer(titolo_corrente, prezzi_correnti)

    # Chiediamo all'oggetto di generare il report formattato
    report = analizzatore.formatta_report()

    # Mostriamo il report nella GUI
    gui.aggiorna_output(testo_output, report)


def callback_salva():
    """
    Chiamata quando l'utente clicca su 'Salva CSV'.
    Usa il modulo dell'esperto 3 per scrivere il file.
    """
    global prezzi_correnti, titolo_corrente, nome_file_csv

    if not prezzi_correnti:
        gui.mostra_errore("Nessun dato", "Prima genera i prezzi con il bottone 'Genera Prezzi'!")
        return

    # Salviamo il file (delegato all'esperto 3)
    successo = csv_mod.salva_dati_csv(nome_file_csv, titolo_corrente, prezzi_correnti)

    if successo:
        gui.mostra_info("Salvato!", f"Dati salvati in '{nome_file_csv}'")
        gui.aggiorna_output(testo_output,
            f"✅ File '{nome_file_csv}' salvato con successo!\n"
            f"   Titolo: {titolo_corrente}\n"
            f"   Giorni: {len(prezzi_correnti)}\n"
            f"   Prezzi da € {prezzi_correnti[0]:.2f} a € {prezzi_correnti[-1]:.2f}"
        )
    else:
        gui.mostra_errore("Errore", "Impossibile salvare il file.")


def callback_carica():
    """
    Chiamata quando l'utente clicca su 'Carica CSV'.
    Usa il modulo dell'esperto 3 per leggere il file.
    """
    global prezzi_correnti, titolo_corrente, nome_file_csv

    # Carichiamo i dati (delegato all'esperto 3)
    dati = csv_mod.carica_dati_csv(nome_file_csv)

    if dati is None:
        gui.mostra_errore("File non trovato",
            f"Il file '{nome_file_csv}' non esiste.\nGenera e salva prima i dati.")
        return

    # Aggiorniamo le variabili globali con i dati caricati
    prezzi_correnti = dati["prezzi"]
    titolo_corrente = dati["titolo"][0] if dati["titolo"] else "N/D"

    # Formattiamo e mostriamo i dati (esperto 3)
    testo = csv_mod.formatta_dati_per_output(dati)
    gui.aggiorna_output(testo_output, testo)
    gui.mostra_info("Caricato!", f"Dati di {titolo_corrente} caricati ({len(prezzi_correnti)} giorni)")


# ── Avvio dell'applicazione ───────────────────────────────────────────────────

if __name__ == "__main__":
    """
    Punto di ingresso del programma.
    Questo blocco viene eseguito solo se avviamo direttamente questo file,
    non quando lo importiamo come modulo.
    """

    # Creiamo la finestra principale con tkinter
    root = tk.Tk()
    root.title("📈 Simulatore Mercato Azionario")
    root.geometry("650x580")
    root.configure(bg="#1a1a2e")
    root.resizable(False, False)

    # Costruiamo l'interfaccia (esperto 1) passando le nostre callback
    # Le callback collegano i bottoni della GUI alle funzioni definite qui sopra
    entry_titolo, entry_giorni, testo_output = gui.crea_interfaccia(
        root,
        callback_genera=callback_genera,
        callback_analizza=callback_analizza,
        callback_salva=callback_salva,
        callback_carica=callback_carica
    )

    # Messaggio di benvenuto nell'area output
    gui.aggiorna_output(testo_output,
        "Benvenuto nel Simulatore Mercato Azionario!\n\n"
        "Come usare l'app:\n"
        "  1. Inserisci il nome del titolo (es. ACME)\n"
        "  2. Scegli quanti giorni simulare (es. 10)\n"
        "  3. Clicca 'Genera Prezzi' per la simulazione\n"
        "  4. Clicca 'Analizza' per le statistiche\n"
        "  5. Clicca 'Salva CSV' per esportare i dati\n"
        "  6. Clicca 'Carica CSV' per rileggere un file salvato\n"
    )

    # Avviamo il loop degli eventi di tkinter (mantiene la finestra aperta)
    root.mainloop()