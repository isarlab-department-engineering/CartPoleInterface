# Pendolo Inverso

### Panoramica del Progetto
Questo progetto implementa un sistema di pendolo inverso controllato tramite un motore a corrente continua (DC), utilizzando tecniche di apprendimento per rinforzo. Il sistema coinvolge simulazioni, comunicazione con hardware (come Arduino) e modelli di controllo allenati. 
Questo progetto è stato pensato con Python 3.11.9 e Matlab 2024a in mente.
La repository contiene i seguenti componenti principali:

1. **Ambiente di Simulazione (basato su Gymnasium)**: `Pendolo_Inverso_DC_Motor.py`
2. **Addestramento e Test del Modello di Apprendimento per Rinforzo (RL)**: `PendulumGym.py`
3. **Comunicazione Seriale con l'Hardware**: `Serial_Communication.py`
4. **Modello Simulink**: `Pendolo_Inverso.slx`

---

### Descrizione dei File

1. **`Controllore Python`**

    1. **`Pendolo_Inverso_DC_Motor.py`**  
    Questo file contiene l'ambiente personalizzato basato su Gymnasium per simulare un sistema di pendolo inverso controllato da un motore DC.
    - **Classe principale**: `CartPoleEnv`
    - **Caratteristiche principali**:
        - Simula un sistema di pendolo su carrello con parametri come gravità, massa e caratteristiche del motore.
        - Lo spazio delle azioni definisce il segnale PWM (Pulse Width Modulation) che controlla la forza applicata al carrello.
        - Lo spazio delle osservazioni include la posizione e la velocità del carrello, l'angolo del pendolo e la velocità angolare.
        - Include la fisica per il calcolo delle forze sul sistema e integra questi dati nel tempo utilizzando l'integrazione di Eulero.
        - L'ambiente può essere visualizzato (rendering) e supporta condizioni di terminazione basate sulla posizione del carrello o sull'angolo del pendolo.

    2. **`PendulumGym.py`**  
    Questo file integra l'ambiente `CartPoleEnv` con l'algoritmo di apprendimento per rinforzo, in particolare il Deep Q-Network (DQN) dalla libreria `stable_baselines3`.
    - **Caratteristiche principali**:
        - Carica l'ambiente personalizzato `CartPoleEnv`.
        - Un modello DQN pre-addestrato (`dqn_DC_Motor_cartpole`) è già incluso e viene caricato per controllare il sistema.
        - Il modello DQN interagisce con l'ambiente prevedendo azioni da applicare in tempo reale con l'obiettivo di mantenere il pendolo in equilibrio.
        - Per un controllo avanzato, il modello DQN può essere riaddestrato utilizzando diverse politiche o parametri.


    3. **`Serial_Communication.py`**  
    Questo script gestisce la comunicazione tra l'ambiente Python e un setup hardware esterno (ad esempio, un controller Arduino) tramite una porta seriale.
    - **Caratteristiche principali**:
        - Apre e gestisce la comunicazione seriale con l'hardware utilizzando la libreria `pyserial`.
        - Invia segnali di controllo (come abilitazione, homing e movimento del pendolo) tramite comandi predefiniti (`ENABLE`, `HOME`, ecc.).
        - Legge lo stato del pendolo (posizione, velocità, angolo) dall'hardware e utilizza il modello DQN per prevedere la coppia necessaria per la stabilizzazione.
        - Gestisce input della tastiera in tempo reale per controllare l'hardware e passare tra le diverse modalità.

    - **Significato dei Comandi**:
        - `ENABLE`: Abilita o disabilita i motori **Controllato dal tasto `1`**
        - `HOME`: Abilita o disabilità la modalità di homing del pendolo **Controllato dal tasto `2`**
        - `MOVE_CENTER`: Sposta il carrello al centro della base **Controllato dal tasto `3`**
        - `MODE`: Passa dalla modalità di calibrazione alla modalità di stabilizzazione (in modalità di stabilizzazione Arduino ignora i comandi di `HOME` e `MOVE_CENTER` e attua esclusivamente il segnale di controllo generato dal modello DQN) **Controllato dal tasto `4`**
        - `ENABLE_CONTROL`: Abilita o disabilita la generazione del segnale di controllo da parte del modello DQN **Controllato dal tasto `5`**
    
    4. **`File_and_Serial_Manager.py`**
    Questo script Python utilizza la libreria tkinter per creare un'interfaccia grafica che permette di selezionare una porta seriale e scegliere file o directory sul sistema.

    - **Classe principale**: `Manager`
    - **Caratteristiche principali**:
        - Selezione della Porta Seriale: Visualizza una lista di porte seriali disponibili e permette di selezionare una porta.
        - Aggiornamento delle Porte Seriali: Consente di aggiornare la lista delle porte seriali in tempo reale.
        - Selezione di un File ZIP: Apre un dialogo per selezionare un file ZIP dal sistema.
        - Scelta del Percorso di Salvataggio: Permette di selezionare una directory e specificare il nome di un file da salvare.

2. **`Pendolo Inverso Simulink`**

    Vengono spiegati solo i file principali

    1. **`Pendolo_Inverso.slx`**  
    Un modello Simulink per la simulazione del sistema di pendolo inverso nei test in tempo reale. Questo modello può essere utilizzato per confrontare le prestazioni teoriche e quelle reali del sistema.
    Il modello viene eseguito ad un periodo pari a `Tc` (Vedi `LoadData.m`)
    In breve il codice:
       - Legge ogni ciclo dalla seriale
        - Decifra il messaggio letto e lo applica
        - Legge i valori degli encoder e attua sui motori grazie alle S-Function `sfcn_encoder.c` e `sfcn_toPins.c`
        - Ogni 0.05 secondi invia informazioni a python

    2. **`Pendulum_Calibration.slx`**  
    Un modello Simulink per la calibrazione dell'asta del pendolo

    3. **`SaveCalibrateData.m`**
    Uno script Matlab per salvare permanentemente i valori di calibrazione

    4. **`LoadData.m`**
    Uno script Matlab per caricare nel Workspace tutte le variabili utili per la corretta esecuzione del modello `Pendolo_Inverso.slx`

---

### Come Utilizzare

1. **Calibrazione Pendolo**
    Prima di iniziare è necessario calibrare correttamente il pendolo. Se questa è la prima calibrazione, è possibile calibrare il pendolo seguendo le istruzzioni contentute nel file `Pendulum_Calibration.slx`. E' poi necessario eseguire i due script `SaveCalibrateData.m` e `LoadData.m`.
    Se la calibrazione è già stata eseguita in precedenza allora è possibile eseguire semplicemente lo script `LoadData.m`.

2. **Caricamento del codice su Arduino**
    Una volta eseguita la calibrazione, e aver caricato nel Matlab Workspace tutti i dati necessari, è possibile caricare il codice di `Pendolo_Inverso.slx` sulla scheda Arduino cliccando il bottone `Build, Deploy & Start` sotto la sezione `Hardware`.
    In caso non fossero, già presenti, è necessario generare il codice C associato ai due blocchi `S-Function Builder`, questo può essere fatto aprendo i due blocchi presenti nel sottosistema `Pendulum Control` e cliccando il tasto `Build`.

3. **Addestrare o Testare il Modello RL**  
   È possibile modificare il file `PendulumGym.py` per addestrare un nuovo modello DQN o testare il modello pre-addestrato. Per addestrare un nuovo modello, decommentare le linee nel codice relative all'addestramento del modello:
   
   ```python
   model = DQN("MlpPolicy", env, verbose=1)
   model.learn(total_timesteps=100000, log_interval=5)
   model.save("dqn_DC_Motor_cartpole_v100")
   ```

   Per visualizzare i test del modello caricato, assicurati di generare nel seguente modo l'ambiente env:

   ```python
   env = CartPoleEnv(render_mode='human')
   ```

   In fase di addestramento è consigliabile invece generare l'ambiente nel seguente modo, in quanto la fase di rendering va a rallentare l'addestramento:

   ```python
   env = CartPoleEnv()
   ```

4. **Connessione all'Hardware**  
   Lo script `Serial_Communication.py` deve essere utilizzato per interfacciarsi con l'hardware tramite comunicazione seriale. 

   Utilizzare input della tastiera per controllare l'hardware e il modello DQN prevederà le azioni necessarie per mantenere il pendolo in equilibrio in base ai dati ricevuti dai sensori dell'hardware.

    - Attivare `ENABLE` (tasto **1**) e la funzione `HOME` (tasto **2**).
    - Dopo averli attivati, il sistema si dirigerà verso il lato della base e cercherà di eseguire un'azione di homing (non spegnere mai il pulsante Home dopo che il sistema è stato messo in homing).
    - Attendere che il motore smetta di generare suoni prima di procedere.
    - Dopo il processo di homing, attivare `MOVE_CENTER` (tasto **3**) per spostare il carrello al centro del sistema.
    - Ora il sistema dovrebbe essere al centro. 
    - Ora è possibile avviare il controllo. A tale scopo, cambiare la modalità attivando `MODE` (tasto **4**).
    - Sollevare l'asta verso l'alto con la mano per avviare il controllo.
    - Quindi attivare il `ENABLE_CONTROL` (tasto **5**) tenendo l'asta in posizione verticale con la mano.
    - Una volta attivato il controllo di abilitazione, il sistema entrerà in modalità di controllo automatico e cercherà di stabilizzare l'asta.


---

### Dipendenze Python

Per eseguire gli script Python, sono necessarie le seguenti dipendenze:
- `gymnasium 0.29.1`
- `numpy 2.1.1`
- `stable-baselines3 2.3.2`
- `pygame 2.6.1` (per il rendering)
- `pyserial 3.5` (per la comunicazione seriale)
- `keyboard 0.13.5` (per gestire gli input della tastiera)

È possibile installarle tramite pip:
```bash
pip install gymnasium==0.29.1 numpy==2.1.1 stable-baselines3==2.3.2 pygame==2.6.1 pyserial==3.5 keyboard==0.13.5
```

### Dipendenze Simulink

Per eseguire i modelli Simulink sono necessarie le seguenti dipendenze:
- `Arduino Drivers`
- `Simulink Support Package for Arduino Hardware 24.1.3`
- `MATLAB Support for MinGw-w64 C / C ++ Compiler 24.1.0`
- `Embedded Coder 24.1`

Per installare i driver di Arduino, scaricare e installare l'IDE Arduino da questo link. [https://www.arduino.cc/en/software]

Gli Add-On `Simulink Support Package for Arduino Hardware`, `MATLAB Support for MinGw-w64 C / C ++ Compiler` e `Embedded Coder` possono essere installati direttamente da Simulink aprendo un qualsiasi modello e seguento i seguenti passaggi:
-   Apps ->  Get Add-Ons e cercando gli Add-On richiesti 

---

### Note
- `tkinter` è solitamente preinstallato con Python, ma potrebbe essere necessario installarlo manualmente in alcuni ambienti.
- Assicurarsi che il modello Simulink (`Pendolo_Inverso.slx`) sia compatibile con la versione di MATLAB in uso e sia configurato correttamente per interagire con il setup hardware.
- Le impostazioni di comunicazione seriale (porta, velocità) devono corrispondere alla configurazione del proprio hardware (ad esempio, Arduino) per garantire una corretta sincronizzazione.

---
