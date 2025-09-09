class AppContext:
    """
    Classe per la gestione centralizzata di oggetti/istanze condivise.

    Permette di registrare, recuperare, modificare e rimuovere oggetti
    utilizzati in diverse parti dell'applicazione, facilitando la gestione
    dello stato e delle dipendenze (service locator pattern).
    """

    def __init__(self):
        """
        Inizializza il contesto con un dizionario vuoto per i servizi.
        """
        self._services = {}

    def register(self, name: str, instance):
        """
        Registra un oggetto con un nome specifico.

        Args:
            name (str): Nome identificativo del servizio.
            instance: Istanza dell'oggetto da registrare.
        """
        self._services[name] = instance

    def get(self, name: str):
        """
        Recupera un oggetto registrato con il nome specificato.

        Args:
            name (str): Nome del servizio da recuperare.

        Returns:
            object | bool: L'istanza registrata se esiste, altrimenti False.
        """
        if not self.exists(name):
            return False
        return self._services.get(name)

    def unregister(self, name: str):
        """
        Rimuove un oggetto registrato dal contesto.

        Args:
            name (str): Nome del servizio da rimuovere.
        """
        if name in self._services:
            del self._services[name]

    def change_instance(self, name: str, instance):
        """
        Sostituisce un'istanza esistente con una nuova.

        Args:
            name (str): Nome del servizio da aggiornare.
            instance: Nuova istanza da associare al nome.
        """
        if self.exists(name):
            self.unregister(name)
        self.register(name, instance)

    def exists(self, name: str) -> bool:
        """
        Verifica se un oggetto è registrato nel contesto.

        Args:
            name (str): Nome del servizio da verificare.

        Returns:
            bool: True se il servizio è presente, False altrimenti.
        """
        return name in self._services

    def debug_print(self):
        """
        Stampa il contenuto attuale del contesto per scopi di debug.
        """
        print(f"Contenuto attuale del context: {self._services}")


# Istanza singleton globale per accesso centralizzato
Mantieni_context = AppContext()
