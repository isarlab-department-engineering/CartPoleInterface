import numpy as np

class CircularBuffer:
    """
    Buffer circolare a dimensione fissa per la gestione efficiente di sequenze numeriche.

    Utilizzato per tenere traccia di valori recenti (es. ricompense, perdite di training,
    misurazioni in tempo reale), supporta l'inserimento con sovrascrittura automatica e
    il calcolo della media.

    Attributi:
        size (int): Capacità massima del buffer.
        buffer (np.ndarray): Array NumPy che contiene i valori.
        index (int): Indice corrente per l'inserimento.
    """
    def __init__(self, size):
        """
        Inizializza il buffer con dimensione fissa.

        Args:
            size (int): Numero massimo di elementi da mantenere nel buffer.
        """
        self.size = size
        self.buffer = np.zeros(size, dtype=float)
        self.index = 0

    def _circular_index(self, offset):
        """
        Calcola un indice circolare basato su un offset relativo all'indice corrente.

        Args:
            offset (int): Offset rispetto all'indice corrente.

        Returns:
            int: Indice corretto, tenendo conto del wrap-around circolare.
        """
        return (self.index + offset) % self.size

    def insert(self, value):
        """
        Inserisce un nuovo valore nel buffer, sovrascrivendo il più vecchio se necessario.

        Args:
            value (float): Valore da inserire.
        """
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size

    def add_to_current(self, value):
        """
        Aggiunge un valore al più recente inserito nel buffer.

        Args:
            value (float): Quantità da sommare all'ultimo elemento.
        """
        self.buffer[self._circular_index(-1)] += value

    def get_average(self):
        """
        Calcola la media dei valori attualmente presenti nel buffer.

        Returns:
            float: Media dei valori nel buffer.
        """
        return np.mean(self.buffer)

    def current_val(self):
        """
        Restituisce l'ultimo valore inserito nel buffer.

        Returns:
            float: Valore più recente.
        """
        return self.buffer[self._circular_index(-1)]
