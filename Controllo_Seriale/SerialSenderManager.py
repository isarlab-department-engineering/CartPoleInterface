import threading
import traceback

DEBUG_MODE = False  # Set False per disattivare i print di debug

from Controllo_Seriale.File_di_appoggio_funzioni import (
    salva_il_modello_se_necessario,
    send_serial_commands,
    should_enable_control,
    should_start_training,
    action_to_real,
    predict_deterministic,
    process_training_step,
    finish_episode_if_needed,
    flush_serial,
    read_sensor_data
)

from Controllo_e_Simulazione.PendulumGym import SACRunner




Holder_meta_var = {
    "in_traning": False,
    "stato_prec": None,
    "old_obs": None,
    "n_step": 0,
    "reward_dell_episodio": 0,
}


class SerialSenderManager:
    instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            with cls._lock:
                if cls.instance is None:
                    cls.instance = super().__new__(cls)
                    cls.instance.shared_vars = {
                        'mode_value': 0,
                        'enable_control_value': 0,
                        'Torque': 0.0,
                        'messaggio': 0,
                        'seriale': None,
                        'X': 0.0,
                        'Xdot': 0.0,
                        'theta': 0.0,
                        'thetadot': 0.0
                    }
                    cls.instance.shared_vars_lock = threading.RLock()
        return cls.instance

    def __init__(self, **kwargs):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

        with self.shared_vars_lock:
            self.shared_vars.update(kwargs)

        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def _run(self):
        if DEBUG_MODE:
            print("[DEBUG] Thread di comunicazione attivato.")
        agente = SACRunner()

        from GUI.ArduinoGui import PyArduinoGUIView
        env = model = None

        path = PyArduinoGUIView.get_sim_to_real_met()
        if path is not None:
            if DEBUG_MODE:
                print(f"[DEBUG] Caricamento modello da path: {path}")
            agente.load(path)

            env = agente.env
            model = agente.model
            if DEBUG_MODE:
                print("[DEBUG] Modello caricato con successo.")
        else:
            print("[WARNING] Modello non caricato: selezionare porta seriale prima.")

        self._implementazione_della_comunicazione(env=env, model=model)

    def _implementazione_della_comunicazione(self, env=None, model=None):
        ser = self._get_serial_port()
        if ser is None:
            print("[ERROR] Porta seriale non impostata.")
            return

        if DEBUG_MODE:
            print("[DEBUG] Inizio ciclo di comunicazione seriale.")
        while self._running:
            try:
                if ser.in_waiting > 0:
                    flush_serial(ser)
                    data = read_sensor_data(ser)

                    if data is None:
                        if DEBUG_MODE:
                            print("[DEBUG] Dati sensori non validi o incompleti.")
                        continue

                    x, x_dot, theta, theta_dot = data
                    if DEBUG_MODE:
                        print(f"[DEBUG] Sensor data: x={x:.3f}, x_dot={x_dot:.3f}, theta={theta:.3f}, theta_dot={theta_dot:.3f}")

                    mode_val, enable_ctrl, sent_message, torque_shared = self._read_shared_parameters()

                    control_loop(
                        model, env, ser, sent_message,
                        x, x_dot, theta, theta_dot,
                        mode_val, enable_ctrl, torque_shared
                    )

                    if sent_message != 0:
                        if DEBUG_MODE:
                            print("[DEBUG] Reset messaggio dopo invio comando.")
                        self.modifica_variabile('messaggio', 0)

            except Exception as e:
                print(f"[ERROR] Eccezione nel thread seriale: {e}")
                traceback.print_exc()

    def modifica_variabile(self, key, value):
        with self.shared_vars_lock:
            self.shared_vars[key] = value

    def _get_serial_port(self):
        with self.shared_vars_lock:
            return self.shared_vars.get("seriale", None)

    def _read_shared_parameters(self):
        with self.shared_vars_lock:
            return (
                self.shared_vars['mode_value'],
                self.shared_vars['enable_control_value'],
                self.shared_vars['messaggio'],
                self.shared_vars['Torque'],
            )


def determine_torque(model, env, obs, torque_shared, enable_ctrl):
    from Context.AppContext import Mantieni_context
    if DEBUG_MODE:
        print(f"[DEBUG] determine_torque: obs={obs}, enable_ctrl={enable_ctrl}")

    if model is not None and env is not None:
        if Mantieni_context.get("FLAG_PER_ALLENAMENTO"):
            if DEBUG_MODE:
                print("[DEBUG] Modalità ALLENAMENTO attiva")
            if should_enable_control(obs, enable_ctrl, Holder_meta_var["in_traning"]):
                if DEBUG_MODE:
                    print("[DEBUG] Inizio controllo automatico")
                Mantieni_context.get("holder_buttons")("Enable Control")
            elif should_start_training(obs, enable_ctrl):
                if DEBUG_MODE:
                    print("TRANING")
                Holder_meta_var["in_traning"] = True
                action = process_training_step(model, obs, Holder_meta_var)
                if DEBUG_MODE:
                    print(f"[DEBUG] Azione appresa: {action}")
                return action_to_real(action)
            else:
                if DEBUG_MODE:
                    print("[DEBUG] CADUTO")
                finish_episode_if_needed(obs, Holder_meta_var)
                if enable_ctrl:
                    Mantieni_context.get("holder_buttons")("Enable Control")

            print()
        else:
            if DEBUG_MODE:
                print("[DEBUG] Predizione deterministica")
            return predict_deterministic(model, obs)

    if DEBUG_MODE:
        print("[DEBUG] Uso torque condiviso")
    return torque_shared


def control_loop(model, env, ser, sent_message, x, x_dot, theta, theta_dot,
                 mode_val, enable_ctrl, torque_shared):
    obs = [x, x_dot, theta, theta_dot]
    if DEBUG_MODE:
        print(f"[DEBUG] Stato attuale: {obs}")

    torque = determine_torque(model, env, obs, torque_shared, enable_ctrl)
    if DEBUG_MODE:
        print(f"[DEBUG] Torque calcolato: {torque}")

    if mode_val == 1 and enable_ctrl == 1:
        if DEBUG_MODE:
            print(f"[DEBUG] Invio comando: torque={torque}, messaggio={sent_message}")
        send_serial_commands(ser, sent_message, torque)
    else:
        if DEBUG_MODE:
            print("[DEBUG] Controllo disattivato o modalità non attiva. Invio torque = 0.0")
        salva_il_modello_se_necessario(model)
        send_serial_commands(ser, sent_message, 0.0)
