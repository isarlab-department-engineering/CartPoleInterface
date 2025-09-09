import os
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import filedialog
from typing import Any


class ModelManagerGUI:
    """
    Classe statica che gestisce l'interazione tra l'interfaccia grafica Tkinter e i modelli
    di reinforcement learning.

    Funzionalità principali:
        - Salvataggio e caricamento di file modello (.zip)
        - Avvio dell'addestramento tramite un oggetto runner esterno
        - Esecuzione di simulazioni
        - Integrazione con contesti Real e Sim-to-Real

    Tutti i metodi sono statici o di classe e non richiedono istanza.
    """

    @staticmethod
    def save_file() -> str | None:
        """
        Apre una finestra di dialogo per selezionare dove salvare un file .zip.

        Returns:
            str | None: Percorso selezionato dall'utente, oppure None se annullato.
        """
        root = None
        try:
            root = tk.Tk()
            root.withdraw()
            root.update()

            file_path = fd.asksaveasfilename(
                title="Salva il file come",
                defaultextension=".zip",
                filetypes=[("File ZIP", "*.zip"), ("Tutti i file", "*.*")]
            )
        finally:
            root.destroy()

        return file_path if file_path else None

    @staticmethod
    def choose_file() -> str:
        """
        Apre una finestra di dialogo per selezionare un file .zip esistente.

        Returns:
            str | None: Percorso del file scelto, oppure None se annullato.
        """
        root = tk.Tk()
        root.withdraw()
        root.update()

        file_path = filedialog.askopenfilename(
            title="Scegliere un set di dati di allenamento",
            filetypes=[("File zip", "*.zip")]
        )

        return file_path if file_path else None

    @staticmethod
    def on_train_model(gui_instance, train_steps: int, verbose: int, log_interval: int) -> Any | None:
        """
        Avvia l'addestramento del modello tramite il runner integrato nella GUI.

        Args:
            gui_instance: Oggetto GUI che contiene un attributo `runner` con metodo `train(...)`.
            train_steps (int): Numero di passi di addestramento.
            verbose (int): Livello di dettaglio nei log.
            log_interval (int): Frequenza dei log durante l'addestramento.

        Returns:
            str | None: Percorso del modello salvato, oppure None se non salvato.
        """
        if train_steps != -1 and log_interval != -1:
            saved_path = gui_instance.runner.train(
                learning_step=train_steps,
                verbose=verbose,
                log_interval=log_interval,
                learning_rate=4e-4,
                ent_coef='auto',
                buffer_size=1_000_000,
                batch_size=512,
                tau=0.005,
                gamma=0.99
            )

            if saved_path:
                print(f"[SUCCESS] Addestramento completato, modello salvato in: {saved_path}")
                return saved_path
        else:
            print("log_interval o train_steps non  sono valori accettabili")



        print("[WARNING] Addestramento terminato senza salvare un modello. ")

        return None

    @staticmethod
    def simulate_model(current_model_path: str, runner, num_of_step: int) -> None:
        """
        Esegue la simulazione del modello caricato per un numero definito di passi.

        Args:
            current_model_path (str): Percorso del file modello .zip.
            runner: Oggetto con metodo `run(steps: int)` per simulazione.
            num_of_step (int): Numero di passi da simulare.

        Returns:
            None
        """
        if not current_model_path or not os.path.isfile(current_model_path):
            print("NESSUN MODELLO CARICATO O IL PERCORSO NON È VALIDO")
            return

        print("Modello caricato, procedo con la simulazione...")
        runner.run(num_of_step)

    @staticmethod
    def on_carica_modello(gui_instance) -> None:
        """
        Carica un file modello scelto tramite dialog e lo associa al runner nella GUI.

        Args:
            gui_instance: Oggetto GUI contenente:
                - model_name_var (tk.StringVar)
                - current_model_path (str)
                - runner con metodo `load(filepath)`
        """
        filepath = fd.askopenfilename(
            title="Seleziona il file del modello",
            filetypes=[("Cartelle", "*.zip"), ("Tutti i file", "*.*")]
        )

        if not filepath:
            return

        nome_file = os.path.basename(filepath)
        gui_instance.model_name_var.set(nome_file)
        gui_instance.current_model_path = filepath
        gui_instance.runner.load(filepath)

    @staticmethod
    def on_carica_modello_sim_to_real(gui_instance) -> None:
        """
        Carica un file modello per l'utilizzo in contesto Sim-to-Real e aggiorna il Context globale.

        Args:
            gui_instance: Oggetto GUI con attributo `model_name_var_sim_to_real`.
        """
        filepath = fd.askopenfilename(
            title="Seleziona il file del modello",
            filetypes=[("Cartelle", "*.zip"), ("Tutti i file", "*.*")]
        )

        if not filepath:
            return

        nome_file = os.path.basename(filepath)
        gui_instance.model_name_var_sim_to_real.set(nome_file)

        from GUI.ArduinoGui import PyArduinoGUIView
        PyArduinoGUIView.sim_to_real_met = filepath

        from Context.AppContext import Mantieni_context
        Mantieni_context.change_instance("path_modello", filepath)

    @classmethod
    def on_open_new_gui(cls):
        """
        Apre una nuova GUI per il fine-tuning, se le condizioni di contesto sono rispettate.

        Verifica la presenza di:
            - 'ser' nel Mantieni_context (seriale arduino attivo)
            - 'path_modello' (modello caricato)
        """
        from Context.AppContext import Mantieni_context

        if Mantieni_context.exists("ser") and Mantieni_context.exists("path_modello"):
            from GUI.FineTuningGUI.RealTuningGUI import FineTuningGUI
            FineTuningGUI().run()
        else:
            print("ERRORE parametri non rispettati per accedere a questa sezione consultare la documentazione")


