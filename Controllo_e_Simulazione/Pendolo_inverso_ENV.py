import math
import numpy as np
import gymnasium as gym
from dataclasses import dataclass
from typing import Optional, Union
from gymnasium import spaces
from gymnasium.error import DependencyNotInstalled
import matplotlib.pyplot as plt
#---------------------------------------------------------------#
from Controllo_e_Simulazione.Circ_Buff import CircularBuffer
from Controllo_e_Simulazione.SACLogger import SACLogger


def _vince_attrito_statico(vel, f_applicata, coef_statico):
    """
    Determina se l'attrito statico vince sulla forza applicata.

    Args:
        vel (float): Velocità attuale del corpo (m/s o rad/s).
        f_applicata (float): Forza o momento applicato.
        coef_statico (float): Coefficiente di attrito statico.

    Returns:
        bool: True se l'attrito statico impedisce il movimento, False altrimenti.
    """
    return abs(vel) < 1e-6 and abs(f_applicata) <= coef_statico


def immetti_nei_plt(x, x_dot, theta, theta_dot, action):
    """
    Salva e visualizza l'evoluzione temporale dei parametri del sistema in grafici separati.

    Ogni chiamata aggiunge i valori attuali alla figura matplotlib.
    I plot includono posizione, velocità, angolo, velocità angolare e azione.

    Args:
        x (float): Posizione del carrello.
        x_dot (float): Velocità del carrello.
        theta (float): Angolo del palo rispetto alla verticale.
        theta_dot (float): Velocità angolare del palo.
        action (float): Azione applicata al sistema.
    """
    if not hasattr(immetti_nei_plt, "fig"):
        immetti_nei_plt.fig, axs = plt.subplots(5, 1, figsize=(10, 10), sharex=True)
        immetti_nei_plt.axs = axs
        labels = ['x', 'x_dot', 'theta', 'theta_dot', 'action']
        colors = ['blue', 'orange', 'green', 'red', 'purple']
        immetti_nei_plt.lines = []
        for ax, label, color in zip(axs, labels, colors):
            line, = ax.plot([], [], label=label, color=color)
            ax.set_ylabel(label)
            ax.legend()
            ax.grid(True)
            immetti_nei_plt.lines.append(line)
        axs[-1].set_xlabel('Time step')
        plt.tight_layout()
        immetti_nei_plt.data = [[] for _ in range(5)]

    immetti_nei_plt.data[0].append(x)
    immetti_nei_plt.data[1].append(x_dot)
    immetti_nei_plt.data[2].append(theta)
    immetti_nei_plt.data[3].append(theta_dot)
    immetti_nei_plt.data[4].append(action)

    for i in range(5):
        immetti_nei_plt.lines[i].set_data(range(len(immetti_nei_plt.data[i])), immetti_nei_plt.data[i])
        immetti_nei_plt.axs[i].relim()
        immetti_nei_plt.axs[i].autoscale_view()

    immetti_nei_plt.fig.canvas.draw()
    immetti_nei_plt.fig.canvas.flush_events()


class CartPoleEnv(gym.Env[np.ndarray, Union[int, np.ndarray]]):
    """
    Ambiente CartPole personalizzato per simulazione e controllo di un sistema carrello-pendolo.

    Supporta dinamicità fisica realistica, attriti non lineari e
    integrazione con hardware esterno (Arduino). Conforme allo standard gymnasium.Env.
    """
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 50,
    }

    def __init__(self, sutton_barto_reward: bool = False, render_mode: Optional[str] = None):
        """
        Inizializza l'ambiente CartPole.

        Args:
            sutton_barto_reward (bool): Usa reward stile Sutton-Barto se True.
            render_mode (str, optional): 'human' o 'rgb_array' per il rendering.
        """
        self.sutton_barto_reward = sutton_barto_reward
        self.render_mode = render_mode
        self.pos_perf = 0
        self.theta_perf = 0
        self.state = None

        self._init_logger()
        self._init_reward()
        self._init_thresholds()
        self._init_physical_params()
        self._init_fit_coefficients()
        self._init_attriti()
        self._init_communication()
        self._init_initial_state()
        self._init_spazi()
        self._init_rendering()

    def _init_logger(self):
        """Crea il logger per il monitoraggio dei reward."""
        self.logger = SACLogger()
        #self.logger.create_liveplot("reward_medio_per_episodio")

    def _init_reward(self):
        """Definisce la dataclass per i parametri di reward."""
        @dataclass
        class RewParam:
            num_step: int = 10000
            max_step_per_episodio: int = 750
            step_per_episodio: int = 0
            num_episod: int = 0
            step_totali: int = 0

        self.reward_param = RewParam()

    def _init_thresholds(self):
        """Definisce i limiti fisici per terminazione episodio."""
        @dataclass
        class Thresholds:
            theta: float = math.radians(90)
            x: float = 0.4

        self.Thresholds = Thresholds()

    def _init_physical_params(self):
        """Inizializza i parametri fisici primari e derivati."""
        @dataclass
        class PhysicalParams:
            _gravity: float = 9.81
            _masscart: float = 0.6
            _masspole: float = 0.1528
            _length: float = 0.1
            max_action: float = 900

            gravity: float = 0
            masscart: float = 0
            masspole: float = 0
            length: float = 0
            total_mass: float = 0
            polemass_length: float = 0

        self.phys = PhysicalParams()

    def _init_fit_coefficients(self):
        """Imposta i coefficienti di conversione azione→forza."""
        @dataclass
        class CoeffFit:
            _coef_ang_1: float = 0.0215
            _coef_ang_2: float = 0.0221
            _costante_1: float = -1.67
            _costante_2: float = -1.39

            coef_ang_1: float = 0
            coef_ang_2: float = 0
            costante_1: float = 0
            costante_2: float = 0

        self.coef_reali = CoeffFit()

    def _init_attriti(self):
        """Inizializza i coefficienti di attrito (statico, dinamico, viscoso)."""
        @dataclass
        class Attriti:
            coefatr_cart_stat: float = 0
            coefatr_cart_dinam: float = 0
            coefatr_cart_visc: float = 0
            coefatr_pole_stat: float = 0
            coefatr_pole_dinam: float = 0
            coefatr_pole_visc: float = 0

        self.attriti = Attriti()

    def _init_communication(self):
        """Configura i parametri di comunicazione simulata con l'hardware."""
        @dataclass
        class ComunicazioneArduino:
            tau: float = 0.005
            period: float = 0.05

            @property
            def non_allineamento_tra_freq(self) -> int:
                return int(self.period / self.tau)

        self.comunicationPar = ComunicazioneArduino()

    def _init_initial_state(self):
        """Prepara stato iniziale, buffer reward e parametri random iniziali."""
        class ParaminitStatus:
            gradi_init: int = 5
            gradi_al_secondo_init: float = 0.1

        self.parm_stat_iniziale = ParaminitStatus()
        self.buffer_reward = CircularBuffer(40)
        self.buffer_reward.insert(0)

    def _init_spazi(self):
        """Definisce action_space e observation_space compatibili con Gymnasium."""
        high = np.array([
            self.Thresholds.x,
            np.inf,
            self.Thresholds.theta,
            np.inf,
        ], dtype=np.float32)

        self.action_space = spaces.Box(
            low=-self.phys.max_action,
            high=self.phys.max_action,
            shape=(1,),
            dtype=np.float32
        )
        self.observation_space = spaces.Box(
            low=-high,
            high=high,
            shape=(4,),
            dtype=np.float32
        )

    def _init_rendering(self):
        """Prepara variabili per il rendering (pygame)."""
        self.screen_width = 600
        self.screen_height = 400
        self.screen = None
        self.clock = None
        self.state: Optional[np.ndarray] = None
        self.steps_beyond_terminated = None

    def step(self, action):
        """
        Esegue un passo dell'ambiente applicando l'azione data.

        Args:
            action (float or np.ndarray): Forza sul carrello.

        Returns:
            tuple: (observation, reward, terminated, truncated, info)
        """
        assert self.action_space.contains(action), f"{action} invalid"
        assert self.state is not None, "reset() non è stato chiamato"

        self.reward_param.step_per_episodio += 1
        self.reward_param.step_totali += 1

        x, x_dot, theta, theta_dot = self._genera_e_applica_la_forza(action)
        self.state = [x, x_dot, theta, theta_dot]

        #immetti_nei_plt(x, x_dot, theta, theta_dot, action)

        terminated, truncated = self._get_status_terminated(x, theta)

        if not (terminated or truncated):
            reward = self._calcola_reward()
            self.buffer_reward.add_to_current(reward)
        else:
            reward = 0

        if self.render_mode == "human":  # and self.reward_param.num_episod % 10 == 0:
            self.render()

        return np.array(self.state, dtype=np.float32), reward, terminated, truncated, {}

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        """
        Reinizializza l'ambiente per un nuovo episodio.

        Args:
            seed (int, optional): Seed per la generazione casuale.
            options (dict, optional): Non usate in questa implementazione.

        Returns:
            tuple: (initial_observation, info)
        """
        self.state = self.init_state_iniziale(seed)
        self.reward_param.num_episod += 1
        self.aggiorna_parametri_random()

        #self.logger.update_liveplot("reward_medio_per_episodio", self.buffer_reward.current_val())
        print(
            f"rew.ep {self.buffer_reward.current_val():.3f}\t"
            f" Avg: {self.buffer_reward.get_average():.3f}\t"
            f" N.ep: {self.reward_param.num_episod}\t"
            f"N.step: {self.reward_param.step_per_episodio}\t"
            f"Avg step/ep: {(self.reward_param.step_totali/self.reward_param.num_episod):.3f}"
        )

        self.buffer_reward.insert(0)
        self.reward_param.step_per_episodio = 0

        """if self.pos_perf != 0 or self.theta_perf != 0:
            print("n. ep:",self.reward_param.num_episod," | pos_perf.: ",self.pos_perf," | theta_perf.: ",self.theta_perf)
            self.pos_perf=0
            self.theta_perf=0"""

        if self.render_mode == "human":
            #episodi_mancanti = 10 - self.reward_param.num_episod % 10
            #print("Episodi mancanti al prossimo render:", episodi_mancanti)
            #if self.reward_param.num_episod % 10 == 0:
            self.render()

        return np.array(self.state, dtype=np.float32), {}

    def apply_force_and_update_state(self, force):
        """
        Applica una forza al carrello e aggiorna lo stato con RK4.

        Args:
            force (float): Forza da applicare (N).

        Returns:
            list: Nuovo stato [x, x_dot, theta, theta_dot].
        """
        def dynamics(state_attuale, applied_force):
            """
            Calcola derivata di stato includendo attriti e dinamica pendolo invertito.
            """
            x, x_dot, theta, theta_dot = state_attuale
            sin_theta = np.sin(theta)
            cos_theta = np.cos(theta)

            f_viscous_cart = -self.attriti.coefatr_cart_visc * x_dot
            f_net = applied_force + f_viscous_cart

            if _vince_attrito_statico(x_dot, f_net, self.attriti.coefatr_cart_stat):
                x_acc = 0.0
                temp = (self.phys.polemass_length * theta_dot**2 * sin_theta) / self.phys.total_mass
            else:
                f_dynamic_cart = -self.attriti.coefatr_cart_dinam * np.sign(x_dot if abs(x_dot) >= 1e-6 else f_net)
                f_net += f_dynamic_cart
                temp = (f_net + self.phys.polemass_length * theta_dot**2 * sin_theta) / self.phys.total_mass

            denominator = self.phys.length * (4.0/3.0 - self.phys.masspole*cos_theta**2/self.phys.total_mass)
            theta_acc = (self.phys.gravity*sin_theta - cos_theta*temp) / denominator

            if _vince_attrito_statico(x_dot, f_net, self.attriti.coefatr_cart_stat):
                x_acc = 0.0
            else:
                x_acc = temp - self.phys.polemass_length*theta_acc*cos_theta/self.phys.total_mass

            t_viscous_pole = -self.attriti.coefatr_pole_visc * theta_dot
            t_net = t_viscous_pole

            if not _vince_attrito_statico(theta_dot, t_net, self.attriti.coefatr_pole_stat):
                t_dynamic_pole = -self.attriti.coefatr_pole_dinam * np.sign(theta_dot if abs(theta_dot) >= 1e-6 else t_net)
                t_net += t_dynamic_pole
                theta_acc += t_net/(self.phys.masspole*self.phys.length**2)

            result = [
                x_dot,
                x_acc.item() if isinstance(x_acc, np.ndarray) else x_acc,
                theta_dot,
                theta_acc.item() if isinstance(theta_acc, np.ndarray) else theta_acc,
            ]
            return np.array(result, dtype=np.float32)

        state = np.array(self.state, dtype=np.float32)
        dt = self.comunicationPar.tau

        k1 = dynamics(state, force)
        k2 = dynamics(state + 0.5 * k1 * dt, force)
        k3 = dynamics(state + 0.5 * dt * k2, force)
        k4 = dynamics(state + dt * k3, force)

        state_next = state + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)
        self.state = state_next.tolist()
        return self.state

    def _compute_reward(self):
        """
        Calcola reward basato sugli errori normalizzati di posizione e angolo.

        Returns:
            float: Reward computato.
        """
        x, theta, x_dot, theta_dot = self.state
        theta_limit = self.Thresholds.theta
        x_limit = self.Thresholds.x

        errore_theta = abs(theta)/theta_limit
        rew_theta = 1 - errore_theta**2

        errore_x = abs(x)/x_limit
        rew_x = 1 - errore_x**2

        w_theta, w_x = 0.8, 0.2
        reward = w_theta*rew_theta + w_x*rew_x

        if abs(theta) < 1e-6:
            reward += 10

        #if abs(theta) > math.radians(60):
        #    reward -= 10

        return reward

    def render(self):
        """
        Renderizza l'ambiente con pygame in modalità 'human' o restituisce array RGB.
        """
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "Chiamata a render() senza render_mode; specificare render_mode all'inizializzazione."
            )
            return

        try:
            import pygame
            from pygame import gfxdraw
        except ImportError as e:
            raise DependencyNotInstalled(
                'pygame non installato; eseguire pip install "gymnasium[classic-control]"'
            ) from e

        if self.screen is None:
            pygame.init()
            if self.render_mode == "human":
                pygame.display.init()
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            else:
                self.screen = pygame.Surface((self.screen_width, self.screen_height))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        world_width = self.Thresholds.x*2
        scale = self.screen_width/world_width
        polewidth = 10.0
        polelen = scale*(2*self.phys.length)
        cartwidth, cartheight = 50.0, 30.0

        if self.state is None:
            return None

        x = self.state
        self.surf = pygame.Surface((self.screen_width, self.screen_height))
        self.surf.fill((255, 255, 255))

        l, r, t, b = -cartwidth/2, cartwidth/2, cartheight/2, -cartheight/2
        axleoffset = cartheight/4.0
        cartx = x[0]*scale + self.screen_width/2.0
        carty = 100
        coords = [(c[0]+cartx, c[1]+carty) for c in [(l,b), (l,t), (r,t), (r,b)]]
        gfxdraw.aapolygon(self.surf, coords, (0,0,0))
        gfxdraw.filled_polygon(self.surf, coords, (0,0,0))

        l, r, t, b = -polewidth/2, polewidth/2, polelen-polewidth/2, -polewidth/2
        pole_coords = [
            (pygame.math.Vector2(coord).rotate_rad(-x[2]) + pygame.math.Vector2(cartx, carty+axleoffset))
            for coord in [(l,b), (l,t), (r,t), (r,b)]
        ]
        gfxdraw.aapolygon(self.surf, pole_coords, (202,152,101))
        gfxdraw.filled_polygon(self.surf, pole_coords, (202,152,101))
        gfxdraw.aacircle(self.surf, int(cartx), int(carty+axleoffset), int(polewidth/2), (129,132,203))
        gfxdraw.filled_circle(self.surf, int(cartx), int(carty+axleoffset), int(polewidth/2), (129,132,203))

        #mapup = int((self.screen_width/2.0 + self.x_threshold*scale/2.0)+cartwidth/2.0)
        #mapdown = int((self.screen_width/2.0 - self.x_threshold*scale/2.0)+cartwidth/2.0)

        gfxdraw.hline(self.surf, 0, self.screen_width, carty, (0,0,0))

        #gfxdraw.vline(self.surf, mapup, carty, self.screen_height, (255,0,0))
        #gfxdraw.vline(self.surf, mapdown, carty, self.screen_height, (255,0,0))

        self.surf = pygame.transform.flip(self.surf, False, True)
        self.screen.blit(self.surf, (0,0))

        if self.render_mode == "human":
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"])
            pygame.display.flip()
        else:  # rgb_array
            return np.transpose(np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1,0,2))

    def _genera_e_applica_la_forza(self, action: float) -> np.ndarray:
        """
        Traduce un'azione in forza e la applica ripetutamente per simulare disallineamento frequenze.

        Args:
            action (float): Azione da convertire.

        Returns:
            np.ndarray: Stato aggiornato dopo applicazione forza.
        """
        force = self.action_to_force(action)
        state = None
        for _ in range(self.comunicationPar.non_allineamento_tra_freq - 1):
            state = self.apply_force_and_update_state(force)
        return np.array(state, dtype=np.float64)

    def _get_status_terminated(self, x, theta):
        """
        Controlla se l'episodio termina per soglia o per step massimi.

        Args:
            x (float): Posizione attuale.
            theta (float): Angolo attuale.

        Returns:
            tuple: (terminated: bool, truncated: bool)
        """
        terminated = bool(abs(x) > self.Thresholds.x or abs(theta) > self.Thresholds.theta)
        truncated = self.reward_param.max_step_per_episodio - self.reward_param.step_per_episodio < 0
        #if truncated or terminated:
        #    self._DEBUG_status(terminated,truncated,x)
        return terminated, truncated

    def _calcola_reward(self):
        """
        Se non Sutton-Barto, calcola reward personalizzato, altrimenti 0.

        Returns:
            float: Reward calcolato.
        """
        if self.sutton_barto_reward:
            return 0.0
        return self._compute_reward()

    def _stamp_info_status(self, terminated, truncated, x):
        """
        Stampa informazioni di debug sullo stato di terminazione.

        Args:
            terminated (bool): Episodio terminato per soglia.
            truncated (bool): Episodio troncato per step massimi.
            x (float): Posizione attuale.
        """
        print('---------- DEBUG STATUS ----------')
        print("| N. ep:", self.reward_param.num_episod, end=" | causa: ")
        if truncated:
            print("MAX STEP RAGGIUNTI", end=" |")
        if terminated:
            if abs(x) > self.Thresholds.x:
                print("X fuori soglia", end=" |")
            else:
                print("T inclinazione", end=" |")
            print("last step:", self.reward_param.step_per_episodio, end=" |")
        print()
        if self.reward_param.num_episod % 10 == 0:
            print("Step totali attuali:", self.reward_param.step_totali, end=" | ")
            print("Media ultimi 50 reward episodio:", self.buffer_reward.get_average(), end=" |")
            print()
        print("--------------------------------")

    def action_to_force(self, action):
        """
        Converte un'azione continua in forza con funzione piecewise lineare.

        Args:
            action (float or np.ndarray): Valore dell'azione.

        Returns:
            float: Forza risultante.
        """
        x = np.array(action)
        return np.where(
            x <= 340,
            self.coef_reali.coef_ang_1 * x + self.coef_reali.costante_1,
            self.coef_reali.coef_ang_2 * x + self.coef_reali.costante_2
        )

    def aggiorna_parametri_random(self):
        """
        Randomizza i parametri fisici e di attrito per ogni nuovo episodio.
        """
        rng = np.random.default_rng()

        self.phys.gravity = float(rng.normal(self.phys._gravity, self.phys._gravity * 0.01))
        self.phys.masscart = float(rng.normal(self.phys._masscart, self.phys._masscart * 0.05))
        self.phys.masspole = float(rng.normal(self.phys._masspole, self.phys._masspole * 0.05))
        self.phys.length = float(rng.normal(self.phys._length, self.phys._length * 0.05))

        self.phys.total_mass = self.phys.masscart + self.phys.masspole
        self.phys.polemass_length = self.phys.masspole * self.phys.length

        self.coef_reali.coef_ang_1 = float(rng.normal(self.coef_reali._coef_ang_1, self.coef_reali._coef_ang_1 * 0.08))
        self.coef_reali.coef_ang_2 = float(rng.normal(self.coef_reali._coef_ang_2, self.coef_reali._coef_ang_2 * 0.08))
        self.coef_reali.costante_1 = float(rng.normal(self.coef_reali._costante_1, abs(self.coef_reali._costante_1) * 0.08))
        self.coef_reali.costante_2 = float(rng.normal(self.coef_reali._costante_2, abs(self.coef_reali._costante_2) * 0.08))

        self.attriti.coefatr_cart_stat = float(rng.uniform(0.3, 1))
        self.attriti.coefatr_cart_dinam = float(rng.uniform(0.3, self.attriti.coefatr_cart_stat))
        self.attriti.coefatr_cart_visc = float(rng.uniform(0.3, 1))
        self.attriti.coefatr_pole_stat = float(rng.uniform(0.0, 0.01))
        self.attriti.coefatr_pole_dinam = float(rng.uniform(0.0, self.attriti.coefatr_pole_stat))
        self.attriti.coefatr_pole_visc = float(rng.uniform(0.0, 0.01))

        #print(f"| mc={self.phys.masscart:.3f} | mp={self.phys.masspole:.3f} | ... | pv={self.attriti.coefatr_pole_visc:.3f} |")

    def init_state_iniziale(self, seed):
        """
        Genera uno stato iniziale randomico per carrello e palo.

        Args:
            seed (int): Seed per RNG.

        Returns:
            np.ndarray: Stato iniziale [x, x_dot, theta, theta_dot].
        """
        if seed is not None:
            self.np_random, _ = gym.utils.seeding.np_random(seed)

        angle_range_rad = np.deg2rad(self.parm_stat_iniziale.gradi_init)
        ang_vel_range = np.deg2rad(self.parm_stat_iniziale.gradi_al_secondo_init)

        x_dot = 0.0
        theta = self.np_random.uniform(-angle_range_rad, angle_range_rad)
        theta_dot = self.np_random.uniform(-ang_vel_range, ang_vel_range)
        x = self.np_random.uniform(-0.1, 0.1)

        return np.array([x, x_dot, theta, theta_dot], dtype=np.float32)
