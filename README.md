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

I passi successivi arriveranno come nuovi branch.

## Lab 2: aprire la porta di B

In `giornata1/compose.yaml`, sotto `couch-b`, togliamo il cancelletto dalle due righe

```
    # ports:
    #   - "5985:5984"
```

salviamo e rilanciamo `docker compose up -d`. Ora **http://localhost:5985/_utils** si apre.

È una modifica nostra al file: git la vede (`git status`). Se poi vogliamo cambiare branch e git si lamenta, la mettiamo da parte con `git stash`.

## I dati

I documenti stanno in due volumi Docker, `dati-a` e `dati-b`: `docker compose down` spegne e cancella i container, ma i dati restano. Alla fine della giornata **non cancelliamo nulla**: la lezione 3 riparte da A e B come sono.

Solo alla fine del corso, per ripulire tutto: `docker compose down -v` (il `-v` cancella anche i volumi).
