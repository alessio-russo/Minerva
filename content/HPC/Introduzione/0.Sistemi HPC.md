# Sistemi per il calcolo ad alte prestazioni


## Tassonomia di FLYNN

Esistono diversi criteri per categorizzare i sistemi dedicati al calcolo ad alte prestazioni. Una delle metodologie di classificazione più riconosciute ed efficaci è stata proposta da Flynn. Questa tassonomia prende in considerazione due aspetti fondamentali: il **flusso delle istruzioni** e il **flusso dei dati**. Entrambi questi flussi possono essere caratterizzati come **singoli** o **multipli**.

#### SISD

Nel modello **SISD** (Single Instruction Stream, Single Data Stream), troviamo una configurazione in cui una singola CPU esegue un flusso di istruzioni sequenziale, operando su un unico flusso di dati alla volta. Questo approccio corrisponde ai sistemi di calcolo serialo, che seguono la tradizionale architettura di Von Neumann.
#### SIMD

Il modello **SIMD** (Single Instruction, Multiple Data) rappresenta un'architettura di calcolo parallelo in cui la stessa istruzione viene eseguita su più flussi di dati simultaneamente. Questa configurazione permette l'elaborazione parallela di dati attraverso l'utilizzo di più unità di elaborazione che operano in sincrono sotto la guida di un'istruzione comune, massimizzando l'efficienza per operazioni che possono essere eseguite in parallelo su set di dati.

Principali tipologie di sistemi SIMD:

- **Processori Vettoriali**: Questi sistemi sono caratterizzati da un array di unità di elaborazione (Processing Units, PU) che condividono una singola unità di controllo. Le istruzioni vengono distribuite in parallelo a tutte le PU, permettendo l'esecuzione simultanea su diversi dati. Ogni PU dispone di propria memoria, il che richiede una rete di comunicazione dedicata per lo scambio di dati.

- **Istruzioni Vettoriali**: In questa configurazione, il parallelismo viene realizzato internamente al processore attraverso istruzioni che possono operare contemporaneamente su più dati. La memoria in questo caso è condivisa tra le diverse unità funzionali, rendendo la banda di memoria disponibile un fattore critico per le prestazioni.

I sistemi SIMD sono particolarmente efficaci per applicazioni che richiedono l'elaborazione di grandi quantità di dati con operazioni ripetitive, come il processing di immagini, operazioni su matrici, e in generale, compiti che possono beneficiare di un'elaborazione parallela massiva.

#### MISD

Il modello **MISD** (Multiple Instruction, Single Data) è il meno comune e il più difficile da trovare in applicazioni pratiche rispetto agli altri modelli. 

In un sistema MISD, diverse unità di elaborazione eseguono diverse istruzioni su lo stesso dato in parallelo. Teoricamente, questo approccio potrebbe essere utile per operazioni di elaborazione che richiedono multipli livelli di trasformazione o analisi del medesimo dato in sequenza, come certi tipi di elaborazioni di segnali o algoritmi di crittografia.

#### MIMD

I sistemi **MIMD** (Multiple Instruction, Multiple Data) rappresentano un'architettura di calcolo parallelo estremamente versatile e potente, in cui ogni processore opera indipendentemente, eseguendo flussi di istruzioni diversi su flussi di dati distinti. Questo modello consente una flessibilità notevole, poiché ogni unità di elaborazione può affrontare compiti differenti contemporaneamente, rendendo i sistemi MIMD particolarmente adatti a gestire una vasta gamma di applicazioni parallele e distribuite. 

Molte architetture MIMD possono includere, come casi particolari, elementi di elaborazione SIMD, combinando i vantaggi del parallelismo a livello di dati con la flessibilità del parallelismo a livello di istruzioni.

##### Limiti della tassonomia di Flynn

La tassonomia ha fornito uno schema di classificazione influente per i sistemi di calcolo parallelo basato sulla distinzione tra flussi di istruzioni e flussi di dati. Nonostante il suo ampio utilizzo e il suo valore concettuale nel distinguere tra diversi modelli di elaborazione parallela, presenta alcune limitazioni nella descrizione delle architetture di calcolo moderne. Una delle principali criticità è l'incapacità di esprimere differenze significative tra architetture a memoria distribuita e architetture a memoria condivisa.

## Sistemi a memoria condivisa

I sistemi a memoria condivisa rappresentano una classe importante di architetture di calcolo parallelo, in cui tutti i processori hanno accesso a un unico spazio di indirizzamento della memoria. Questo significa che qualsiasi modifica alla memoria effettuata da una CPU è immediatamente visibile a tutte le altre CPU nel sistema. All'interno di questa categoria, si distinguono due sottocategorie principali: **Uniform Memory Access** (UMA) e **Non-Uniform Memory Access** (NUMA)

##### UMA (Uniform Memory Access)

Il modello UMA, in maniera analoga ai sistemi SMP, è caratterizzato dal fatto che tutti i processori hanno lo stesso tempo di latenza per accedere a qualsiasi parte della memoria condivisa.

Tuttavia, la scalabilità può essere un problema, poiché l'aumento del numero di processori può portare a congestione nell'accesso alla memoria condivisa. Inoltre, poiché ogni processore deve avere accesso a tutta la memoria con lo stesso tempo di latenza, diventa più difficile mantenere questa proprietà man mano che il sistema cresce di dimensioni.

##### NUMA  (Non-Uniform Memory Access)

I sistemi a memoria condivisa NUMA (Non-Uniform Memory Access) rappresentano un'evoluzione dell'architettura UMA per affrontare alcune delle sue limitazioni, in particolare riguardo alla scalabilità e alla performance in sistemi con un numero elevato di processori. 

In un sistema NUMA, ogni processore possiede una propria memoria locale. Tuttavia, l'insieme di queste memorie locali costituisce uno spazio di indirizzi globale, rendendo possibile per ogni processore accedere alla memoria di qualsiasi altro processore.

Di conseguenza, la caratteristica distintiva di NUMA è che il **tempo di accesso** alla memoria **varia** in base alla locazione dei dati: l'accesso è più veloce se il processore accede alla propria memoria locale, mentre l'accesso alla memoria di processori remoti introduce un ritardo (delay), dovuto alla rete interna di interconnessione.

L'architettura NUMA migliora la scalabilità dei sistemi multiprocessore, consentendo a più processori di lavorare in parallelo senza intasare un bus di memoria condiviso. Tuttavia, la programmazione su sistemi NUMA può essere più complessa, poiché occorre considerare la posizione dei dati per ottimizzare le prestazioni.

## Sistemi a memoria distribuita

Nei sistemi a memoria distribuita, ogni CPU (o **nodo di calcolo**) dispone di una propria memoria locale, che non è direttamente accessibile dagli altri processori attraverso uno spazio di indirizzamento comune. La comunicazione tra i nodi avviene esclusivamente tramite lo scambio di messaggi, utilizzando infrastrutture di rete che possono variare dalla comune Ethernet a soluzioni più avanzate come Intel OmniPath Architecture (OPA) e Infiniband, progettate per ridurre la latenza e aumentare la larghezza di banda.

##### Vantaggi dei sistemi a memoria distribuita

- **Scalabilità**: Il numero di processori e la quantità totale di memoria possono essere incrementati semplicemente aggiungendo più nodi al sistema.

- **Costi Contenuti**: Utilizzando hardware standard (commodity), i sistemi a memoria distribuita possono offrire un'eccellente rapporto costo-efficienza, rendendoli accessibili anche per progetti con budget limitati.

##### Svantaggi dei sistemi a memoria distribuita

- **Gestione della Comunicazione**: A differenza dei sistemi a memoria condivisa, in un ambiente a memoria distribuita, il programmatore deve gestire esplicitamente i dettagli della comunicazione tra i nodi, compreso lo scambio di messaggi, la sincronizzazione e la coerenza dei dati. 

- **Latenza nella Comunicazione**: Il tempo necessario per accedere alla memoria remota e per la comunicazione tra i nodi dipende significativamente dall'infrastruttura di rete utilizzata. Anche con tecnologie ad alta velocità come OPA e Infiniband, la latenza può essere significativa, soprattutto quando si accede a nodi lontani nella rete, influenzando le prestazioni complessive del sistema.

## Sistemi ibridi

I sistemi ibridi combinano le caratteristiche dei sistemi a memoria condivisa (sia UMA che NUMA) e dei sistemi a memoria distribuita per creare architetture potenti e flessibili. Questi sistemi sono composti da più nodi a memoria condivisa, ciascuno dei quali può funzionare come un'entità autonoma con i propri processori e memoria condivisa, interconnessi tramite una rete ad alta velocità. L'integrazione di acceleratori, come le GPU (Graphics Processing Units), aggiunge ulteriore potenza computazionale, rendendo questi sistemi particolarmente adatti per applicazioni di elaborazione dati e computazionali ad alta intensità. 