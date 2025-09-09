# Interfaccia Grafica Python per il Controllo, l’Addestramento e il Test di un Agente SAC  

## Panoramica del Progetto  

Questo progetto consiste nello sviluppo di un'interfaccia grafica (GUI) in **Python** progettata per interfacciarsi con un sistema di controllo, sia in ambiente virtuale che su hardware reale, sfruttando un agente di **Reinforcement Learning** di tipo **SAC (Soft Actor-Critic)**.  

L'interfaccia offre le seguenti funzionalità principali:  

1. **Gestione della Comunicazione Seriale**  
   La GUI consente l'apertura e la gestione di una comunicazione seriale con dispositivi hardware esterni (es. un CartPole robotico), facilitando il collegamento tra software e componente fisica.  

2. **Simulazione Virtuale dell'Agente SAC Pre-addestrato**  
   È possibile simulare il comportamento di un agente SAC già addestrato all'interno di un ambiente virtuale, specificando il numero di step desiderati per l'esecuzione.  

3. **Controllo di un CartPole Reale tramite Comunicazione Seriale**  
   L'interfaccia permette di controllare direttamente un CartPole reale attraverso la porta seriale, inclusa la possibilità di eseguire su di esso una simulazione del comportamento di un agente SAC.  

4. **Test Manuale del CartPole con Azioni Personalizzate**  
   L'utente può inviare manualmente comandi al CartPole reale sotto forma di azioni, che vengono convertite in segnali PWM, utili per attività di test e taratura dei parametri fisici del progetto.  

5. **Addestramento di un Nuovo Agente SAC**  
   È possibile avviare l'addestramento di un nuovo agente SAC direttamente dall'interfaccia. Alcuni parametri, come quelli di training o la frequenza di stampa, possono essere configurati dall'interfaccia, mentre altri sono modificabili solo tramite codice (hardcoded), così come i parametri tecnici passati al costruttore dell'agente.  

6. **Accesso a un'Interfaccia per Fine-Tuning su Hardware Reale**  
   Il sistema include una seconda interfaccia grafica che consente di eseguire il **fine-tuning** di un agente SAC direttamente sul CartPole reale, permettendo un adattamento più preciso del modello all'ambiente fisico attraverso un ulteriore processo di addestramento mirato.  

---  

## Struttura del Progetto  

Il progetto è organizzato in **quattro package principali**, che riflettono le diverse responsabilità del sistema: **GUI**, **Controllo_Seriale**, **Controllo_e_Simulazione**, e **Context**. Di seguito una panoramica dei package e dei file principali, con le rispettive funzionalità.  

---  

### `GUI/`  

Questo package gestisce l'interfaccia grafica principale del progetto. Contiene le classi che compongono la GUI e il sottopackage dedicato al fine-tuning su hardware reale.  

#### Classi principali:  

- **`Index.py`**  
  Entry point del programma. Inizializza e avvia l'interfaccia grafica.  

- **`ArduinoGUI.py`**  
  Implementa l'interfaccia utente per l'interazione con il sistema.  

- **`PyArduinoGUIController.py`**  
  Controller che collega la GUI ad altri moduli, come quelli per il controllo seriale e la simulazione.  

#### Sottopackage:  

##### `FineTuningGUI/`  

Contiene l'interfaccia dedicata al **fine-tuning** di un agente SAC direttamente sul CartPole reale.  

- **`RealTuningGUI.py`**  
  GUI che permette il **fine-tuning** di un agente SAC sull'hardware fisico (CartPole reale).  

---  

### `Controllo_Seriale/`  

Questo package gestisce tutta la comunicazione seriale con l'hardware.  

- **`File_di_appoggio_funzioni.py`**  
  Contiene funzioni di supporto utilizzate internamente per operazioni comuni.  

- **`SerialController.py`**  
  Implementa funzioni utilizzate sia da `PyArduinoGUIController` sia da `SerialSenderManager`. Media il controllo tra interfaccia e comunicazione.  

- **`SerialSenderManager.py`**  
  Classe fondamentale che gestisce la comunicazione seriale su un **thread separato**, garantendo efficienza e asincronia nella comunicazione con l'hardware.  

---  

### `Controllo_e_Simulazione/`  

Package dedicato alla simulazione, training e gestione degli agenti SAC e del loro ambiente virtuale.  

- **`Circ_Buff.py`**  
  Implementazione di un **buffer circolare** con metodi per calcolare medie e altre statistiche, utile per logging e smoothing.  

- **`Pendolo_inverso_Env.py`**  
  Definisce l'**environment fisico simulato**, compresi parametri dinamici, funzioni di reward e logica dell'ambiente.  

- **`PendulumGym.py`**  
  Contiene funzioni come `train()` e `load()` per gestire il ciclo di vita di un **modello SAC**, dall'addestramento al testing.  
  Il modello utilizza la **MlpPolicy** (Multilayer Perceptron) come architettura neurale predefinita, ideale per ambienti con spazio degli stati e delle azioni continuo.  

- **`SACLogger.py`**  
  Utilizza **LivePlot** per visualizzare l'andamento dell'addestramento in tempo reale.  
  La classe fornisce metodi semplici da utilizzare e si integra nell'`_init_logger(self)` contenuto nel `__init__` di **`Pendolo_inverso_Env.py`**.  

- **`ModelManagerGUI.py`**  
  Classe che fornisce funzionalità per **caricare, simulare e trasferire modelli SAC** (sim-to-real), e gestire le operazioni relative alla loro esecuzione.  

---  

### `Context/`  

- **`AppContext.py`**  
  Classe centrale per la **gestione del contesto applicativo**. Contiene variabili e oggetti condivisi tra i diversi moduli del progetto, semplificando l'integrazione e la comunicazione tra componenti.  

---  

## Riepilogo  

La suddivisione in package riflette una struttura **modulare e scalabile**, che separa chiaramente le responsabilità:  

| Package                     | Responsabilità Principale                                   |  
|-----------------------------|------------------------------------------------------------|  
| `GUI`                       | Interfaccia utente e controllo generale                    |  
| `FineTuningGUI`             | Fine-tuning SAC direttamente su hardware reale             |  
| `Controllo_Seriale`         | Comunicazione asincrona e gestione seriale                 |  
| `Controllo_e_Simulazione`   | Simulazione, training e gestione agenti SAC                |  
| `Context`                   | Gestione centralizzata dello stato e dei parametri globali |  

---  

## Requisiti  

- **Python**: 3.13 o superiore  (attualmente in  3.13.2)
- **IDE consigliato**: PyCharm 2024.3.5 (Community Edition)  
- **Sistema operativo**: Windows  

---  

## Installazione  

Per utilizzare il progetto, è necessario installare i seguenti pacchetti Python:  

| Package                  | Versione      |  
|--------------------------|--------------|  
| cloudpickle              | 3.1.1        |  
| contourpy                | 1.3.3        |  
| cycler                   | 0.12.1       |  
| Farama-Notifications     | 0.0.4        |  
| filelock                 | 3.18.0       |  
| fonttools                | 4.59.0       |  
| fsspec                   | 2025.7.0     |  
| gymnasium                | 1.2.0        |  
| Jinja2                   | 3.1.6        |  
| kiwisolver               | 1.4.8        |  
| MarkupSafe               | 3.0.2        |  
| matplotlib               | 3.10.5       |  
| mpmath                   | 1.3.0        |  
| networkx                 | 3.5          |  
| numpy                    | 2.3.2        |  
| packaging                | 25.0         |  
| pandas                   | 2.3.1        |  
| pillow                   | 11.3.0       |  
| pygame                   | 2.6.1        |  
| pyparsing                | 3.2.3        |  
| pyserial                 | 3.5          |  
| python-dateutil          | 2.9.0.post0  |  
| pytz                     | 2025.2       |  
| six                      | 1.17.0       |  
| stable_baselines3        | 2.7.0        |  
| sympy                    | 1.14.0       |  
| torch                    | 2.7.1        |  
| typing_extensions        | 4.14.1       |  
| tzdata                   | 2025.2       |  

---  

### Installazione Rapida  

Per installare tutte le dipendenze in un solo comando:  

```bash
pip install cloudpickle==3.1.1 contourpy==1.3.3 cycler==0.12.1 Farama-Notifications==0.0.4 filelock==3.18.0 fonttools==4.59.0 fsspec==2025.7.0 gymnasium==1.2.0 Jinja2==3.1.6 kiwisolver==1.4.8 MarkupSafe==3.0.2 matplotlib==3.10.5 mpmath==1.3.0 networkx==3.5 numpy==2.3.2 packaging==25.0 pandas==2.3.1 pillow==11.3.0 pygame==2.6.1 pyparsing==3.2.3 pyserial==3.5 python-dateutil==2.9.0.post0 pytz==2025.2 six==1.17.0 stable_baselines3==2.7.0 sympy==1.14.0 torch==2.7.1 typing_extensions==4.14.1 tzdata==2025.2
```

---

## Come Utilizzare

Per utilizzare il progetto scaricare la cartella:

**`CODICE.zip`** in cui si troveranno tutti i file py.
Per il codice Matlab leggere il paragrafo **"Informazioni sul Microcontrollore Arduino"**

Tutte le informazioni necessarie per il corretto utilizzo dell'interfaccia sono disponibili nel file:

**`GUIDA_all_uso_dell_interfaccia.pdf`**

Assicurati di consultare questo documento per istruzioni dettagliate su:

- Avvio dell’interfaccia grafica  
- Connessione seriale  
- Simulazione e controllo dell'agente SAC  
- Fine-tuning sul CartPole reale/simulato  
- Parametri configurabili


---

## Informazioni sul Microcontrollore Arduino

Una parte delle informazioni riguardanti:

- Il **caricamento del codice** sul microcontrollore Arduino  
- La **struttura del codice embedded**  
- Le **funzionalità implementate lato Arduino**

Sono documentate all'interno di una **repository separata**, creata nell’ambito di una **precedente tesi di laurea triennale**. Alcuni dettagli tecnici non sono inclusi in questo progetto, pertanto è necessario consultare quella risorsa per ottenere una visione completa e corretta del funzionamento dell’intero sistema.

**Repository Arduino:**  
[Visita la repository](https://github.com/isarlab-department-engineering/CartPoleInterface/tree/main)

### Sezioni Importanti da Consultare

All'interno di quella repository, le parti più rilevanti per l'integrazione con questo progetto sono:

- **Sezione `Dipendenze Simulink`**  
  Contiene tutte le indicazioni fondamentali per la configurazione di Arduino tramite Simulink. È importante seguire scrupolosamente le istruzioni presenti per garantire la compatibilità con la parte hardware.

- **Cartella `Pendolo Inverso Simulink`**  
  Include i **codici MATLAB e Simulink** necessari per il controllo del sistema fisico del pendolo inverso. Questa sezione può essere utile per comprendere il comportamento del codice dell'Arduino e per l’eventuale riconfigurazione del modello.

**Nota Importante**  
Per usare il controllo su hardware reale, è **obbligatorio configurare correttamente Arduino tramite Simulink**, come spiegato nella repository. La compatibilità tra software e componente embedded dipende da questa configurazione.
