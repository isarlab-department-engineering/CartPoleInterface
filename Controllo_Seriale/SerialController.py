import struct

# Variabili condivise per il controllo degli stati
enable_value = 0
home_value = 0
move_center_value = 0
mode_value = 0
enable_control_value = 0

# Codici di comando float predefiniti
ENABLE = 1.0
HOME = 2.0
MOVE_CENTER = 3.0
MODE = 4.0
ENABLE_CONTROL = 5.0

# Valore speciale per sincronizzazione
INF = float('inf')


class SerialController:
    """
    Gestisce la comunicazione seriale con un dispositivo esterno tramite comandi float.

    Fornisce metodi per:
      - Lettura e scrittura di float little-endian (4 byte).
      - Invio di comandi standard (enable, home, centraggio, modalità, controllo).
      - Coordinamento con un serial_scheduler per variabili condivise.

    Destinato ad applicazioni embedded/robotiche che inviano float e ricevono risposte.
    """

    def __init__(self, port, baud_rate: int = 912600, serial_scheduler=None):
        """
        Configura il canale seriale e pulisce i buffer.

        Args:
            port: Oggetto seriale aperto (es. serial.Serial).
            baud_rate (int): Baud rate della connessione.
            serial_scheduler: Optional, gestore di variabili condivise.
        """
        self.ser = port
        self.ser.flush()
        self.ser.flushInput()
        self.ser.flushOutput()
        self.serial_scheduler = serial_scheduler
        self.baund_rate = baud_rate
        self.aperto = True

    @staticmethod
    def read_line(ser) -> float:
        """
        Legge un valore float (4 byte) da seriale.

        Args:
            ser: Porta seriale.

        Returns:
            float: Valore decodificato, 0.0 in caso di errore.
        """
        try:
            raw = ser.read(4)
            message = struct.unpack('<f', raw)[0]
        except Exception as e:
            print("ERRORE NELLA LETTURA DA read_line():", e)
            message = 0.0
        return message

    @staticmethod
    def throw_on_serial(ser, message: float):
        """
        Invia un float al dispositivo seriale.

        Args:
            ser: Porta seriale.
            message (float): Valore da inviare in formato float32.
        """
        try:
            packed = struct.pack('<f', message)
            ser.write(packed)
        except struct.error as e:
            print(f"ERRORE PACKING: valore {message} non convertibile in float32: {e}")
        except Exception as e:
            print(f"ERRORE DURANTE L'INVIO SU SERIALE: {e}")

    def toggle_enable(self):
        """
        Alterna lo stato di abilitazione nel sistema remoto.

        Aggiorna 'enable_value' su serial_scheduler e nel Context globale,
        quindi imposta il messaggio ENABLE.
        """
        corrente = self.serial_scheduler.shared_vars.get("enable_value", 0)
        nuovo = 1 - corrente
        self.serial_scheduler.modifica_variabile("enable_value", nuovo)
        self.serial_scheduler.modifica_variabile("messaggio", ENABLE)
        from Context.AppContext import Mantieni_context
        Mantieni_context.change_instance("enable", nuovo)

    def toggle_home(self):
        """
        Alterna il comando 'home' per portare il sistema in posizione iniziale.

        Aggiorna 'home_value', imposta messaggio HOME e aggiorna Context.
        """
        corrente = self.serial_scheduler.shared_vars.get("home_value", 0)
        nuovo = 1 - corrente
        self.serial_scheduler.modifica_variabile("home_value", nuovo)
        self.serial_scheduler.modifica_variabile("messaggio", HOME)
        from Context.AppContext import Mantieni_context
        Mantieni_context.change_instance("home_value", nuovo)

    def toggle_move_center(self):
        """
        Alterna il comando per centrare il sistema (MOVE_CENTER).

        Aggiorna 'move_center_value', imposta messaggio e Context.
        """
        corrente = self.serial_scheduler.shared_vars.get("move_center_value", 0)
        nuovo = 1 - corrente
        from Context.AppContext import Mantieni_context
        Mantieni_context.change_instance("move_center_value", nuovo)
        self.serial_scheduler.modifica_variabile("move_center_value", nuovo)
        self.serial_scheduler.modifica_variabile("messaggio", MOVE_CENTER)

    def toggle_mode(self):
        """
        Alterna la modalità operativa (manuale vs automatico).

        Aggiorna 'mode_value', invia MODE e aggiorna Context.
        """
        corrente = self.serial_scheduler.shared_vars.get("mode_value", 0)
        nuovo = 1 - corrente
        from Context.AppContext import Mantieni_context
        Mantieni_context.change_instance("mode_value", nuovo)
        self.serial_scheduler.modifica_variabile("mode_value", nuovo)
        self.serial_scheduler.modifica_variabile("messaggio", MODE)

    def toggle_enable_control(self):
        """
        Abilita/disabilita il controllo automatico (ENABLE_CONTROL).

        Aggiorna 'enable_control_value', imposta messaggio e Context.
        """
        corrente = self.serial_scheduler.shared_vars.get("enable_control_value", 0)
        nuovo = 1 - corrente
        from Context.AppContext import Mantieni_context
        Mantieni_context.change_instance("enable_control_value", nuovo)
        self.serial_scheduler.modifica_variabile("enable_control_value", nuovo)
        self.serial_scheduler.modifica_variabile("messaggio", ENABLE_CONTROL)

    def close(self):
        """
        Chiude la connessione seriale se aperta.

        Effetti:
            - Chiude self.ser.
            - Stampa conferma o warning se già chiusa.
        """
        if self.ser.is_open:
            self.ser.close()
            print("Connessione seriale chiusa.")
        else:
            print("Si è tentato di chiudere la connessione, ma era già chiusa.")
