import math
from typing import Optional, Tuple, Union

import numpy as np

import gymnasium as gym
from gymnasium import logger, spaces
from gymnasium.envs.classic_control import utils
from gymnasium.error import DependencyNotInstalled


class CartPoleEnv(gym.Env[np.ndarray, Union[int, np.ndarray]]):
    """
    ## Descrizione

    Questo ambiente corrisponde a una versione modificata del problema del cart-pole (pendolo su carrello) 
    descritto da Barto, Sutton e Anderson. Il problema originale è documentato in 
    ["Neuronlike Adaptive Elements That Can Solve Difficult Learning Control Problem"].
    (https://ieeexplore.ieee.org/document/6313077)
    
    Un'asta (il pendolo) è collegata tramite un giunto non attuato a un carrello che si muove su una pista senza attrito.
    Il pendolo è inizialmente posizionato verticalmente sul carrello, e l'obiettivo è bilanciare l'asta applicando forze 
    a sinistra o a destra sul carrello.

    ## Spazio delle azioni

    L'azione è un array con forma `(1,)` che può assumere valori `{0, 1, ..., 2* self.max_action - 1}`. Indica il valore PWM
    della tensione applicata al motore DC.
    
            Azione                 |                Effetto
    _______________________________|_________________________________________________
    -           0:                 | Valore max_action PWM a sinistra               |
    -           1:                 | ( max_action - 1 ) PWM a sinistra              |
    .                              |                                                |
    .                              |                                                |
    - ( 2 * self.max_action ) - 1: | ( max_action - 1 ) PWM a destra                |
    - ( 2 * self.max_action ):     | Valore max_action PWM a destra                 |
    _______________________________|________________________________________________|

    Per questo motivo è importante che la variabile self.max_action sia inizializzata con un valore compreso tra 0 e 255.

    **Nota**: La velocità che viene ridotta o aumentata dalla forza applicata non è fissa e dipende dall'angolo 
    dell'asta. Il centro di gravità del pendolo varia l'energia necessaria per spostare il carrello.

    ## Spazio delle osservazioni

    L'osservazione è un array con forma `(4,)` con i seguenti valori che corrispondono a posizioni e velocità:

    | Num | Osservazione                  | Min                 | Max               |
    |-----|-------------------------------|---------------------|-------------------|
    | 0   | Posizione del carrello        | -0.8                | 0.8               |
    | 1   | Velocità del carrello         | -Inf                | Inf               |
    | 2   | Angolo del pendolo            | ~ -0.418 rad (-24°) | ~ 0.418 rad (24°) |
    | 3   | Velocità angolare del pendolo | -Inf                | Inf               |

    **Nota:** Sebbene i limiti sopra indichino i valori possibili per ogni elemento dello spazio di osservazione,
    non riflettono necessariamente i valori consentiti nello stato dell'episodio. In particolare:
    - La posizione del carrello può variare tra `(-0.8, 0.8)`, ma l'episodio termina se il carrello esce dalla gamma `(-0.4, 0.4)`.
    - L'angolo del pendolo può essere osservato tra `(-0.418, 0.418)` radianti (o **±24°**), ma l'episodio termina
      se l'angolo non rientra nel range `(-0.2095, 0.2095)` (o **±12°**).

    ## Ricompense
    L'obiettivo è mantenere l'asta in equilibrio il più a lungo possibile. Viene data una ricompensa per ogni passo, compreso il passo finale.
    La soglia di ricompensa predefinita è 500.
    Inoltre, la ricompensa è proporzionale alla posizione del carrello, con maggiori ricompense se il carrello è vicino al centro.

    Se `sutton_barto_reward=True`, viene assegnata una ricompensa di `0` per ogni passo non terminato e `-1` per il passo terminante.
    La soglia di ricompensa è 0 per v0 e v1.

    ## Stato iniziale
    Le osservazioni sono assegnate a valori casuali uniformi in `(-0.05, 0.05)`.

    ## Fine dell'episodio
    L'episodio termina se una delle seguenti condizioni si verifica:

    1. Terminazione: L'angolo del pendolo è maggiore di ±12°
    2. Terminazione: La posizione del carrello è maggiore di ±0.4 (il centro del carrello raggiunge il bordo dello schermo)
    3. Troncamento: La lunghezza dell'episodio supera 500 step.

    ## Argomenti

    CartPole ha solo `render_mode` come parola chiave per `gymnasium.make`.
    Al reset, il parametro `options` permette di cambiare i limiti usati per determinare lo stato casuale.

    """

    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 50,
    }

    def __init__(
        self, sutton_barto_reward: bool = False, render_mode: Optional[str] = None
    ):
        self._sutton_barto_reward = sutton_barto_reward

        #### Valori nominali del pendolo 
        self.gravity = 9.81  # Gravità terrestre
        self.masscart = 0.6  # Massa del carrello
        self.masspole = 0.1528  # Massa del pendolo
        self.total_mass = self.masspole + self.masscart  # Massa totale del sistema
        self.length = 0.2  # Lunghezza del pendolo (in realtà metà della lunghezza effettiva)
        self.polemass_length = self.masspole * self.length  # Prodotto tra la massa del pendolo e la sua lunghezza

        ##### Valori nominali del motore DC
        self.max__nominal_voltage = 12.0  # Tensione massima del motore
        self.Ra_nominal = 180/83  # Resistenza nominale
        self.K_nominal = 18/(83*math.pi)  # Costante elettromeccanica nominale
        self.r_nominal = 0.0145  # Raggio nominale

        self.margin_of_error = 0.05  # Margine di errore per i valori nominali

        ##### Valori reali del motore DC (± self.margin_of_error% di variazione)
        self.max_voltage = self.max__nominal_voltage*(self.np_random.uniform(1-self.margin_of_error, 1+self.margin_of_error))
        self.Ra = self.Ra_nominal*(self.np_random.uniform(1-self.margin_of_error, 1+self.margin_of_error))
        self.K = self.K_nominal*(self.np_random.uniform(1-self.margin_of_error, 1+self.margin_of_error))
        self.r = self.r_nominal*(self.np_random.uniform(1-self.margin_of_error, 1+self.margin_of_error))

        self.old_voltage = 0.0  # Tensione precedente applicata
        self.max_action = 175.0  # Azione massima (PWM)
        self.PWM_resolution = 255.0  # Risoluzione del segnale PWM

        """ L'Arduino esegue il loop ogni self.tau = 0.005 secondi, ma comunica con Python ogni self.period = 0.05 secondi.
        Tra due comunicazioni, Arduino continua ad applicare l'ultimo segnale di controllo generato. """
        self.period = 0.05  # Periodo di comunicazione con Arduino (in secondi)
        self.tau = 0.005  # Secondi tra gli aggiornamenti di stato


        """ Il codice Arduino traduce il segnale di controllo in un valore PWM secondo la relazione: PWM = torque/5.8824 """
        self.torque_pwm_constant = 5.8824  # Costante per convertire coppia in valore PWM

        # Angolo oltre il quale l'episodio fallisce
        self.theta_threshold_radians = 12 * 2 * math.pi / 360  # ±12° in radianti
        self.x_threshold = 0.4  # Posizione limite del carrello

        # Imposta il limite dell'angolo a 2 * theta_threshold_radians per garantire che l'osservazione rimanga valida        
        high = np.array(
            [
                self.x_threshold * 2,
                np.inf,
                self.theta_threshold_radians * 2,
                np.inf,
            ],
            dtype=np.float32,
        )

        # Spazio delle azioni e delle osservazioni
        self.action_space = spaces.Discrete(2*int(self.max_action) + 1)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

        self.render_mode = render_mode

        # Variabili per il rendering
        self.screen_width = 600
        self.screen_height = 400
        self.screen = None
        self.clock = None
        self.isopen = True
        self.state: np.ndarray | None = None

        self.steps_beyond_terminated = None


    # Metodo che aggiorna il sistema
    def step(self, action):
        assert self.action_space.contains(
            action
        ), f"{action!r} ({type(action)}) invalid"
        assert self.state is not None, "Call reset before using step method."
        x, x_dot, theta, theta_dot = self.state

        """ Poiché c'è sempre un ciclo di ritardo da quando Arduino genera i valori di 
        [x, x_dot, theta, theta_dot] e quando riceve il nuovo segnale di controllo,
        durante quel ciclo Arduino continua ad applicare il vecchio segnale di tensione. """
        voltage = self.old_voltage

         # Calcola la forza applicata in base alla tensione e alle caratteristiche del motore
        force = (self.K/(self.Ra*self.r))*(voltage - self.K*x_dot/self.r)
        x, x_dot, theta, theta_dot = self.apply_force(force)

        """ Nei cicli successivi, l'azione scelta determinerà il nuovo segnale di controllo """
        PWM_value = self.action_to_PWM(action) # Converte l'azione in un valore di onda PWM

        # Ricalcola la forza con la nuova tensione
        voltage = self.max_voltage * PWM_value / self.PWM_resolution
        self.old_voltage = voltage
        force = (self.K/(self.Ra*self.r))*(voltage - self.K*x_dot/self.r)

        # Applica la forza per più cicli per simulare l'aggiornamento dello stato
        for i in range(int(self.period/self.tau) - 1):            
            x, x_dot, theta, theta_dot = self.apply_force(force)

        # Aggiorna lo stato del sistema
        self.state = np.array((x, x_dot, theta, theta_dot), dtype=np.float64)

        # Controlla se l'episodio deve terminare
        terminated = bool(
            x < -self.x_threshold
            or x > self.x_threshold
            or theta < -self.theta_threshold_radians
            or theta > self.theta_threshold_radians
        )

        # Ricompensa in base allo stato del sistema
        if not terminated:
            if self._sutton_barto_reward:
                reward = 0.0
            else:
                reward = (self.x_threshold-abs(x))/self.x_threshold

        elif self.steps_beyond_terminated is None:
            # Il pendolo è appena caduto
            self.steps_beyond_terminated = 0

            reward = -1.0 if self._sutton_barto_reward else 1.0
        else:
            if self.steps_beyond_terminated == 0:
                logger.warn(
                    "You are calling 'step()' even though this environment has already returned terminated = True. "
                    "You should always call 'reset()' once you receive 'terminated = True' -- any further steps are undefined behavior."
                )
            self.steps_beyond_terminated += 1

            reward = -1.0 if self._sutton_barto_reward else 0.0

        # Renderizza il sistema se richiesto
        if self.render_mode == "human":
            self.render()

        # truncation=False as the time limit is handled by the `TimeLimit` wrapper added during `make`
        return np.array(self.state, dtype=np.float32), reward, terminated, False, {}


    """ Questa funzione riceve in ingresso la forza da applicare al carrello,e attraverso l'equazione del moto
    calcola l'accelerazione lineare del carrello e l'accelerazione angolare del pendolo.
    L'integrazione di Eulero viene utilizzata per incrementare le posizioni e le velocità """
    def apply_force(self, force):

        x, x_dot, theta, theta_dot = self.state
        
        sintheta = np.sin(theta)
        costheta = np.cos(theta)


        # Calcolo delle accelerazioni angolari e lineari
        temp = (
            force + self.polemass_length * np.square(theta_dot) * sintheta
        ) / self.total_mass
        
        theta_acc = (self.gravity * sintheta - costheta * temp) / (
            self.length
            * (4.0 / 3.0 - self.masspole * np.square(costheta) / self.total_mass)
        )
        
        x_acc = temp - self.polemass_length * theta_acc * costheta / self.total_mass 
        
         # Aggiorna le velocità e le posizioni usando l'integrazione di Eulero
        theta_dot = theta_dot + theta_acc * self.tau
        theta = theta + theta_dot * self.tau

        x_dot = x_dot + x_acc * self.tau
        x = x + x_dot * self.tau

        # Aggiorna lo stato del sistema
        self.state = np.array((x, x_dot, theta, theta_dot), dtype=np.float64)
        return [x, x_dot, theta, theta_dot]


    """ Mappa l'azione dall'intervallo [0; 2*self.max_action] all'intervallo di onda PWM [-self.max_action; +self.max_action] """
    def action_to_PWM(self, action):
        PWM_value = (action - self.max_action)
        return PWM_value


    """ Converte l'azione in coppia applicata al motore """
    def action_to_torque(self, action):
        PWM_value = self.action_to_PWM(action)
        torque = PWM_value*self.torque_pwm_constant
        return torque
    

    """ Metodo di reset dell'ambiente """
    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        # Note that if you use custom reset bounds, it may lead to out-of-bound
        # state/observations.
        low, high = utils.maybe_parse_reset_bounds(
            options, -0.05, 0.05  # default low
        )  # default high
        self.state = self.np_random.uniform(low=low, high=high, size=(4,))
        self.steps_beyond_terminated = None

        # Applica variazioni ai valori nominali del motore
        self.max_voltage = self.max__nominal_voltage*(self.np_random.uniform(1-self.margin_of_error, 1+self.margin_of_error))
        self.r = self.r_nominal*(self.np_random.uniform(1-self.margin_of_error, 1+self.margin_of_error))
        self.Ra = self.Ra_nominal*(self.np_random.uniform(1-self.margin_of_error, 1+self.margin_of_error))
        self.K = self.K_nominal*(self.np_random.uniform(1-self.margin_of_error, 1+self.margin_of_error))

        if self.render_mode == "human":
            self.render()
        return np.array(self.state, dtype=np.float32), {}


    """ Metodo per renderizzare l'ambiente """
    def render(self):
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
            )
            return

        try:
            import pygame
            from pygame import gfxdraw
        except ImportError as e:
            raise DependencyNotInstalled(
                'pygame is not installed, run `pip install "gymnasium[classic-control]"`'
            ) from e

        if self.screen is None:
            pygame.init()
            if self.render_mode == "human":
                pygame.display.init()
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height)
                )
            else:  # mode == "rgb_array"
                self.screen = pygame.Surface((self.screen_width, self.screen_height))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        world_width = self.x_threshold * 2
        scale = self.screen_width / world_width
        polewidth = 10.0
        polelen = scale * (2 * self.length)
        cartwidth = 50.0
        cartheight = 30.0

        if self.state is None:
            return None

        x = self.state

        self.surf = pygame.Surface((self.screen_width, self.screen_height))
        self.surf.fill((255, 255, 255))

        l, r, t, b = -cartwidth / 2, cartwidth / 2, cartheight / 2, -cartheight / 2
        axleoffset = cartheight / 4.0
        cartx = x[0] * scale + self.screen_width / 2.0  # MIDDLE OF CART
        carty = 100  # TOP OF CART
        cart_coords = [(l, b), (l, t), (r, t), (r, b)]
        cart_coords = [(c[0] + cartx, c[1] + carty) for c in cart_coords]
        gfxdraw.aapolygon(self.surf, cart_coords, (0, 0, 0))
        gfxdraw.filled_polygon(self.surf, cart_coords, (0, 0, 0))

        l, r, t, b = (
            -polewidth / 2,
            polewidth / 2,
            polelen - polewidth / 2,
            -polewidth / 2,
        )

        pole_coords = []
        for coord in [(l, b), (l, t), (r, t), (r, b)]:
            coord = pygame.math.Vector2(coord).rotate_rad(-x[2])
            coord = (coord[0] + cartx, coord[1] + carty + axleoffset)
            pole_coords.append(coord)
        gfxdraw.aapolygon(self.surf, pole_coords, (202, 152, 101))
        gfxdraw.filled_polygon(self.surf, pole_coords, (202, 152, 101))

        gfxdraw.aacircle(
            self.surf,
            int(cartx),
            int(carty + axleoffset),
            int(polewidth / 2),
            (129, 132, 203),
        )
        gfxdraw.filled_circle(
            self.surf,
            int(cartx),
            int(carty + axleoffset),
            int(polewidth / 2),
            (129, 132, 203),
        )

        gfxdraw.hline(self.surf, 0, self.screen_width, carty, (0, 0, 0))

        self.surf = pygame.transform.flip(self.surf, False, True)
        self.screen.blit(self.surf, (0, 0))
        if self.render_mode == "human":
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"])
            pygame.display.flip()

        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )

    """ Metodo per chiudere l'ambiente """
    def close(self):
        if self.screen is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()
            self.isopen = False


