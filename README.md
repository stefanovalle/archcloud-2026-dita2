# Flotta — i laboratori del corso Architetture Cloud

Repository che accompagna i laboratori del corso **Architetture Cloud** (ITS 2026-2027). Il tema è lo stesso del corso Protocolli IoT: la flotta di auto in car sharing. Qui però non scriviamo un'applicazione: accendiamo e colleghiamo i pezzi su cui un'applicazione si appoggia, a partire da un database, **CouchDB**, che gira in container Docker.

## Cosa serve

- **Docker Desktop**, acceso. Prima della giornata 1 scarichiamo l'immagine una volta sola: `docker pull couchdb:3`.
- **Git Bash**, come nel corso Protocolli: i comandi Docker si danno da lì.
- **Postman** (si può usare senza account): tutte le richieste a CouchDB si fanno da lì.

## Come si parte

```
git clone https://github.com/stefanovalle/archcloud-2026-dita2.git
cd archcloud-2026-dita2/giornata1
docker compose up -d
docker compose ps
```

Nel browser, **http://localhost:5984/_utils** è Fauxton, la pagina web di CouchDB. Utente `admin`, password `password`: vanno bene solo in laboratorio.

## I branch: un passo per ciascuno

Come nel corso Protocolli, ogni branch è un passo del corso e si parte da `main`.

| Branch | Cosa contiene |
|---|---|
| `main` | **Giornata 1, Lab 1 e Lab 2.** `giornata1/compose.yaml`: due nodi CouchDB, A e B, dalla stessa immagine. A risponde su `localhost:5984`; B non ha porte pubblicate finché nel Lab 2 non le apriamo noi. |
| `lab3` | **Giornata 1, dal Lab 3.** Parte da `main` e aggiunge `postman/flotta-couchdb.postman_collection.json`: la collection Postman con le richieste di tutti i laboratori, una cartella per laboratorio. |
| `lab6` | **Lezione 3, Lab 6 e 7 su AWS.** Parte da `lab3` e aggiunge la cartella `aws/`: lo script di avvio delle istanze, il codice della funzione Lambda, la regola di IoT Core e i messaggi di prova. |
| `lezione4` | **Lezione 4, passo 4.** Parte da `lab6` e aggiunge `cluster/compose.yaml`: tre nodi CouchDB sulle porte 5991, 5992 e 5993, che si riconoscono come parti dello stesso cluster. |
| `lezione5` | **Lezione 5, Lab 8 su AWS.** Parte da `lezione4` e aggiunge `aws/fine-noleggio.json`: l’evento «fine noleggio» da pubblicare sul topic SNS. |

I passi successivi arriveranno come nuovi branch.

## La collection Postman (dal Lab 3)

```
git pull
git switch lab3
```

In Postman serve un **account gratuito** (Sign up, basta un indirizzo email): senza account Postman lavora in modalità leggera, che manda le richieste ma non gestisce le collection. Poi:

1. **Import**, in alto a sinistra;
2. trasciniamo il file `postman/flotta-couchdb.postman_collection.json`, oppure incolliamo il link
   `https://raw.githubusercontent.com/stefanovalle/archcloud-2026-dita2/lab3/postman/flotta-couchdb.postman_collection.json`.

Compare la collection «Flotta - Laboratorio CouchDB». Autenticazione (Basic Auth, `admin`/`password`) e indirizzi dei nodi sono già impostati sulla collection: `{{A}}` vale `http://localhost:5984`, `{{B}}` vale `http://localhost:5985`. Dove troviamo `INCOLLA_LA_REV` va la `_rev` vera, copiata dalla risposta precedente.

## Lab 2: aprire la porta di B

In `giornata1/compose.yaml`, sotto `couch-b`, togliamo il cancelletto dalle due righe

```
    # ports:
    #   - "5985:5984"
```

salviamo e rilanciamo `docker compose up -d`. Ora **http://localhost:5985/_utils** si apre.

È una modifica nostra al file: git la vede (`git status`). Quando passiamo a `lab3` viene con noi, perché lì `compose.yaml` è identico. Se un giorno git si lamenta cambiando branch, la mettiamo da parte con `git stash`.

## I dati

I documenti stanno in due volumi Docker, `dati-a` e `dati-b`: `docker compose down` spegne e cancella i container, ma i dati restano. Alla fine della giornata **non cancelliamo nulla**: la lezione 3 riparte da A e B come sono.

Solo alla fine del corso, per ripulire tutto: `docker compose down -v` (il `-v` cancella anche i volumi).

## I laboratori su AWS (lezione 3)

```
git pull
git switch lab6
```

Nella cartella `aws/` ci sono i file da copiare nella console di AWS, invece di ridigitarli dalle slide:

| File | Dove si usa |
|---|---|
| `user-data.sh` | Lab 6: EC2 → Launch instances → Advanced details → User data |
| `lambda_function.py` | Lab 7: il codice della funzione Lambda (cambiamo `TABELLA` con il nostro cognome) |
| `evento-test.json` | Lab 7: l’evento di prova della funzione (Test → Create new event) |
| `regola.sql` | Lab 7: la query della regola di IoT Core (cambiamo `rossi` con il nostro cognome) |
| `messaggio.json` | Lab 7: il messaggio da pubblicare dal client MQTT di prova |

Ogni risorsa che creiamo su AWS comincia con il nostro cognome, e alla fine della lezione si cancella tutto, nell’ordine indicato sulle slide.

## Il cluster (lezione 4, passo 4)

```
git pull
git switch lezione4
cd cluster
docker compose up -d
```

Tre nodi nuovi, `couch-1`, `couch-2` e `couch-3`, sulle porte 5991, 5992 e 5993 (in Postman `{{C1}}` e `{{C3}}`). Possono restare accesi insieme ad A e B della cartella `giornata1`: usano porte diverse. Le richieste sono nella collection, cartella «Lezione 4 / Passo 4 · Cluster».

Per spegnere un nodo e riaccenderlo: `docker compose stop couch-3` e `docker compose start couch-3`.

## L’evento «fine noleggio» (lezione 5, Lab 8)

```
git pull
git switch lezione5
```

Il Lab 8 si fa tutto dalla console di AWS, senza codice: un topic SNS `rossi-fine-noleggio` e due code SQS iscritte, `rossi-fatturazione` e `rossi-manutenzione`, più la coda degli errori `rossi-manutenzione-errori` (al posto di `rossi`, il nostro cognome). Il messaggio da pubblicare (SNS → il nostro topic → Publish message) è in `aws/fine-noleggio.json`.
