import serial.tools.list_ports
from tkinter import messagebox
from Controllo_Seriale.SerialController import SerialController

ENABLE = 1.0
HOME = 2.0
MOVE_CENTER = 3.0
MODE = 4.0
ENABLE_CONTROL = 5.0


class PyArduinoGUIController:
    """
    Controller per l'interfaccia GUI PyArduino.
    Gestisce la selezione della porta seriale, l'invio dei comandi
    e l'interazione con il controller seriale sottostante.
    Implementa un pattern singleton per garantire una sola istanza.
    """
    _instance = None  # Singleton instance

    def __new__(cls, view=None):
        """
        Crea una nuova istanza singleton se non esistente, altrimenti ritorna l'istanza esistente.

        Args:
            view: Riferimento alla vista GUI associata (opzionale).

        Returns:
            Istanza singleton di PyArduinoGUIController.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, view=None):
        """
        Inizializza il controller, assegnando la vista e le variabili interne.
        Evita reinizializzazioni multiple.

        Args:
            view: Riferimento alla vista GUI associata (opzionale).
        """
        if getattr(self, "_initialized", False):
            return
        self._initialized = True

        self.view = view
        self.serial_controller = None
        self.serial_scheduler = None
        self.current_model_path = None
        self.port_name = None

    def aggiorna_porte(self):
        """
        Aggiorna la lista delle porte seriali disponibili e aggiorna il dropdown nella GUI.
        Se non ci sono porte disponibili, mostra un messaggio appropriato.
        """
        ports = serial.tools.list_ports.comports()
        port_list = [(port.device, port.description) for port in ports]

        if not port_list:
            port_list = [("Nessuna porta disponibile", "")]

        max_width = max(sum(len(str(item)) for item in port) for port in port_list)
        values = [f"{device}: {description}" for device, description in port_list]

        self.view.dropdown['values'] = values
        self.view.dropdown.current(0)
        self.view.dropdown.configure(width=max_width)

        print("Porte seriali aggiornate")

    def on_select_port(self):
        """
        Gestisce la selezione della porta seriale dall'interfaccia.
        Tenta di aprire la porta selezionata e inizializza il controller seriale.
        Mostra messaggi di errore in caso di problemi.
        """
        selected = self.view.dropdown.get()
        if selected.startswith("Nessuna porta disponibile"):
            messagebox.showwarning("Attenzione", "Nessuna porta seriale disponibile.")
            return

        self.port_name = selected.split(":")[0]

        try:
            ser = serial.Serial(self.port_name, 912600, timeout=1)

            from Controllo_Seriale.SerialSenderManager import SerialSenderManager
            self.serial_scheduler = SerialSenderManager(messaggio=0, Torque=0.0, seriale=ser, mode_value=0,
                                                        enable_control_value=0, X=0.0, Xdot=0.0, theta=0.0,
                                                        thetadot=0.0)

            controller = SerialController(ser, serial_scheduler=self.serial_scheduler)
            from Context.AppContext import Mantieni_context
            Mantieni_context.change_instance("controller", controller)
            if not controller.aperto:
                print(f"Impossibile aprire la porta {self.port_name}. Aggiorna le porte e riprova.")
                return

            self.serial_controller = controller
            print(f"Porta selezionata: {self.port_name} \nController istanziato.")
            Mantieni_context.change_instance("ser",ser)

        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'apertura della porta {self.port_name}:\n{e}")

    def on_toggle(self, button_text: str):
        """
        Gestisce il toggle dei pulsanti di comando nella GUI,
        eseguendo il metodo corrispondente del controller seriale e
        aggiornando il colore del pulsante per indicare lo stato.

        Args:
            button_text: Testo del pulsante premuto.
        """
        if self.serial_controller is None:
            print("Errore: la porta seriale non è selezionata. Seleziona una porta seriale.")
            return

        comando_map = {
            "Enable": ENABLE,
            "Home": HOME,
            "Move Center": MOVE_CENTER,
            "Mode": MODE,
            "Enable Control": ENABLE_CONTROL,
        }

        toggle_methods = {
            "Enable": self.serial_controller.toggle_enable,
            "Home": self.serial_controller.toggle_home,
            "Move Center": self.serial_controller.toggle_move_center,
            "Mode": self.serial_controller.toggle_mode,
            "Enable Control": self.serial_controller.toggle_enable_control,
        }
        comando = comando_map.get(button_text)
        if comando is None:
            print(f"Comando non riconosciuto: {button_text}")
            return

        toggle_fn = toggle_methods.get(button_text)
        if toggle_fn:
            toggle_fn()
        else:
            print(f"Nessuna funzione toggle definita per '{button_text}'")

        # Cambio colore del bottone (toggle visuale)
        btn = self.view.buttons.get(button_text)
        if btn:
            current_bg = btn.cget("bg")
            new_bg = "#2e2e2e" if current_bg == "#32CD32" else "#32CD32"
            btn.config(bg=new_bg)
            stato = "disattivato" if new_bg == "#2e2e2e" else "attivato"
            print(f"Comando '{button_text}' {stato}.")

    def invia_testo(self):
        """
        Legge il testo inserito nell'area di testo della GUI, lo converte in float
        e lo invia come valore di coppia (Torque) tramite il serial scheduler.
        Gestisce errori di conversione o invio e stampa messaggi di errore.
        """
        errore_generico = "❌ Errore durante l'invio del valore. Controlla che tutti i requisiti siano soddisfatti."

        try:
            if (not self.view or
                    not self.view.text_area or
                    not (contenuto := self.view.text_area.get("1.0", "end-1c").strip()) or
                    self.serial_controller is None or
                    not getattr(self.serial_controller, "aperto", False) or
                    self.serial_scheduler is None):
                print(errore_generico)
                return

            torque = float(contenuto)
            print(f"DEBUG invia_testo: valore convertito in float = {torque}")

            self.serial_scheduler.modifica_variabile("Torque", torque)
            print(f"Coppia inviata: {torque}")

        except Exception as e:
            print(f"{errore_generico} Dettagli: {e}")
