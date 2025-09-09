import tkinter.filedialog as fd
from gymnasium.wrappers import FlattenObservation
from stable_baselines3 import SAC
from stable_baselines3.common.vec_env import DummyVecEnv

from Controllo_e_Simulazione.ModelManagerGUI import ModelManagerGUI as Mm
from Controllo_e_Simulazione.Pendolo_inverso_ENV import CartPoleEnv


class SACRunner:
    """
    Gestisce il ciclo completo di addestramento, salvataggio, caricamento e simulazione
    di un agente Soft Actor-Critic (SAC) su un ambiente continuo personalizzato (CartPoleEnv).

    Funzionalità:
      - Inizializzazione dell’ambiente compatto in DummyVecEnv + FlattenObservation.
      - Addestramento del modello SAC con parametri configurabili.
      - Salvataggio/ricaricamento del modello via file ZIP.
      - Esecuzione di simulazioni per un dato numero di episodi.
    """

    def __init__(self, render: bool = False):
        """
        Inizializza l'ambiente CartPoleEnv con o senza rendering e crea il wrapper vettoriale.

        Args:
            render (bool): Se True, abilita il rendering 'human' nell'ambiente.
        """
        render_mode = 'human' if render else None
        self.env = DummyVecEnv([
            lambda: FlattenObservation(CartPoleEnv(render_mode=render_mode))
        ])
        self.model = None

    def train(
        self,
        learning_step: int,
        verbose: int,
        log_interval: int,
        learning_rate: float = 1e-4,
        ent_coef: float = 0.1,
        buffer_size: int = 1_000_000,
        batch_size: int = 512,
        tau: float = 0.001,
        gamma: float = 0.99
    ) -> str | None:
        """
        Addestra un agente SAC e salva il modello su file ZIP.

        Args:
            learning_step (int): Numero totale di passi di addestramento.
            verbose (int): Livello di verbosità (0=silenzioso, 1=base, 2=dettagliato).
            log_interval (int): Frequenza dei log di addestramento.
            learning_rate (float): Tasso di apprendimento.
            ent_coef (float): Coefficiente entropico per esplorazione.
            buffer_size (int): Dimensione del replay buffer.
            batch_size (int): Dimensione dei batch di campioni.
            tau (float): Rate di aggiornamento target network.
            gamma (float): Fattore di sconto del reward futuro.

        Returns:
            str | None: Percorso del file ZIP salvato, oppure None in caso di annullamento o errore.
        """
        try:
            self.model = SAC(
                policy="MlpPolicy",
                env=self.env,
                learning_rate=learning_rate,
                ent_coef=ent_coef,
                buffer_size=buffer_size,
                batch_size=batch_size,
                tau=tau,
                gamma=gamma,
                verbose=verbose,
            )

            self.model.learn(
                total_timesteps=learning_step,
                log_interval=log_interval
            )

            save_path = Mm.save_file()
            if save_path:
                self.model.save(save_path)
                return save_path
            else:
                print("[DEBUG] Percorso di salvataggio non valido, modello non salvato")
                return None

        except Exception as e:
            print(f"[ERROR] Eccezione durante train(): {e}")
            return None

    def load(self, path: str = None):
        """
        Carica un modello SAC da file ZIP e configura il logger.

        Args:
            path (str, optional): Percorso del file ZIP. Se None, apre un file dialog.

        Returns:
            SAC | None: Istanza del modello caricato, oppure None se annullato.
        """
        if path is None:
            path = fd.askopenfilename(
                title="Seleziona il file del modello SAC",
                filetypes=[("File ZIP", "*.zip"), ("Tutti i file", "*.*")]
            )
            if not path:
                return None

        self.model = SAC.load(path, env=self.env)

        import os
        from stable_baselines3.common.logger import configure

        # Crea la cartella dei log se non esiste
        os.makedirs("logs", exist_ok=True)

        # Configura un nuovo logger compatibile con SB3 2.7.0
        new_logger = configure(folder="logs")
        self.model.set_logger(new_logger)

        return self.model

    def run(self, num_episodes: int) -> None:
        """
        Esegue simulazioni con l'agente SAC per un numero specificato di episodi.

        Args:
            num_episodes (int): Numero di episodi da eseguire.

        Returns:
            None
        """
        if self.model is None or self.env is None:
            print("Errore: modello o ambiente non inizializzato.")
            return

        obs = self.env.reset()
        for episode in range(num_episodes):
            done = False
            while not done:
                action, _ = self.model.predict(obs, deterministic=True)
                obs, reward, done, _ = self.env.step(action)

        self.env.close()
        print("\n|| SIMULAZIONE CONCLUSA ||\n")
