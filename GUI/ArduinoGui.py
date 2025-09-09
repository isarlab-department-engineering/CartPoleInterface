import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from Controllo_e_Simulazione.ModelManagerGUI import ModelManagerGUI
from Controllo_e_Simulazione.PendulumGym import SACRunner
from GUI.PyArduinoGUIController import PyArduinoGUIController


def _try_to_extract(var_to_test):
    try:
        value = var_to_test.get()
    except Exception as e:
        print(f"Errore durante l'accesso con .get(): {e}")
        return -1
    # Rifiuta int negativi
    if value < 0:
        print(f"Errore: il valore è un intero negativo ({value})")
        return -1

    return value






class PyArduinoGUIView:
    # Variabile di classe per memorizzare il percorso modello "sim-to-real"
    sim_to_real_met = None

    @classmethod
    def get_sim_to_real_met(cls):
        """Restituisce il percorso del modello sim-to-real."""
        return cls.sim_to_real_met

    def __init__(self, controller, render):
        self.current_model_path = None
        self.current_model_path_sim_to_real = None
        self.controller = controller
        self.dropdown = None
        self.porta_var = None
        self.root = tk.Tk()
        self.root.title("Interfaccia Py Arduino")
        self.root.configure(bg="#2e2e2e")  # Colore sfondo scuro
        self.runner = SACRunner(render=render)
        self._create_widgets()

    @staticmethod
    def _button_style():
        """Stile base per i bottoni."""
        return {
            'width': 20,
            'padx': 10,
            'pady': 5,
            'font': ("Helvetica", 10, "bold"),
            'bg': "#2e2e2e",
            'fg': "white",
            'activebackground': "#444444",
            'activeforeground': "white",
            'borderwidth': 2,
            'relief': "raised"
        }

    def run(self):
        """Avvia il mainloop di Tkinter."""
        self.root.mainloop()

    def _checkbutton_style(self):
        """Stile per le checkbox, basato sul bottone ma con alcune modifiche."""
        style = self._button_style().copy()
        for key in ['width', 'padx', 'fg', 'activeforeground']:
            style.pop(key, None)
        style['selectcolor'] = '#444444'  # Colore sfondo selezione
        return style

    def _styled_button(self, parent, text, command):
        """Crea un bottone stilizzato."""
        opts = self._button_style()
        return tk.Button(parent, text=text, command=command, **opts)

    def _styled_checkbutton(self, parent, text, variable):
        """Crea una checkbox stilizzata."""
        opts = self._checkbutton_style()
        return tk.Checkbutton(parent, text=text, variable=variable, **opts)

    def _create_widgets(self):
        """Costruisce i widget della GUI."""
        PyArduinoGUIController(None)  # Inizializza controller (anche se senza parametri)

        # Titolo principale
        title_opts = {
            'font': ("Helvetica", 20, "bold"),
            'fg': "#FFA500",
            'bg': "#2e2e2e"
        }
        tk.Label(self.root, text="Interfaccia Py Arduino", **title_opts).pack(pady=(20, 10))

        main_frame = tk.Frame(self.root, bg="#2e2e2e")
        main_frame.pack(expand=True, padx=20, pady=20)

        # Tre colonne principali della GUI
        self.left_column(main_frame)
        self.center_column(main_frame)
        self.right_column(main_frame)

    def left_column(self, main_frame):
        """Colonna sinistra: selezione porta seriale e simulazione modelli."""
        left_frame = tk.Frame(main_frame, bg="#2e2e2e")
        left_frame.grid(row=0, column=0, padx=30, pady=10, sticky="n")

        subtitle_opts = {'font': ("Helvetica", 14, "bold"), 'fg': "#7FFFD4", 'bg': "#2e2e2e"}
        tk.Label(left_frame, text="Seleziona una porta seriale", **subtitle_opts).pack(pady=(0, 5))

        self.gestione_porte(left_frame)
        self.seleziona_simula_modelli(left_frame)

    def center_column(self, main_frame):
        """Colonna centrale: pulsanti di controllo e caricamento modello sim-to-real."""
        center_frame = tk.Frame(main_frame, bg="#2e2e2e")
        center_frame.grid(row=0, column=1, padx=30, pady=10, sticky="n")
        self._crea_pulsanti_controllo(center_frame)
        self._crea_carica_modello_sim_to_real(center_frame)
        self._crea_tuning_real(center_frame)

    def _crea_pulsanti_controllo(self, parent):
        """Crea i pulsanti di controllo nella colonna centrale."""
        self.button_texts = ["Enable", "Home", "Move Center", "Mode", "Enable Control"]
        self.buttons = {}
        for testo in self.button_texts:
            btn = self._styled_button(
                parent,
                testo,
                lambda t=testo: self.controller.on_toggle(t)
            )
            btn.pack(pady=10, fill="x", expand=True)
            self.buttons[testo] = btn
        from Context.AppContext import Mantieni_context
        Mantieni_context.change_instance("holder_buttons",self.controller.on_toggle)

    def right_column(self, main_frame):
        """Colonna destra: invio testo e addestramento agente."""
        right_frame = tk.Frame(main_frame, bg="#2e2e2e")
        right_frame.grid(row=0, column=2, padx=30, pady=10, sticky="n")
        self._crea_invio_testo(right_frame)

        subtitle_opts = {'font': ("Helvetica", 14, "bold"), 'fg': "#7FFFD4", 'bg': "#2e2e2e"}
        tk.Label(right_frame, text="Addestramento Agente", **subtitle_opts).pack(pady=(10, 5))

        training_frame = tk.Frame(right_frame, bg="#2e2e2e")
        training_frame.pack(pady=10, expand=True, anchor="center")

        self._create_training_controls(training_frame)

    def _crea_invio_testo(self, parent):
        """Crea area testo e bottone di invio."""
        self.send_button = self._styled_button(parent, "Send", self.controller.invia_testo)
        self.send_button.pack(pady=10, expand=True, anchor="center")

        self.text_area = ScrolledText(parent, height=2, width=15, bg="#1e1e1e", fg="white",
                                     font=("Helvetica", 15), relief="flat")
        self.text_area.pack(pady=10, expand=True, anchor="center")

    def gestione_porte(self, left_frame):
        """Gestione pulsanti e dropdown per le porte seriali."""
        self._styled_button(left_frame, "Aggiorna Porte", self.controller.aggiorna_porte).pack(pady=5, fill="x", expand=True)

        self._styled_button(left_frame, "Seleziona Porta", self.controller.on_select_port).pack(pady=10, fill="x", expand=True)


        porte_seriali = ["COM1", "COM2", "COM3", "COM4"]  # Esempio porte seriali
        self.porta_var = tk.StringVar(value=porte_seriali[0])
        self.dropdown = ttk.Combobox(
            left_frame,
            textvariable=self.porta_var,
            values=porte_seriali,
            state="readonly",
            font=("Helvetica", 10)
        )
        self.dropdown.pack(pady=10, fill="x", expand=True)

    def _create_training_controls(self, parent):
        """Crea i controlli per l'addestramento dell'agente."""
        self.verbose_var = tk.BooleanVar()
        self.verbose_check = self._styled_checkbutton(parent, "Verbose", self.verbose_var)
        self.verbose_check.pack(pady=4, anchor="center")

        ttk.Label(parent, text="Intervallo tra log:", font=(None, 9),
                  background="#2e2e2e", foreground="white").pack(pady=4, anchor="center")
        self.log_interval_var = tk.IntVar(value=100)
        self.log_interval_entry = tk.Entry(parent, textvariable=self.log_interval_var, width=6, justify="center")
        self.log_interval_entry.pack(pady=4, anchor="center")

        ttk.Label(parent, text="Step di train:", font=(None, 9),
                  background="#2e2e2e", foreground="white").pack(pady=4, anchor="center")
        self.train_steps_var = tk.IntVar(value=5000)
        self.train_steps_entry = tk.Entry(parent, textvariable=self.train_steps_var, width=6, justify="center")
        self.train_steps_entry.pack(pady=4, anchor="center")

        self.train_button = self._styled_button(parent, "Avvia",
            lambda: ModelManagerGUI.on_train_model(
                self,
                train_steps=_try_to_extract(self.train_steps_var),#self.train_steps_var.get(),
                verbose=1 if self.verbose_var.get() else 0,
                log_interval=_try_to_extract(self.log_interval_var)#self.log_interval_var.get()
            ))
        self.train_button.pack(pady=6, anchor="center")

    def _create_simulation_controls(self, parent):
        """Crea i controlli per simulare un agente."""
        row, col = 1, 0
        self.model_name_var = tk.StringVar(value="Nessun modello ancora caricato")
        tk.Label(parent, textvariable=self.model_name_var, bg="#2e2e2e", fg="white",
                 font=("Helvetica", 9)).grid(row=row, column=col, pady=4)
        row += 1

        self.load_model_button = self._styled_button(parent, "Carica",
                                                    lambda: ModelManagerGUI.on_carica_modello(self))
        self.load_model_button.grid(row=row, column=col, pady=4)
        row += 1

        self.sim_steps_var = tk.IntVar(value=1000)
        self.simula_model_button = self._styled_button(parent, "Simula", self._on_simulate_clicked)
        self.simula_model_button.grid(row=row, column=col, pady=4)
        row += 1

        ttk.Label(parent, text="epis. di simulazione :", font=(None, 9),
                  background="#2e2e2e", foreground="white").grid(row=row, column=col, pady=4, sticky="w")
        self.sim_steps_entry = tk.Entry(parent, textvariable=self.sim_steps_var, width=6, justify="center")
        self.sim_steps_entry.grid(row=row, column=col, padx=(95, 0))

    def _on_simulate_clicked(self):
        """Handler per il click sul bottone 'Simula'."""
        try:
            steps = int(self.sim_steps_var.get())
        except (tk.TclError, ValueError):
            print("problema lettura numero di step")
            steps = 0
        ModelManagerGUI.simulate_model(self.current_model_path, self.runner, steps)

    def seleziona_simula_modelli(self, left_frame):
        """Crea la sezione per simulare un agente nella colonna sinistra."""
        model_frame = tk.Frame(left_frame, bg="#2e2e2e")
        model_frame.pack(pady=10, anchor="center")

        subtitle_opts = {'font': ("Helvetica", 14, "bold"), 'fg': "#7FFFD4", 'bg': "#2e2e2e"}
        tk.Label(model_frame, text="Simula un Agente", **subtitle_opts).grid(row=0, column=0, columnspan=2,
                                                                             pady=(0, 10))

        self._create_simulation_controls(model_frame)
        for i in range(2):
            model_frame.columnconfigure(i, weight=1)

    def _crea_carica_modello_sim_to_real(self, center_frame):
        """Crea il controllo per caricare il modello sim-to-real nella colonna centrale."""
        self.model_name_var_sim_to_real = tk.StringVar(value="Nessun modello ancora caricato")
        tk.Label(center_frame, textvariable=self.model_name_var_sim_to_real, bg="#2e2e2e",
                 fg="white", font=("Helvetica", 9)).pack()

        self._styled_button( center_frame, "Carica",lambda: ModelManagerGUI.on_carica_modello_sim_to_real(self)).pack()

    @classmethod
    def get_sim_to_real(cls):
        """Metodo ridondante che restituisce sim_to_real_met."""
        return cls.sim_to_real_met

    def _crea_tuning_real(self,center_frame):
        self._styled_button(
            center_frame, "fine tuning",
            lambda: ModelManagerGUI.on_open_new_gui()
        ).pack()
