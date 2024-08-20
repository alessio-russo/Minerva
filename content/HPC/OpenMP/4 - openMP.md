
# OpenMP

OpenMP, acronimo di Open specifications for Multi Processing, è un modello di programmazione parallela che utilizza la memoria condivisa per facilitare la scrittura di applicazioni multithread. OpenMP mira a semplificare la programmazione parallela aggiungendo costrutti specifici per il multithreading nei linguaggi C, C++ e Fortran.

Uno dei principali vantaggi di OpenMP è la sua capacità di gestire codice che può essere eseguito sia in modalità seriale sia parallela. Questo significa che lo stesso codice può essere utilizzato su sistemi con e senza supporto OpenMP, offrendo una flessibilità significativa agli sviluppatori

## Modello di esecuzione 

L'esecuzione inizia con un singolo thread, conosciuto come il thread master. Quando è necessario il parallelismo, OpenMP utilizza il modello fork/join per gestire l'attivazione e la disattivazione delle regioni parallele.

Questo modello si attiva mediante specifiche direttive che delimitano l'inizio della regione parallela. All'interno di questa regione, più thread vengono creati per eseguire il codice in parallelo. Questi thread operano concorrentemente fino al completamento dei loro compiti. Al termine dell'esecuzione parallela, si verifica un evento di join, dove tutti i thread creati completano il loro compito e si riuniscono al thread master. Questo comportamento è gestito dal costrutto `#pragma omp parallel`

```cpp
//master thread

#pragma omp parallel
{
	// parallel region
}
```


## Funzioni

L'uso delle funzioni di OpenMP fornisce ai programmatori strumenti per gestire con precisione i thread e il parallelismo nelle loro applicazioni. Tuttavia, è importante notare che l'integrazione di queste funzioni rende il codice dipendente da OpenMP. Ecco una panoramica delle principali funzioni offerte da OpenMP e come vengono utilizzate per controllare l'esecuzione parallela:

1. **`omp_set_num_threads()`** - Questa funzione permette di impostare il numero di thread da utilizzare nelle future aree parallele, a meno che non sia sovrascritto dalla clausola `num_threads` nelle direttive di parallelizzazione. Questo consente ai programmatori di modificare la concorrenza in base alle necessità specifiche del carico di lavoro.

2. **`omp_get_num_threads()`** - Restituisce il numero di thread attualmente attivi nell'area parallela. Questo può essere utile per ottenere informazioni dinamiche sul numero di thread durante l'esecuzione del programma.

3. **`omp_get_max_threads()`** - Fornisce il numero massimo di thread che sarebbero disponibili per l'esecuzione se un'area parallela venisse definita in quel punto del codice senza una specifica clausola `num_threads`. È utile per valutare la capacità massima di parallelismo del sistema.

4. **`omp_get_thread_num()`** - Restituisce l'identificativo del thread corrente all'interno del team di thread. Questa funzione è spesso usata per distribuire il lavoro tra i thread in modo che ciascuno esegua un compito specifico basato sul suo identificativo.

5. **`omp_get_wtime()`** - Offre un modo per misurare il tempo trascorso, fornendo il valore in secondi da un certo punto, simile a un cronometro. È utile per benchmarking e per misurare le prestazioni di sezioni specifiche del codice.

6. **`omp_set_lock()`** e **`omp_unset_lock()`** - Queste funzioni gestiscono i meccanismi di blocco, permettendo di sincronizzare l'accesso a risorse condivise. `omp_set_lock()` blocca l'esecuzione del thread finché non si libera un blocco, mentre `omp_unset_lock()` rilascia un blocco precedentemente impostato.

7. **`omp_test_lock()`** - Prova a impostare un blocco senza bloccare l'esecuzione del thread. Questa funzione può essere usata per verificare se una risorsa è disponibile senza causare un arresto del thread chiamante.

**Impostare il numero di Thread**

Per gestire il numero di thread in un'applicazione che utilizza OpenMP esistono diverse tecniche

**Variabile d'ambiente OMP_NUM_THREADS**: Questa variabile d'ambiente può essere impostata per definire il numero di thread utilizzati da OpenMP se non vi sono indicazioni contrarie all'interno del codice. La variabile viene letta all'avvio dell'applicazione.

```
OMP_NUM_THREADS=4 ./a.out
```

In questo caso, l'applicazione verrà eseguita utilizzando quattro thread, a meno che non vi siano altre specifiche nel codice.

**Funzione omp_set_num_threads()**: Questa funzione può essere utilizzata all'interno del programma per specificare il numero di thread. L'impostazione avrà effetto solo per le regioni parallele che vengono eseguite dopo la chiamata della funzione

```cpp
omp_set_num_threads(4);
```

**Clausola num_threads nelle direttive omp parallel**: Questo metodo consente di specificare il numero di thread direttamente nella direttiva che definisce una regione parallela, sovrascrivendo qualsiasi altra impostazione.

```cpp
#pragma omp parallel num_threads(8)
{
   // codice da eseguire in parallelo
}
```


**Identificazione dei Thread**

All'interno di un pool di thread, ogni thread è identificato da un numero intero che va da 0 a $N-1$, dove $N$ è il numero totale di thread nel pool. Il thread master ha sempre identificatore 0.

**Funzione omp_get_thread_num()**: Questa funzione restituisce l'identificatore del thread corrente. Se chiamata al di fuori di una regione parallela, restituisce sempre 0, indicando che il codice è eseguito dal thread master.

```cpp
int t = omp_get_thread_num();
```

Utilizzando questa funzione, ogni thread può determinare il proprio identificatore, utile per distribuire il lavoro o per debug.

## Variabili

In OpenMP, le variabili possono essere classificate in due categorie principali: **shared** e **private**. 

**Variabili Shared**

Le **variabili shared** sono accessibili da tutti i thread all'interno di una regione parallela. Queste variabili sono dichiarate esternamente alla regione parallela e, per default, sono visibili e modificabili da ogni thread nel pool.

Ogni thread può leggere e modificare le variabili shared (questo può portare a race condition se più thread cercano di accedere contemporaneamente alla stessa variabile)

La variabili dichiarate esternamente alla regione parallela sono per default shared. 

```cpp
// OpenMP header
#include <omp.h>
#include <string>
#include <iostream>
using namespace std;

int main()
{
	int shared_var = 10;
	
	#pragma omp parallel num_threads(8)
	{

		string message = "Thread " + to_string(omp_get_thread_num()) + ": " 
		+ to_string(shared_var) + "\n";
	
		cout << message;
	}
	
}
```

**Output**

```
Thread 3: 10
Thread 0: 10
Thread 2: 10
Thread 1: 10
Thread 7: 10
Thread 5: 10
Thread 4: 10
Thread 6: 10
```

**Variabili Private**

Le **variabili private** sono locali a ogni thread. Questo significa che ogni thread ha la sua copia indipendente della variabile, che è localizzata nello stack del thread. Quando una variabile viene dichiarata come private, essa non viene inizializzata e contiene un valore indeterminato all'inizio della regione parallela.

Le variabili dichiarate direttamente all'interno di una regione parallela sono automaticamente private per ciascun thread.

```cpp
#pragma omp parallel
{
  int private_var;  // Ogni thread ha la sua copia di private_var
}
```

**Modifica dello scope delle variabili**

OpenMP offre clausole specifiche per modificare esplicitamente il comportamento predefinito delle variabili all'interno delle regioni parallele, come `shared` e `private`.

```cpp
int shared1, shared2;
#pragma omp parallel private(shared2) shared(shared1)
{
	int private1, private2;  // private1 e private2 sono private per default
    // shared2 è private qui, nonostante sia dichiarata fuori come shared
    // shared1 è condivisa tra tutti i thread
}
```

## Direttive e clausole

Le direttive in OpenMP sono cruciali per gestire il comportamento delle regioni parallele nel codice. Queste direttive possono essere modificate attraverso l'uso di clausole specifiche

Come già introdotto, la direttiva `parallel` è utilizzata per definire una regione di codice che deve essere eseguita in parallelo dai thread. È la base per la maggior parte delle programmazioni parallele in OpenMP.

#### Clausole

Clausole comuni della direttiva `parallel` sono `shared()`, `private()`, `num_threads()` e 
`reduction()` 

**Clausola `reduction()`**

La clausola `reduction()` automatizza il processo di combinazione dei risultati di ogni thread in una singola variabile risultante. Questo è particolarmente utile per operazioni come la somma, la moltiplicazione, o il calcolo del massimo o del minimo.

```cpp
int t;
#pragma omp parallel reduction(+:t)
{
    t = omp_get_thread_num();  // Ogni thread assegna il proprio numero identificativo a t
}
// All'uscita della regione parallela, t contiene la somma dei numeri di tutti i thread
```

In questo esempio, `reduction(+:t)` indica che la variabile `t` dovrebbe essere sommata attraverso tutti i thread. Alla fine della regione parallela, `t` conterrà la somma dei valori di `t` di ogni thread, ovvero la somma dei loro numeri identificativi.

#### Direttive

OpenMP offre diverse direttive che permettono ai programmatori di controllare il flusso di esecuzione parallela e la divisione del lavoro tra i thread. Queste direttive possono essere annidate, con la direttiva `parallel` che funge spesso da contenitore per altre direttive, gestendo l'inizializzazione e la terminazione dell'ambiente parallelo. Ogni direttiva ha uno scopo specifico e può essere utilizzata per ottimizzare e controllare l'esecuzione del codice parallelo.

**Direttiva `for`**

Utilizzata per parallelizzare i cicli `for`, dividendo automaticamente le iterazioni del ciclo tra i thread disponibili. Questa direttiva implementa la **decomposizione di dominio**: tutti i thread svolgono le stesse operazioni su dati differenti.

Le direttive `parallel` e `for` possono essere combinate in un'unica direttiva `parallel for`

``` cpp
#pragma omp parallel for
for(int i = 0; i < n; i++) 
{
	// Il lavoro qui viene diviso tra i thread	
}
```
 
**Clausola `schedule`**

La clausola `schedule` è particolarmente importante perché definisce come le iterazioni del ciclo `for` vengono distribuite tra i thread. Ci sono diverse opzioni per la schedulazione:

- **Static**: Il carico di lavoro viene diviso in parti uguali (chunks) e distribuito ai thread all'inizio dell'esecuzione. Questo metodo è efficace quando tutte le iterazioni richiedono un tempo simile per essere completate.

- **Dynamic**: I chunk di lavoro vengono assegnati ai thread man mano che questi diventano disponibili. È utile quando le iterazioni possono avere durate molto diverse, permettendo un migliore bilanciamento del carico.

```cpp
#pragma omp parallel for schedule(dynamic, 5)
for (int i = 0; i < n; i++) 
{
// Il codice qui permette che ogni thread prenda 5 iterazioni per volta, assegnate dinamicamente
}
```

Per default, lo scheduling è `static`, con il numero di iterazioni per chunk calcolato come il numero totale di iterazioni diviso il numero di thread. Questo assicura che ogni thread abbia più o meno la stessa quantità di lavoro.

**Direttiva `section`**

Serve per dividere manualmente il codice in diverse sezioni, che verranno eseguite in parallelo da diversi thread. Questo approccio è noto come **decomposizione funzionale**, poiché differenti blocchi di codice (o funzioni) possono essere assegnati a diversi thread per l'esecuzione parallela

```cpp
// OpenMP header
#include <omp.h>
#include <iostream>
#include <string>
using namespace std;

int main()
{
	#pragma omp parallel sections num_threads(8)
    {

        #pragma omp section
        {
                string message = "Section 1 executed by thread " + to_string(omp_get_thread_num()) + "\n";
                cout << message;
        }

        #pragma omp section
        {
                string message = "Section 2 executed by thread " + to_string(omp_get_thread_num()) + "\n";
                cout << message;
        }
    }
}
```

**Output**

```
Section 1 executed by thread 6
Section 2 executed by thread 4
```

**Direttiva `single`**

Consente di eseguire un blocco di codice su un solo thread, che non è necessariamente il thread master.  Questa direttiva ha una **barriera implicita** all’uscita: i thread che non entrano attendono comunque all’uscita

```cpp
#pragma omp parallel
{
	#pragma omp single
	{
		// Questo codice è eseguito da un solo thread
	}
}
```

**Direttiva `master`**

Assicura che solo il thread master esegua il blocco di codice specificato

```cpp
#pragma omp parallel
{
	#pragma omp master
	{
		// Solo il thread master esegue questo blocco
	}
}
```

**Direttiva `critical`**

Specifica che il blocco di codice all'interno deve essere eseguito da un solo thread alla volta, creando una sezione critica.

```cpp
#pragma omp parallel
{
	#pragma omp critical
	{
		// Solo un thread alla volta esegue questo blocco
	}
}
```

**Direttiva `atomic`**

La direttiva `atomic` è utilizzata per specificare che un'operazione su una variabile, come un incremento, deve essere eseguita atomicamente (ovvero senza interruzioni). Ciò è particolarmente utile per prevenire race condition durante l'aggiornamento di una variabile condivisa tra più thread. 

```c
int count = 0; 
#pragma omp parallel 
{ 
    #pragma omp atomic 
    count++; 
}
```

Questo approccio assicura che l'incremento del contatore sia sicuro e privo di conflitti tra i thread

**Direttiva `barrier`**

Una barriera che sincronizza tutti i thread; tutti i thread si fermano a questo punto e possono proseguire solo quando tutti hanno raggiunto la barriera

```cpp
#pragma omp parallel
{
	// Codice eseguito da tutti i thread
	#pragma omp barrier
	// Altri codici che saranno eseguiti dopo che tutti i thread hanno raggiunto la barriera
}
```

Queste direttive offrono un controllo fine e flessibile sul comportamento parallelo, consentendo ai programmatori di ottimizzare le prestazioni e gestire correttamente la concorrenza e la sincronizzazione nelle loro applicazioni

## Thread affinity

La gestione dell'affinità dei thread è un aspetto cruciale nell'ottimizzazione delle prestazioni dei programmi multithread, specialmente quando si opera su sistemi multicore. Un thread in esecuzione su un determinato core può essere spostato in run-time su un core diverso dal sistema operativo, invalidando potenzialmente i dati memorizzati nella cache. Per mitigare questo problema, si utilizza la CPU affinity, che consente di legare un processo o un thread a un core fisico specifico.

A partire dalla versione 4, OpenMP supporta la gestione dell'affinità dei thread attraverso due variabili di ambiente, `OMP_PLACES` e `OMP_PROC_BIND`, che permettono di definire e controllare come i thread vengano associati ai core fisici. La variabile `OMP_PLACES` definisce i livelli di affinità, consentendo di specificare se i thread possono spostarsi all'interno di un socket, di un core, o essere legati a uno specifico hyper-thread. Queste opzioni sono rispettivamente indicate come `socket`, `core`, e `thread`.

La variabile `OMP_PROC_BIND` consente di impostare il modello di affinità, offrendo le opzioni:

- `false` per disabilitare l'affinità
- `true` per abilitarla
- `close` per posizionare i thread tra core vicini, seguendo la numerazione progressiva dei core
- `spread` per distribuire i thread tra core più distanti

Ad esempio, per eseguire un programma con i thread che possono muoversi liberamente all'interno di un socket, ma con una strategia di posizionamento vicino tra core vicini, si configurerebbe così

```bash
OMP_PLACES=socket OMP_PROC_BIND=close ./a.out
```

Per verificare le impostazioni correnti dell'affinità di un programma, si può utilizzare la funzione `omp_get_proc_bind()`, che restituisce lo stato dell'affinità del thread corrente