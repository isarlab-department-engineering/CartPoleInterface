import time
import tkinter as tk
from Context.AppContext import Mantieni_context


class FineTuningGUI:
    """
    Interfaccia grafica per gestire il fine tuning di un modello,
    utilizzando tkinter come framework GUI e Mantieni_context per
    gestire lo stato e le azioni di controllo.
    """

    def __init__(self, title="Fine Tuning", width=500, height=300):
        """
        Inizializza la finestra principale della GUI con titolo e dimensioni specificate.
        Se alcune variabili di contesto non sono presenti, avvia una sequenza di comandi
        e inizializza i widget, altrimenti mostra un messaggio di errore.

        Args:
            title (str): Titolo della finestra.
            width (int): Larghezza della finestra.
            height (int): Altezza della finestra.
        """
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        #self.root.resizable(False, False)

        if not (Mantieni_context.exists("Enable") or
                Mantieni_context.exists("home_value") or
                Mantieni_context.exists("move_center_value") or
                Mantieni_context.exists("mode_value") or
                Mantieni_context.exists("enable_control_value")):

            self.root.after(100, lambda: self.mandacomandi())
            self.inizializza_widget()

        else:
            self.label = tk.Label(
                self.root,
                text="Pagina non disponibile per config di init.\nSegnali impropri per la funzione.\nRiavviare il programma.",
                font=("Arial", 14)
            )
            self.label.pack(pady=20)

    def mandacomandi(self):
        """
        Esegue una sequenza di comandi predefiniti tramite Mantieni_context,
        simulando l'attivazione di diversi pulsanti con pause temporali.
        Gestisce eventuali eccezioni e ripristina il cursore della finestra.
        """
        try:
            Mantieni_context.get("holder_buttons")("Enable")
            time.sleep(0.2)

            Mantieni_context.get("holder_buttons")("Home")
            time.sleep(1.5)

            Mantieni_context.get("holder_buttons")("Move Center")
            time.sleep(1.5)

            Mantieni_context.get("holder_buttons")("Mode")

        except Exception as e:
            print(f"Errore durante mandacomandi: {e}")

        finally:
            # Ripristina interattività
            self.root.config(cursor="")

    def inizializza_widget(self):
        """
        Crea e posiziona i widget principali della GUI: i pulsanti per
        avviare e fermare il training del modello.
        """
        # Pulsante "Avvia training"
        btn_avvia = tk.Button(self.root, text="Avvia training", command=self._avvia_modello)
        btn_avvia.pack(pady=10)

        # Pulsante "Stop"
        btn_stop = tk.Button(self.root, text="Stop", command=self._termina_modello)
        btn_stop.pack(pady=10)

    def run(self):
        """
        Avvia il ciclo principale dell'interfaccia grafica.
        """
        self.root.mainloop()

    @staticmethod
    def _avvia_modello():
        """
        Metodo statico che modifica il contesto per segnalare l'inizio
        del training del modello e attiva il controllo abilitato.
        """
        Mantieni_context.change_instance("FLAG_PER_ALLENAMENTO", True)
        Mantieni_context.change_instance("SAVE_MODELLO_REAL", False)
        Mantieni_context.get("holder_buttons")("Enable Control")

    @staticmethod
    def _termina_modello():
        """
        Metodo statico che modifica il contesto per segnalare la fine
        del training del modello, disattiva il controllo se attivo e
        abilita il salvataggio del modello reale.
        """
        # se Enable control è attivo allora disattivalo
        if Mantieni_context.get("enable_control_value"):
            Mantieni_context.get("holder_buttons")("Enable Control")
        Mantieni_context.change_instance("FLAG_PER_ALLENAMENTO", False)
        Mantieni_context.change_instance("SAVE_MODELLO_REAL", True)
