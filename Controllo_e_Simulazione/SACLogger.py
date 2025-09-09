import numpy as np
from matplotlib import pyplot as plt


class SACLogger:
    """
    Supporto per il logging e la visualizzazione in tempo reale di metriche numeriche
    (ad es. reward, loss) durante l'addestramento o l'esecuzione di agenti SAC.

    Funzionalità:
        - Creazione di grafici live per variabili.
        - Aggiornamento incrementale dei plot.
    """

    def __init__(self):
        """
        Inizializza le strutture interne:
            - plots: dict che associa variabili a dati e componenti grafici.
            - figures: dict per eventuali figure separate.
        """
        self.plots = {}
        self.figures = {}

    def create_liveplot(self, var_name: str) -> None:
        """
        Crea un grafico interattivo per una variabile numerica.

        Args:
            var_name (str): Identificatore della variabile da tracciare.

        Effetti:
            - Apre una figura matplotlib con titolo e legende.
            - Imposta assi 'Steps' e nome variabile.
            - Memorizza figura, asse, linea e dati in self.plots.
            - Attiva plt.ion() per aggiornamenti in tempo reale.
        """
        if var_name in self.plots:
            print(f"Plot per '{var_name}' già esistente.")
            return

        fig, ax = plt.subplots()
        line, = ax.plot([], [], label=var_name)
        ax.set_title(f"Live plot per {var_name}")
        ax.set_xlabel("Steps")
        ax.set_ylabel(var_name)
        ax.legend()

        self.plots[var_name] = {
            "fig": fig,
            "ax": ax,
            "line": line,
            "x_data": [],
            "y_data": []
        }
        plt.ion()
        fig.show()
        fig.canvas.draw()

    def update_liveplot(self, var_name: str, value: float, x: int = None) -> None:
        """
        Aggiorna il grafico live aggiungendo un nuovo punto.

        Args:
            var_name (str): Nome della variabile creata con create_liveplot().
            value (float): Valore da aggiungere.
            x (int, optional): Step su asse x. Default usa indice interno.

        Effetti:
            - Mantiene al massimo 200 punti per plot diversi da 'reward_medio_per_episodio'.
            - Ridisegna il plot.

        Raises:
            ValueError: se il valore non è numerico.
        """
        if var_name not in self.plots:
            print(f"Plot per '{var_name}' non esiste, crea prima con create_liveplot()")
            return

        if not isinstance(value, (int, float)):
            raise ValueError(
                f"Valore per '{var_name}' non è numerico: {value}"
            )

        data = self.plots[var_name]
        x_data = data["x_data"]
        y_data = data["y_data"]

        if var_name != "reward_medio_per_episodio" and len(x_data) > 200:
            x_data.pop(0)
            y_data.pop(0)

        x_data.append(x if x is not None else len(x_data))
        y_data.append(value)

        line = data["line"]
        ax = data["ax"]
        fig = data["fig"]

        line.set_xdata(np.array(x_data, dtype=np.float32))
        line.set_ydata(np.array(y_data, dtype=np.float32))

        ax.relim()
        ax.autoscale_view()

        fig.canvas.draw()
        fig.canvas.flush_events()

    def reset_liveplot(self, var_name: str) -> None:
        """
        Resetta i dati di un liveplot eliminando tutti i punti.

        Args:
            var_name (str): Nome del plot da resettare.

        Effetti:
            - Svuota x_data e y_data.
            - Ripristina assi e linea.
            - Ridisegna figura.
        """
        if var_name not in self.plots:
            print(f"Plot per '{var_name}' non esiste, niente da resettare.")
            return

        data = self.plots[var_name]
        data["x_data"].clear()
        data["y_data"].clear()

        line = data["line"]
        ax = data["ax"]
        fig = data["fig"]

        line.set_xdata([])
        line.set_ydata([])

        ax.relim()
        ax.autoscale_view()

        fig.canvas.draw()
        fig.canvas.flush_events()
