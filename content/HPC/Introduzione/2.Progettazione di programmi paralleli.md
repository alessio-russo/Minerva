
## Parallel computing

Il parallel computing è la tecnica di programmazione utilizzata per dividere il carico di lavoro in vari **task**, che verranno poi distribuiti ed eseguiti sfruttando i molteplici livelli di parallelismo offerti dai sistemi HPC (High-Performance Computing). Questa tecnica si avvale principalmente di due metodi di decomposizione: la decomposizione di dominio e la decomposizione funzionale.

**Decomposizione di dominio (parallelismo sui dati)**

La decomposizione di dominio è una tecnica utilizzata per gestire efficacemente l'elaborazione di dataset di grandi dimensioni costituiti da dati organizzati in strutture regolari. Questa strategia prevede la suddivisione del dataset in sottodomini più piccoli, ognuno dei quali viene assegnato a un task specifico per l'elaborazione. La peculiarità di questa metodologia è che ogni task esegue le stesse operazioni, ma opera su un insieme di dati diverso. La decomposizione di dominio è particolarmente utile quando i dati sono organizzati in strutture regolari come array e matrici, che possono avere dimensioni variabili (1D, 2D, e così via).

**Decomposizione funzionale (parallelismo sui task)**

La decomposizione funzionale è un'altra strategia fondamentale nel calcolo parallelo, caratterizzata dalla divisione di un problema complesso in insiemi di elaborazioni distinte e indipendenti. Questo approccio comporta l'identificazione dei diversi task che possono essere eseguiti in parallelo, ciascuno assegnato a processi distinti.

**Vantaggi**

- **Scalabilità**: Questa metodologia si scala bene con l'aumentare del numero di elaborazioni indipendenti

- **Specializzazione**: Ogni task può essere ottimizzato per una specifica funzione, permettendo un utilizzo più efficiente delle risorse e una maggiore efficienza nell'elaborazione.

**Svantaggi**

- **Complessità**: La strategia risulta essere vantaggiosa principalmente per problemi di elaborazione complessi. Per task semplici o per problemi che non si prestano facilmente alla segregazione funzionale, i benefici del parallelismo potrebbero non giustificarne la complessità

- **Gestione della concorrenza**: La necessità di coordinare task indipendenti che potrebbero dover accedere a risorse condivise introduce una complessità addizionale nella gestione della concorrenza

## Comunicazione nelle applicazioni parallele

La comunicazione nelle applicazioni parallele è un aspetto fondamentale che determina l'efficienza e l'efficacia dell'esecuzione parallela, in particolare nei modelli a memoria distribuita. Esistono diverse tipologie di applicazioni:

**Tightly Coupled Applications**

Le applicazioni parallele strettamente accoppiate (tightly coupled) richiedono un'intensa comunicazione tra i task, spesso a ogni iterazione dell'applicazione. In queste applicazioni, la frequenza di comunicazione è elevata perché i dati processati da un task sono direttamente influenzati dai risultati degli altri task vicini.

**Loosely Coupled Applications**

Al contrario, le applicazioni parallele debolmente accoppiate (loosely coupled) sono caratterizzate da comunicazioni meno frequenti tra i task. Questi scambi di dati possono avvenire principalmente all'inizio dell'esecuzione, per distribuire compiti o dati iniziali ai vari task, e alla fine, per raccogliere e aggregare i risultati. 

**Embarrassingly Parallel Problems**

I problemi definiti come "embarassingly parallel" rappresentano il caso ideale di parallelismo, dove la comunicazione tra i task è praticamente assente o del tutto inutile. Questi problemi consentono una decomposizione in task che possono essere eseguiti completamente in parallelo, senza necessità di scambiare informazioni.

#### Comunicazione tra i Task

La comunicazione tra i task può essere classificata in due categorie principali: comunicazione punto-punto e comunicazione collettiva.

**Comunicazione punto-punto**

La comunicazione punto-punto si verifica tra due task specifici, dove un task invia dati direttamente a un altro

**Comunicazione collettiva**

La comunicazione collettiva, d'altra parte, coinvolge tutti i task all'interno di un'applicazione parallela. Questi schemi di comunicazione sono usati per operazioni che richiedono la partecipazione di tutti i task. Esistono diverse varianti di comunicazioni collettive, ognuna con un proprio scopo specifico:

- **Broadcast.** Un singolo task invia lo stesso dato a tutti gli altri task del gruppo
- **Scatter.** Lo scatter distribuisce parti diverse di un insieme di dati dal task sorgente a tutti gli altri task nel gruppo. Ogni task riceve una porzione unica e distinta del dataset originale.
- **Gather.** Il gather è l'operazione inversa dello scatter. Raccoglie dati da tutti i task del gruppo in un unico task destinatario. Ogni task invia una porzione di dati che viene aggregata nel dataset complessivo dal task ricevente.
- **Reduction.** La reduction è un'operazione che combina i dati da tutti i task del gruppo utilizzando un'operazione specifica (come somma, massimo, minimo, ecc.) e restituisce il risultato finale a un singolo task o a tutti i task.

#### Costo della Comunicazione

Il costo della comunicazione nelle applicazioni parallele e distribuite è un fattore critico che può influenzare significativamente le prestazioni complessive. Questo costo è determinato dal tempo necessario per trasmettere i messaggi tra i task, e può variare a seconda della natura della comunicazione (punto-punto o collettiva) e della topologia della rete.
 
**Comunicazioni punto-punto**

Per le comunicazioni punto-punto, il tempo di trasmissione di un messaggio ($T_{\text{mess}}$) può essere calcolato attraverso la formula 

$T_{\text{mess}} = T_{\text{lat}} + \frac{M}{\text{Band}}$

Dove:

- $T_{\text{lat}}$ è il tempo impiegato per stabilire la comunicazione (espresso in secondi)
- $M$ è la dimensione del messaggio (in byte)
- $\text{Band}$ è la larghezza di banda della rete (Byte/s)

**Comunicazioni collettive**

Nel caso delle comunicazioni collettive, il tempo di comunicazione $T_{\text{coll}}$ può essere calcolato attraverso la formula

$T_{\text{coll}} = T_{\text{mess}} \cdot (P - 1)$

Dove:

- $T_{\text{mess}}$ è il tempo di trasmissione di un messaggio
- $P$ è il numero di task coinvolti 

Utilizzando una strategia di tipo divide-et-impera, il costo della comunicazione nelle operazioni collettive può essere notevolmente ridotto. Questo approccio prevede la divisione dei task in gruppi più piccoli e l'esecuzione parallela delle comunicazioni all'interno di questi gruppi, seguita dall'aggregazione dei risultati. Il costo della comunicazione può quindi essere migliorato a una complessità logaritmica rispetto al numero di task $O(\log{⁡P})$ .

### Sincronizzazione

La sincronizzazione è un meccanismo fondamentale nelle applicazioni parallele, essenziale per coordinare l'esecuzione dei task in presenza di dipendenze tra sezioni di codice o dati. Questa necessità si manifesta sia nei modelli a memoria distribuita che a memoria condivisa, e le strategie di sincronizzazione possono variare a seconda se debbano coinvolgere solo due (o più) task o tutti i task di un sistema.

**Tecniche di Sincronizzazione (Sistemi a Memoria Condivisa)**

In sistemi a memoria condivisa, dove più task o thread condividono lo stesso spazio di memoria, gli strumenti più comuni per la sincronizzazione sono:

- **Lock e Mutex**: Questi meccanismi forniscono l'accesso esclusivo a sezioni di codice o risorse, permettendo a un solo task per volta di eseguire una determinata sezione critica

- **Semafori**: Funzionano come contatori che gestiscono l'accesso a una o più risorse condivise, limitando il numero di task che possono accedervi contemporaneamente 

**Tecniche di Sincronizzazione (Sistemi a Memoria Distribuita)**

Nei sistemi a memoria distribuita, dove ogni task opera in un proprio spazio di memoria privato, la sincronizzazione avviene tipicamente attraverso:

- **Scambio di Messaggi**: La sincronizzazione è ottenuta comunicando esplicitamente tra i task. 

**Barriere**

Le barriere sono uno strumento di sincronizzazione usato sia nei sistemi a memoria distribuita che condivisa. Funzionano costringendo tutti i task partecipanti ad attendere presso un punto di sincronizzazione fino a che tutti non vi hanno raggiunto. Questo meccanismo è particolarmente utile per sincronizzare fasi di lavoro in applicazioni che procedono a step iterativi.


Il **tempo di inattività** (tempo di **idle**) di un task, dovuto a dipendenze, attese su lock o semafori, o attese per l'arrivo di messaggi, è un fattore critico nelle prestazioni dell'applicazione. Una gestione inefficace della sincronizzazione può portare a elevati tempi di inattività, causando un degrado delle performance complessive.

### Bilanciamento del carico

Il bilanciamento del carico, o load balancing, ha come obiettivo la distribuzione del lavoro in modo equilibrato tra tutti i processi o i task disponibili, in modo da minimizzare il tempo di inattività (idle time) e massimizzare l'utilizzo delle risorse computazionali. Un bilanciamento del carico ottimale assicura che nessun singolo nodo o processo sia sovraccaricato mentre altri sono inattivi, prevenendo così i colli di bottiglia e migliorando il throughput generale del sistema.

Una delle tecniche comuni impiegate per il bilanciamento del carico è il modello master-slave, noto anche come manager-worker. In questo modello, un processo centrale (il master o manager) ha il compito di orchestrare la distribuzione del lavoro, suddividendo il carico complessivo in task più piccoli. Questi task vengono poi assegnati dinamicamente a un pool di processi lavoratori (gli slave o worker), che eseguono il lavoro assegnato.

### Granularità

La decomposizione del problema in un contesto di calcolo parallelo può essere affrontata con diversi livelli di granularità:

**Parallelismo a Grana Fine (Fine-Grained Parallelism)**

Il parallelismo a grana fine si caratterizza per la suddivisione del carico di lavoro in piccolissime unità di elaborazione, che possono essere eseguite quasi simultaneamente su più processori. Questo approccio è particolarmente utile per:

- **Bilanciare il carico**: Con tante piccole unità di lavoro, è più facile distribuire equamente il carico tra i diversi processori o core

- **Diminuire l'overhead di sincronismo**: La ridotta dimensione dei task può semplificare le esigenze di sincronizzazione

Tuttavia, il parallelismo a grana fine può anche portare a:

- **Aumento delle comunicazioni**: La necessità di coordinare molti piccoli task può incrementare il volume delle comunicazioni tra processori, specialmente in architetture a memoria distribuita

- **Overhead di comunicazione**: L'aumento delle comunicazioni può introdurre un significativo overhead

**Parallelismo a Grana Grossa (Coarse-Grained Parallelism)**

Il parallelismo a grana grossa, al contrario, implica una suddivisione del carico di lavoro in unità più grandi, che vengono eseguite parallelamente. Questo metodo è vantaggioso per:

- **Migliorare il rapporto tra Calcolo e Comunicazioni**: Con task più grandi, il rapporto tra il tempo speso per calcoli effettivi e il tempo speso per comunicazioni tende a migliorare, riducendo l'overhead di comunicazione

- **Semplificare la gestione**: La gestione di un numero minore di task di dimensioni maggiori può essere più semplice rispetto alla coordinazione di molti piccoli task

D'altra parte, il parallelismo a grana grossa presenta alcune sfide:

- **Bilanciamento del carico**: Può essere più difficile assicurare che il carico di lavoro sia distribuito equamente tra tutti i processori o core, specialmente se i task hanno dimensioni o tempi di esecuzione molto diversi

- **Flessibilità**: Ridurre il numero di task può limitare la flessibilità nell'adattarsi dinamicamente a cambiamenti nel carico di lavoro o nella disponibilità delle risorse

### Performance del parallelismo 

**Speedup**

Lo **speedup** di un'applicazione parallela è definito come il rapporto tra il tempo di esecuzione della migliore implementazione seriale del programma $T_{seriale}$ e il tempo di esecuzione della versione parallela dello stesso programma su $P$ processori $T_{parallelo}$ :

$\text{Speedup} = \dfrac{T_{seriale}}{T_{parallelo}}$

Nel caso ideale, lo speedup è direttamente proporzionale al numero di processori, il che significa che raddoppiando il numero di processori si dovrebbe teoricamente dimezzare il tempo di esecuzione. Tuttavia, a causa dell'overhead introdotto dalla sincronizzazione e dalla comunicazione tra i processori, questo ideale è raramente raggiunto.

**Efficienza**

L'**efficienza** $E$ misura quanto efficacemente vengono utilizzate le unità di processamento durante l'esecuzione parallela. È definita come il rapporto tra lo speedup e il numero di processori utilizzati:

$E = \dfrac{\text{Speedup}}{P}$

Nel caso ideale, l'efficienza è pari a 1 (o al 100%), il che indica che ogni processore contribuisce pienamente alla riduzione del tempo di esecuzione. Un'efficienza inferiore a 1 indica che alcuni processori potrebbero essere sottoutilizzati, a causa dell'overhead di comunicazione, di un bilanciamento del carico non ottimale.

### Scalabilità

La **scalabilità** di un programma parallelo si riferisce alla sua capacità di mantenere un incremento proporzionale dello speedup all'aumentare del numero di unità di processamento. Un'applicazione è considerata scalabile se, aumentando il numero di processori, lo speedup cresce in modo proporzionato, mantenendo idealmente costante l'efficienza.

La scalabilità di un programma parallelo può essere classificata in due categorie principali:

- **Strong Scaling.** Misura quanto bene un'applicazione è in grado di ridurre il tempo di esecuzione mantenendo costante la dimensione totale del problema quando si aumenta il numero di unità di elaborazione
- **Weak Scaling.** Valuta l'abilità di un'applicazione di gestire un aumento proporzionale della dimensione del problema con l'aumentare del numero di unità di elaborazione, mantenendo costante la dimensione del problema per ogni processore

Le limitazioni nella scalabilità, sia nel contesto del strong che del weak scaling, sono spesso attribuibili ai **tempi di overhead** introdotto dalla parallelizzazione. Questi tempi indicono sullo speedup, che può essere ridefinito come:

$Speedup =\dfrac{Ts}{(Ts/P) + Toh}$

Dove:
- $Ts$ rappresenta il tempo di esecuzione in modalità sequenziale
- $P$ rappresenta il numero di processori utilizzati
- $Toh$ rappresenta il tempo di overhead dovuto alla parallelizzazione

I tipi principali di overhead includono:

- **Il tempo impiegato per le comunicazioni** ($Tcomm$) dato dalla somma dei tempi di trasmissione dei messaggi ($Tmess$). Questo tipo di overhead è particolarmente significativo nella programmazione che fa uso di memoria distribuita
- **Il tempo di inattività**, che diventa rilevante in programmi con carichi di lavoro non uniformemente distribuiti tra i processori
- **Il tempo necessario per avviare e terminare i task paralleli** (sia processi che thread), che assume importanza nella programmazione che sfrutta la memoria condivisa

### Legge di Amdahl 

La legge di Amdahl distingue in un programma seriale la porzione parallelizzabile da quella non parallelizzabile ( $T_\text{s}=T_\text{p}+T_\text{np}$ ), stabilendo un limite teorico allo speedup massimo ottenibile

$S_{\text{amdahl}} = \dfrac{T_{\text{seriale}}}{T_{\text{parallelo}}} = \dfrac{T_{\text{np}} + T_{\text{p}}}{T_{\text{np}} + \frac{T_{\text{p}}}{P}} = \dfrac{1}{Q_{\text{np}} + \frac{Q_{\text{p}}}{P}}$

Dove:

- $T_{\text{p}}$ rappresenta il tempo che può essere parallelizzato
- $T_{\text{np}}$ rappresenta il tempo che non può essere parallelizzato

- $Q_{\text{np}} = \dfrac{T_{\text{np}}}{T_{\text{np}} + T_{\text{p}}}$

- $Q_{\text{p}} = \dfrac{T_{\text{p}}}{T_{\text{np}} + T_{\text{p}}}$

Queste proporzioni soddisfano la condizione $Q_{\text{np}} + Q_{\text{p}} = 1$

L'effettivo speedup ottenibile, tenendo conto sia della legge di Amdahl che dell'overhead, è dato da:

$S_{\text{real}} = \dfrac{T_{\text{np}} + T_{\text{p}}}{T_{\text{np}} + \frac{T_{\text{p}}}{P} + T_{\text{oh}} }$

dove $T_{\text{oh}}$ rappresenta l'overhead aggiuntivo.

### Programma parallelo

Un **programma parallelo** è un tipo di software progettato per dividere un algoritmo in vari task, come processi o thread, distribuiti su molteplici unità di elaborazione. Questi task vengono coordinati tra loro per raggiungere un obiettivo computazionale comune. L'esecuzione di questo tipo di calcoli, che non seguono una sequenza lineare, necessita di:

- Un calcolatore non sequenziale, capace di eseguire diverse operazioni simultaneamente
- Un linguaggio di programmazione che permetta la descrizione di algoritmi non sequenziali (**parallelismo esplicito**)
- Un compilatore che possa automaticamente parallelizzare parti di un programma sequenziale (**parallelismo implicito**)

Esistono diversi approcci per trasformare un programma seriale in uno parallelo:

- **Parallelizzazione Automatica.** Il compilatore analizza il codice sorgente alla ricerca di sezioni che possono essere eseguite in parallelo. E.g. I cicli sono particolarmente adatti a questo tipo di parallelismo perché spesso gestiscono operazioni indipendenti che possono essere distribuite su più processori

- **Direttive per il Compilatore.** Il programmatore utilizza direttive specifiche per indicare al compilatore quali parti del codice devono essere eseguite in parallelo. Queste direttive, come quelle fornite da OpenMP, permettono di controllare più dettagliatamente la parallelizzazione, includendo la definizione di blocchi di codice e la gestione delle risorse. Le direttive sono trasparenti durante l'esecuzione su compilatori che non le supportano, poiché vengono ignorate.

- **Parallelismo Esplicito.** Questa tecnica richiede che il programmatore identifichi manualmente i task, gestisca la loro distribuzione sui processori e programmi le interazioni tra di loro. Un esempio noto di questo approccio è l'uso dell'MPI (Message Passing Interface), che è particolarmente efficace in ambienti di calcolo ad alte prestazioni (HPC) dove il controllo fine sulle operazioni di comunicazione e sincronizzazione è cruciale.

Ogni architettura (SIMD, MIMD con memoria condivisa o distribuita, GPU, ... ) presenta un modello di programmazione specifico.
#### Programmazione delle istruzioni SIMD

La programmazione SIMD (Single Instruction, Multiple Data) utilizza la vettorizzazione per eseguire la stessa operazione simultaneamente su tutti gli elementi di un vettore. Questo approccio è particolarmente efficace per aumentare le prestazioni delle operazioni sui dati in modo parallelo, sfruttando architetture hardware specifiche che supportano questo tipo di elaborazione. La programmazione SIMD può essere implementata in diversi modi:

- **Vettorizzazione Automatica da parte del Compilatore.** Il compilatore analizza il codice e, dove possibile, trasforma le operazioni su array e cicli in istruzioni vettoriali SIMD. Questo processo è trasparente per il programmatore, che non deve apportare modifiche esplicite al codice per beneficiare del parallelismo.

- **Vettorizzazione Guidata dal Programmatore.** Il programmatore può influenzare la vettorizzazione attraverso l'uso di direttive specifiche, come `#pragma`, comunemente usate in ambienti di programmazione come OpenMP. Queste direttive permettono di specificare quali loop o parti di codice dovrebbero essere vettorializzati, offrendo un maggiore controllo rispetto alla vettorizzazione automatica.

- **Vettorizzazione Esplicita tramite Intrinsics.** Gli intrinsics sono costrutti simili a funzioni che il programmatore può utilizzare per indicare esplicitamente l'uso di istruzioni SIMD specifiche. Questi costrutti sono riconosciuti dal compilatore e mappati direttamente in codice assembly. L'uso degli intrinsics permette un controllo dettagliato delle operazioni SIMD, rendendo possibile ottimizzare manualmente il codice per sfruttare al meglio le capacità dell'hardware.

#### Programmazione parallela MIMD

La programmazione parallela MIMD (Multiple Instruction, Multiple Data) offre la flessibilità di eseguire diverse istruzioni su diversi set di dati, facendo leva su due principali schemi di comunicazione tra i processori in un sistema parallelo:

- **Shared Memory (Memoria condivisa).** In questo paradigma, i processori comunicano accedendo a variabili memorizzate in una memoria condivisa. Tutti i processori hanno accesso alla stessa area di memoria e possono leggere o scrivere le variabili globali. Questo schema è tipico dei sistemi a multiprocessore dove la gestione efficiente della memoria condivisa è cruciale per evitare conflitti e garantire la coerenza dei dati. Il principale vantaggio di questo approccio è la facilità con cui i processi possono condividere informazioni, ma richiede una sincronizzazione accurata per prevenire condizioni di gara e altri problemi di accesso concorrente.

- **Message Passing (Passaggio di messaggi).** Nel paradigma del message passing, ogni processore opera su una propria memoria locale e la comunicazione avviene attraverso lo scambio di messaggi tra i processori. Questo approccio è fondamentale in sistemi distribuiti o reti di computer dove non esiste una memoria condivisa. Ogni processo gestisce le sue informazioni locali e comunica con altri processi inviando e ricevendo messaggi, che possono contenere dati o segnali di controllo. Il message passing è spesso implementato attraverso librerie come MPI (Message Passing Interface), che forniscono funzioni ricche e flessibili per gestire la comunicazione tra processi.

##### Memoria condivisa

Nel paradigma shared memory (memoria condivisa) i task accedono a variabili e strutture dati comuni. Questo approccio richiede l'uso di strumenti per sincronizzare le operazioni al fine di evitare conflitti e garantire la coerenza dei dati.

Per la gestione dei processi, la libreria **SysV-IPC** permette di creare sezioni di memoria condivisa utilizzando funzioni come `shmget()` e `shmctl()`, e di sincronizzare i processi tramite semafori con funzioni come `semget()` e `semctl()`. Per i thread, invece, la libreria Posix thread (**Pthreads**) facilita la comunicazione a memoria condivisa e utilizza semafori per la sincronizzazione, con funzioni come `pthread_mutex_*()`. **OpenMP**, invece, permette ai programmatori di definire sezioni di codice da eseguire parallelamente attraverso direttive specifiche che gestiscono automaticamente la creazione e sincronizzazione dei thread prima dell'esecuzione del codice.

**Fork/Join**

Un modello comunemente usato è il **Fork/Join**, in cui un task **master** genera dinamicamente uno o più nuovi task (**fork**). Questi task eseguono flussi di controllo in parallelo al master, fino al punto di sincronizzazione (**join**). 

Esistono diverse modalità di join:

- **Join All**: tutti i task devono raggiungere il punto di join prima che il master possa proseguire, mentre gli altri task terminano
- **Join Any**: il master procede non appena il primo task raggiunge il join, mentre gli altri completano dopo aver raggiunto anch'essi il join
- **Join None**: il master attiva la fork e continua l'esecuzione senza attendere altri task

L'uso intensivo di strutture fork/join può tuttavia introdurre ritardi dovuti all'avvio e alla terminazione dei thread, specialmente in ambienti con molti thread.

OpenMP utilizza principalmente il modello Join All per gestire i suoi task.

##### Memoria distribuita

Nel paradigma della memoria distribuita, i processi comunicano attraverso lo scambio di messaggi, un metodo che consente loro di operare su dati dislocati su differenti nodi di calcolo. La libreria MPI (Message Passing Interface) rappresenta lo standard de-facto per l'implementazione di questo tipo di comunicazione. MPI offre una vasta gamma di primitive che facilitano le comunicazioni sia punto-punto sia collettive.

**Master-Slave**

Un modello comune di utilizzo di MPI è il **Master-Slave**, dove un task master coordina e controlla l'elaborazione degli altri task, detti slaves. Questo approccio è particolarmente utile per implementare strategie di load balancing, dove il carico di lavoro viene distribuito in modo ottimale tra i vari nodi per evitare collo di bottiglia e sfruttare al massimo le risorse disponibili.

Il modello Master-Slave può essere implementato efficacemente utilizzando l'approccio SPMD (Single Program, Multiple Data). In SPMD, ogni processo esegue lo stesso programma ma su differenti porzioni di dati, permettendo una gestione del lavoro decentralizzata e scalabile, ideale per applicazioni su larga scala che richiedono una grande quantità di elaborazione distribuita.

#### Programmazione GPU con CUDA

NVIDIA ha sviluppato diversi modelli di unità di elaborazione grafica (GPU) che trovano impiego come acceleratori di calcolo nelle applicazioni che sfruttano la parallelizzazione dei dati. La compagnia ha anche creato CUDA, un modello di programmazione dedicato, accompagnato da una libreria e un compilatore specifico (nvcc).

In questo contesto, il codice che non è idoneo alla parallelizzazione o che è intrinsecamente seriale viene ancora eseguito sulla CPU. Al contrario, il codice che può beneficiare di una forte parallelizzazione, di tipo **data parallel**, viene scritto utilizzando il modello CUDA. Questo codice viene organizzato in una struttura detta **kernel**, che è progettata per essere eseguita sulla GPU. In aggiunta al codice, anche i dati necessari per l'elaborazione vengono trasferiti alla GPU.

Una volta che la GPU ha completato l'elaborazione del codice nel kernel, i risultati vengono trasferiti indietro alla CPU.


#### Sistemi ibridi

La programmazione di architetture ibride coinvolge una combinazione strategica di diversi modelli di programmazione parallela per massimizzare l'efficienza e le prestazioni su hardware composito. Questi sistemi ibridi spesso includono l'uso congiunto del modello message passing con il modello basato su thread. Questo approccio permette di sfruttare sia la comunicazione tra processi su differenti nodi di calcolo (MPI) sia la parallelizzazione all'interno di un singolo nodo usando i thread (OpenMP).

Quando un sistema ibrido è anche dotato di una o più GPU, si introduce la programmazione CUDA per gestire specificatamente questi acceleratori di calcolo.

