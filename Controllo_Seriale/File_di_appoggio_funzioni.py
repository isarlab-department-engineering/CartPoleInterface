import math
import numpy as np

DEBUG_MODE = False  # False per disattivare i print di debug

thresholds = {
    # Limite massimo per la posizione assoluta durante il controllo (m)
    "x_threshold": 0.4,

    # Limite massimo per l'angolo durante il controllo (rad, equiv. 45°)
    "theta_threshold": math.radians(45),

    # Soglie per terminazione episodio
    "x_termination_threshold": 0.4,
    "theta_termination_threshold": math.radians(45),

    # Soglie per validità posizione iniziale
    "x_start_threshold": 0.1,
    "theta_start_threshold": 0.05
}

def salva_il_modello_se_necessario(model):
    """
    Salva il modello corrente su file se richiesto dal Context.

    Verifica il flag "SAVE_MODELLO_REAL" in AppContext e, se True,
    apre il file dialog per scegliere il percorso di salvataggio.

    Args:
        model: Oggetto modello con metodo .save(path).

    Returns:
        str | None: Percorso del file salvato, se successo.
    """
    from Context.AppContext import Mantieni_context
    if Mantieni_context.get("SAVE_MODELLO_REAL"):
        if DEBUG_MODE:
            print("[DEBUG] Salvataggio modello richiesto.")
        Mantieni_context.change_instance("SAVE_MODELLO_REAL", False)
        from Controllo_e_Simulazione.ModelManagerGUI import ModelManagerGUI as Mm
        save_path = Mm.save_file()
        if save_path:
            model.save(save_path)
            if DEBUG_MODE:
                print(f"[DEBUG] Modello salvato in: {save_path}")
            return save_path
        else:
            if DEBUG_MODE:
                print("[DEBUG] Salvataggio modello annullato: percorso non valido.")


def pos_consentita(x, t):
    """
    Verifica se la posizione e l'angolo rientrano nei limiti consentiti.

    Args:
        x (float): Posizione carrello (m).
        t (float): Angolo palo (rad).

    Returns:
        bool: True se x e t sono entro thresholds['x_threshold'] e thresholds['theta_threshold'].
    """
    res = abs(x) < thresholds["x_threshold"] and abs(t) < thresholds["theta_threshold"]
    if DEBUG_MODE:
        print(f"[DEBUG] pos_consentita(x={x:.3f}, t={math.degrees(t):.2f}°) = {res}")
    return res


def predict_deterministic(model, obs):
    """
    Esegue una predizione deterministica con il modello e converte l'azione.

    Args:
        model: Modello RL con metodo .predict(obs, deterministic=True).
        obs: Osservazione corrente.

    Returns:
        action: Azione convertita da action_to_real.
    """
    action, _ = model.predict(obs, deterministic=True)
    if DEBUG_MODE:
        print(f"[DEBUG] predict_deterministic: action={action}")
    return action_to_real(action)


def should_start_training(obs, enable_ctrl):
    """
    Controlla se iniziare l'allenamento basato sulla posizione iniziale.

    Args:
        obs (tuple): Stato corrente (x, x_dot, theta, theta_dot).
        enable_ctrl (bool): Flag di controllo abilitato.

    Returns:
        bool: True se pos_consentita e enable_ctrl sono True.
    """
    x, x_d, t, t_d = obs
    res = pos_consentita(x, t) and enable_ctrl
    if DEBUG_MODE:
        print(f"[DEBUG] should_start_training: obs={obs}, enable_ctrl={enable_ctrl} => {res}")
    return res


def action_to_real(action):
    """
    (Stub) Converte l'azione calcolata in una rappresentazione reale.

    Args:
        action: Azione dall'agente (float o np.ndarray).

    Returns:
        action: Valore in input
    """

    #ADESSO QUESTA FUNZIONE NON SERVE MA è UTILIE PER UN POSSIBILE MIGLIORAMENTO NEL TESTING

    if DEBUG_MODE:
        print(f"[DEBUG] action_to_real: input={action}")
    return action


def send_serial_commands(ser, sent_message, torque):
    """
    Invia comandi seriali all'hardware tramite SerialController.

    Args:
        ser: Porta seriale.
        sent_message: Messaggio di controllo.
        torque: Valore di torque da inviare.
    """
    from Controllo_Seriale.SerialController import SerialController as Sc
    if DEBUG_MODE:
        print(f"[DEBUG] Invio seriale: messaggio={sent_message}, torque={torque}")
    Sc.throw_on_serial(ser, sent_message)
    Sc.throw_on_serial(ser, torque)


def calc_reward(old_obs, done):
    """
    Calcola il reward in base allo stato precedente e al flag done.

    Args:
        old_obs (tuple | None): Stato precedente.
        done (bool): Flag di terminazione episodio.

    Returns:
        float: Reward normalizzato con penalità o bonus.
    """
    if done:
        return -1
    if old_obs is None:
        return 0

    x, x_dot, theta, theta_dot = old_obs
    x_limit = 0.8

    errore_theta = np.clip(abs(theta) / math.radians(90), 0, 1)
    rew_theta = 1 - errore_theta ** 2

    errore_x = np.clip(abs(x) / x_limit, 0, 1)
    rew_x = 1 - errore_x ** 2

    w_theta = 0.7
    w_x = 0.3

    reward = w_theta * rew_theta + w_x * rew_x

    epsilon = 1e-6
    if abs(theta) < epsilon:
        reward += 10
    if done:
        reward -= 10

    if DEBUG_MODE:
        print(f"[DEBUG] calc_reward: reward={reward}, done={done}, theta={theta:.3f}")

    return reward


def calcola_reward_done(old_obs, obs):
    """
    Valuta terminazione episodio e calcola reward.

    Args:
        old_obs (tuple | None): Stato precedente.
        obs (tuple): Stato corrente.

    Returns:
        tuple: (terminated: bool, reward: float)
    """
    x, x_d, t, t_d = obs
    terminated = bool(
        abs(x) > thresholds["x_termination_threshold"] or
        abs(t) > thresholds["theta_termination_threshold"]
    )
    rew = calc_reward(old_obs, terminated)
    if DEBUG_MODE:
        print(f"[DEBUG] calcola_reward_done: terminated={terminated}, reward={rew}")
    return terminated, rew


def start_pos_consentita(x, t):
    """
    Verifica se la posizione iniziale è entro soglie di start.

    Args:
        x (float): Posizione iniziale.
        t (float): Angolo iniziale.

    Returns:
        bool: True se entro thresholds di start.
    """
    res = (
        abs(x) < thresholds["x_start_threshold"] and
        abs(t) < thresholds["theta_start_threshold"]
    )
    if DEBUG_MODE:
        print(f"[DEBUG] start_pos_consentita(x={x:.3f}, t={t:.3f}) = {res}")
    return res


def should_enable_control(obs, enable_ctrl, in_traning):
    """
    Determina se abilitare il controllo basato sullo stato iniziale.

    Args:
        obs (tuple): Stato corrente.
        enable_ctrl (bool): Controllo già abilitato.
        in_traning (bool): Flag allenamento in corso.

    Returns:
        bool: True se start_pos_consentita e non in allenamento né controllo attivo.
    """
    x, x_d, t, t_d = obs
    res = start_pos_consentita(x, t) and not in_traning and not enable_ctrl
    if DEBUG_MODE:
        print(f"[DEBUG] should_enable_control: obs={obs}, enable_ctrl={enable_ctrl}, in_traning={in_traning} => {res}")
    return res


def process_training_step(model, obs, holder_meta_var):
    """
    Gestisce l'inserimento nel replay buffer e step di training periodici.

    Args:
        model: Oggetto modello SAC con replay_buffer e metodo .train().
        obs: Stato corrente.
        holder_meta_var (dict): Meta-variabili di stato (stato_prec, n_step, reward_dell_episodio).

    Returns:
        action: Azione scelta dall'agente.
    """
    if holder_meta_var["stato_prec"] is not None:
        old_obs, action_prev = holder_meta_var["stato_prec"]
        done, reward = calcola_reward_done(old_obs, obs)
        model.replay_buffer.add(old_obs, obs, action_prev, reward, done, infos=[{}])
        if DEBUG_MODE:
            print("[DEBUG] Aggiunto al buffer replay.")
        holder_meta_var["reward_dell_episodio"] += reward
        holder_meta_var["n_step"] += 1

        batch_size = 32
        if model.replay_buffer.size() >= batch_size * 10 and holder_meta_var["n_step"] % 10 == 0:
            if True:
                print("[DEBUG] Avvio fase di allenamento modello.")
            model.train(batch_size=batch_size, gradient_steps=1)

    action, _ = model.predict(obs, deterministic=False)
    holder_meta_var["stato_prec"] = (obs, action)
    if DEBUG_MODE:
        print(f"[DEBUG] process_training_step: azione calcolata {action}")
    return action


def finish_episode_if_needed(obs, holder_meta_var):
    """
    Gestisce la logica di fine episodio e stampa statistiche.

    Args:
        obs: Stato finale.
        holder_meta_var (dict): Meta-variabili di stato.
    """
    holder_meta_var["in_traning"] = False
    done, _ = calcola_reward_done(holder_meta_var["old_obs"], obs)
    if done and holder_meta_var["n_step"] != 0:
        print("EPISODIO TERMINATO")
        print("Reward totale episodio:", holder_meta_var["reward_dell_episodio"])
        holder_meta_var["n_step"] = 0
        holder_meta_var["reward_dell_episodio"] = 0
    else:
        if DEBUG_MODE:
            print("[DEBUG] Episodio non terminato o nessun passo fatto.")


def flush_serial(ser):
    """
    Svuota il buffer seriale leggendo fino a valore inf.

    Args:
        ser: Porta seriale.
    """
    from Controllo_Seriale.SerialController import SerialController as Sc
    check = Sc.read_line(ser)
    while check != float("inf"):
        check = Sc.read_line(ser)
    if DEBUG_MODE:
        print("[DEBUG] Buffer seriale svuotato fino a INF.")


def read_sensor_data(ser):
    """
    Legge dati dai sensori via seriale.

    Args:
        ser: Porta seriale.

    Returns:
        tuple | None: (x, x_dot, theta, theta_dot) o None in caso di errore.
    """
    from Controllo_Seriale.SerialController import SerialController as Sc
    try:
        x = Sc.read_line(ser)
        x_dot = Sc.read_line(ser)
        theta = Sc.read_line(ser)
        theta_dot = Sc.read_line(ser)
        if DEBUG_MODE:
            print(f"[DEBUG] read_sensor_data: x={x}, x_dot={x_dot}, theta={theta}, theta_dot={theta_dot}")
        return x, x_dot, theta, theta_dot
    except Exception as e:
        print(f"[ERROR] Errore in lettura sensori: {e}")
        return None
