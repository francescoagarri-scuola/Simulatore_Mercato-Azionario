"""
============================================================
ESPERTO 1 - INTERFACCIA GRAFICA (tkinter)
Progetto: Simulatore Mercato Azionario
Studente: [Nome Cognome]
============================================================
Questo modulo gestisce tutta l'interfaccia grafica dell'app.
Crea la finestra principale con bottoni, etichette e area
di visualizzazione dei risultati.
"""

import tkinter as tk
from tkinter import messagebox


def crea_interfaccia(root, callback_genera, callback_analizza, callback_salva, callback_carica):
    """
    Costruisce e restituisce tutti i widget dell'interfaccia grafica.

    Parametri:
        root            -- la finestra principale (Tk)
        callback_genera -- funzione da chiamare al click di 'Genera'
        callback_analizza -- funzione da chiamare al click di 'Analizza'
        callback_salva  -- funzione da chiamare al click di 'Salva'
        callback_carica -- funzione da chiamare al click di 'Carica'

    Restituisce:
        entry_titolo   -- widget Entry per inserire il nome del titolo
        entry_giorni   -- widget Entry per inserire il numero di giorni
        testo_output   -- widget Text per visualizzare i risultati
    """

    # ----- Titolo dell'app -----
    # Label è un widget di solo testo; lo usiamo come intestazione
    etichetta_titolo = tk.Label(
        root,
        text="📈 Simulatore Mercato Azionario",
        font=("Arial", 18, "bold"),
        bg="#1a1a2e",
        fg="#e0e0e0"
    )
    etichetta_titolo.pack(pady=15)

    # ----- Frame per gli input -----
    # Un Frame raggruppa altri widget, utile per organizzare la GUI
    frame_input = tk.Frame(root, bg="#1a1a2e")
    frame_input.pack(pady=5)

    # Etichetta + campo di testo per il nome del titolo azionario
    tk.Label(frame_input, text="Titolo (es. ACME):", bg="#1a1a2e", fg="#aaaaaa",
             font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_titolo = tk.Entry(frame_input, font=("Arial", 11), width=12, bg="#2d2d44", fg="white",
                            insertbackground="white")
    entry_titolo.insert(0, "ACME")   # valore di default
    entry_titolo.grid(row=0, column=1, padx=10, pady=5)

    # Etichetta + campo di testo per il numero di giorni
    tk.Label(frame_input, text="Giorni da simulare:", bg="#1a1a2e", fg="#aaaaaa",
             font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_giorni = tk.Entry(frame_input, font=("Arial", 11), width=12, bg="#2d2d44", fg="white",
                            insertbackground="white")
    entry_giorni.insert(0, "10")     # valore di default
    entry_giorni.grid(row=1, column=1, padx=10, pady=5)

    # ----- Frame per i bottoni -----
    frame_bottoni = tk.Frame(root, bg="#1a1a2e")
    frame_bottoni.pack(pady=10)

    # Bottone GENERA: chiama la funzione callback_genera passata dall'app principale
    # Il parametro 'command' accetta una funzione; la esegue quando si clicca
    btn_genera = tk.Button(
        frame_bottoni,
        text="🎲 Genera Prezzi",
        command=callback_genera,
        font=("Arial", 11, "bold"),
        bg="#4a90d9", fg="white",
        padx=10, pady=5,
        relief="flat", cursor="hand2"
    )
    btn_genera.grid(row=0, column=0, padx=8)

    # Bottone ANALIZZA
    btn_analizza = tk.Button(
        frame_bottoni,
        text="🔍 Analizza",
        command=callback_analizza,
        font=("Arial", 11, "bold"),
        bg="#27ae60", fg="white",
        padx=10, pady=5,
        relief="flat", cursor="hand2"
    )
    btn_analizza.grid(row=0, column=1, padx=8)

    # Bottone SALVA
    btn_salva = tk.Button(
        frame_bottoni,
        text="💾 Salva CSV",
        command=callback_salva,
        font=("Arial", 11, "bold"),
        bg="#e67e22", fg="white",
        padx=10, pady=5,
        relief="flat", cursor="hand2"
    )
    btn_salva.grid(row=0, column=2, padx=8)

    # Bottone CARICA
    btn_carica = tk.Button(
        frame_bottoni,
        text="📂 Carica CSV",
        command=callback_carica,
        font=("Arial", 11, "bold"),
        bg="#8e44ad", fg="white",
        padx=10, pady=5,
        relief="flat", cursor="hand2"
    )
    btn_carica.grid(row=0, column=3, padx=8)

    # ----- Area di output (testo a scorrimento) -----
    frame_output = tk.Frame(root, bg="#1a1a2e")
    frame_output.pack(pady=10, padx=20, fill="both", expand=True)

    tk.Label(frame_output, text="📊 Output:", bg="#1a1a2e", fg="#aaaaaa",
             font=("Arial", 10)).pack(anchor="w")

    # Widget Text: mostra testo su più righe; è come un piccolo editor
    testo_output = tk.Text(
        frame_output,
        height=18, width=60,
        font=("Courier", 10),
        bg="#0d0d1a", fg="#00ff88",
        insertbackground="white",
        state="disabled"   # disabilitato: l'utente non può modificarlo direttamente
    )
    testo_output.pack(fill="both", expand=True)

    # Restituiamo i widget che l'app principale dovrà usare
    return entry_titolo, entry_giorni, testo_output


def aggiorna_output(testo_output, messaggio):
    """
    Scrive un messaggio nell'area di testo dell'interfaccia.

    Parametri:
        testo_output -- widget Text in cui scrivere
        messaggio    -- stringa da visualizzare
    """
    # Per scrivere nel widget Text bisogna prima abilitarlo (NORMAL),
    # poi scrivere, poi disabilitarlo di nuovo (DISABLED)
    testo_output.config(state="normal")
    testo_output.delete("1.0", tk.END)           # cancella il contenuto precedente
    testo_output.insert(tk.END, messaggio)        # inserisce il nuovo testo
    testo_output.config(state="disabled")


def mostra_errore(titolo, messaggio):
    """Mostra una finestra di dialogo di errore."""
    messagebox.showerror(titolo, messaggio)


def mostra_info(titolo, messaggio):
    """Mostra una finestra di dialogo informativa."""
    messagebox.showinfo(titolo, messaggio)