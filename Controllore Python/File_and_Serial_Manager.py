import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import serial.tools.list_ports

""" Classe per la gestione dei file e delle porte seriali """
class Manager():

    def __init__(self):
        # Crea la finestra principale di tkinter
        self.root = tk.Tk()

        self.root.title("Seleziona Porta Seriale")

        self.label = ttk.Label(self.root, text="Seleziona una porta seriale:")
        self.label.pack(pady=10)

        self.port_combobox = ttk.Combobox(self.root, justify='center')
        self.port_combobox.pack(pady=10)

        self.refresh_button = ttk.Button(self.root, text="Aggiorna Porte", command=self.refresh_ports)
        self.refresh_button.pack(pady=10)

        self.select_button = ttk.Button(self.root, text="Seleziona Porta", command=self.select_port)
        self.select_button.pack(pady=10)

        self.refresh_ports()

    def choose_file(self):
        # Nasconde la finestra principale di tkinter
        self.root.withdraw()
        
        # Apre la finestra di dialogo per la selezione del file, accettando solo file zip
        file_path = filedialog.askopenfilename(
            title="Scegliere un set di dati di allenamento",
            filetypes=[("File zip", "*.zip")]
        )
        
        # Verifica se l'utente ha selezionato un file
        if file_path:
            return file_path
        else:
            return None


    # Funzione per scegliere la cartella e il nome del file
    def save_file(self):
        # Nasconde la finestra principale di tkinter
        self.root.withdraw()
        

        # Apri la finestra di dialogo per il salvataggio
        absolute_path = filedialog.asksaveasfilename(defaultextension=".zip",
                                                filetypes=[("File zip", "*.zip")],
                                                title="Salva il file come")
        
        if absolute_path:
            return absolute_path
        else:
            return None
        
    
    def refresh_ports(self):
        
        ports = serial.tools.list_ports.comports()
        port_list = [(port.device, port.description) for port in ports]

        if not port_list:
            port_list = [("Nessuna porta disponibile", "")]
        
        # Aggiorna la combobox con le porte e le loro descrizioni

        max_width = max(sum(len(port_value) for port_value in port) for port in port_list)

        self.port_combobox['values'] = [f"{device}: {description}" for device, description in port_list]
        self.port_combobox.current(0)  # Seleziona la prima voce
        self.port_combobox.configure(width=max_width)


    def select_port(self):
        
        self.root.deiconify()

        selected_port = self.port_combobox.get()
        if selected_port == "Nessuna porta disponibile":
            messagebox.showwarning("Attenzione", "Nessuna porta seriale disponibile.")
        else:
            # Estrai il nome della porta dalla selezione
            self.port_name = selected_port.split(":")[0]

            self.root.withdraw()
            self.root.quit()  # Chiude la finestra


    def get_serial_port(self):
        self.root.deiconify()
        self.root.mainloop()
        return self.port_name  # Restituisce la porta selezionata

