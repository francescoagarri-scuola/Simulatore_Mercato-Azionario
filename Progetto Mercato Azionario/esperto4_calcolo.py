"""
============================================================
ESPERTO 4 - CALCOLO E STRUTTURA (math + OOP)
Progetto: Simulatore Mercato Azionario
Studente: [Nome Cognome]
============================================================
Questo modulo definisce la classe DataAnalyzer che incapsula
i dati e offre metodi statistici.
Usa il modulo 'math' e i principi OOP (manuale cap.6).
"""

import math


class DataAnalyzer:
    """
    Classe che incapsula una serie di prezzi azionari e offre
    metodi per l'analisi statistica.

    Attributi:
        self.titolo   -- stringa con il nome del titolo
        self.prezzi   -- lista di float con i prezzi giornalieri
        self.giorni   -- int, numero di giorni simulati

    Esempio di utilizzo:
        analizzatore = DataAnalyzer("ACME", [100.0, 102.5, 98.3])
        print(analizzatore.media())
    """

    def __init__(self, titolo, prezzi):
        """
        Costruttore della classe (manuale cap.6 sez.6).
        Viene eseguito automaticamente quando si crea un oggetto.

        Parametri:
            titolo  -- stringa con il nome del titolo azionario
            prezzi  -- lista di float con i prezzi giornalieri
        """
        # Gli attributi si definiscono con 'self.' (manuale cap.6)
        self.titolo = titolo
        self.prezzi = prezzi
        self.giorni = len(prezzi)

    def media(self):
        """
        Calcola il prezzo medio del periodo.

        Restituisce:
            float -- media aritmetica dei prezzi
        """
        # Verifica che ci siano dati (manuale cap.4 sez.1 if...else)
        if self.giorni == 0:
            return 0.0

        somma = sum(self.prezzi)
        return round(somma / self.giorni, 2)

    def deviazione_standard(self):
        """
        Calcola la deviazione standard dei prezzi.
        Indica la volatilità del titolo: più alta = più rischioso.

        Usa math.sqrt() per la radice quadrata.

        Restituisce:
            float -- deviazione standard
        """
        if self.giorni < 2:
            return 0.0

        media_val = self.media()

        # Varianza = media degli scarti quadratici dalla media
        # List comprehension (manuale cap.8) per calcolare gli scarti
        scarti_quadratici = [(p - media_val) ** 2 for p in self.prezzi]
        varianza = sum(scarti_quadratici) / self.giorni

        # math.sqrt() calcola la radice quadrata (manuale cap.3 sez.5)
        return round(math.sqrt(varianza), 2)

    def prezzo_minimo(self):
        """
        Restituisce il prezzo minimo registrato nel periodo.

        Restituisce:
            (valore, giorno) -- tupla con prezzo e numero del giorno
        """
        if self.giorni == 0:
            return (0.0, 0)

        valore_min = min(self.prezzi)
        giorno_min = self.prezzi.index(valore_min) + 1   # +1 perché l'indice parte da 0
        return (valore_min, giorno_min)

    def prezzo_massimo(self):
        """
        Restituisce il prezzo massimo registrato nel periodo.

        Restituisce:
            (valore, giorno) -- tupla con prezzo e numero del giorno
        """
        if self.giorni == 0:
            return (0.0, 0)

        valore_max = max(self.prezzi)
        giorno_max = self.prezzi.index(valore_max) + 1
        return (valore_max, giorno_max)

    def rendimento_totale(self):
        """
        Calcola il rendimento percentuale totale del periodo
        (dal primo all'ultimo giorno).

        Restituisce:
            float -- rendimento percentuale
        """
        if self.giorni < 2:
            return 0.0

        prezzo_start = self.prezzi[0]
        prezzo_end   = self.prezzi[-1]   # [-1] è l'ultimo elemento (manuale cap.8 slicing)
        rendimento = ((prezzo_end - prezzo_start) / prezzo_start) * 100
        return round(rendimento, 2)

    def formatta_report(self):
        """
        Genera una stringa con il report completo dell'analisi.

        Usa f-string (manuale cap.7) per formattare l'output.

        Restituisce:
            stringa con il report formattato
        """
        min_val, min_gg   = self.prezzo_minimo()
        max_val, max_gg   = self.prezzo_massimo()
        rend              = self.rendimento_totale()

        # Simbolo grafico per il rendimento
        simbolo = "📈" if rend >= 0 else "📉"

        report = (
            f"╔══════════════════════════════════════╗\n"
            f"║   ANALISI TITOLO: {self.titolo:<18} ║\n"
            f"╠══════════════════════════════════════╣\n"
            f"║  Giorni simulati  : {self.giorni:<18} ║\n"
            f"║  Prezzo iniziale  : € {self.prezzi[0]:<16.2f} ║\n"
            f"║  Prezzo finale    : € {self.prezzi[-1]:<16.2f} ║\n"
            f"║  Prezzo medio     : € {self.media():<16.2f} ║\n"
            f"║  Volatilità (dev) : € {self.deviazione_standard():<16.2f} ║\n"
            f"║  Minimo  (gg {min_gg:>3}) : € {min_val:<16.2f} ║\n"
            f"║  Massimo (gg {max_gg:>3}) : € {max_val:<16.2f} ║\n"
            f"║  Rendimento tot.  : {simbolo} {rend:>+.2f}%{'':<10} ║\n"
            f"╚══════════════════════════════════════╝"
        )
        return report