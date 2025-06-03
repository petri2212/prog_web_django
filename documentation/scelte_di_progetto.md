# Documentation

- Abbiamo scelto di usare come Database PostgreSQL in quanto per ristrutturare il progetto iniziale ci serviva un database relazionale.
- Principalmente abbiamo usato un ambiente virtuale `.venv/Scripts/activate ` dove abbiamo installato django.
- Abbiamo scelto di usare un approccio modulare, percio abbiamo creato una applicazione museo dove abbiamo i vari *templates* e i file *statici*, in futuro si può ampliare il progetto creando altre app e farle comunicare tra loro o indipendentemente.
- Negli urls.py abbiamo tutti gli url della nostra applicazione museo, questi vengono inclusi nella cartella padre `src/urls`
- In views.py sviluppiamo alcune API che ci servono per fare le varie query a PostgreSQL, queste vengono gestite tramite i file fetch------.js che abbiamo modificato per poter essere compatibili con django.
- Per fare le API non abbiamo utilizzato ORM ma abbiamo preferito riutilizzare le query già create nel progetto precedente, ovviamente con le opportune modifiche per PostgreSQL e python.

## Running program

- Per far avviare il progetto abbimo scelto di usare dei file `.bat`
- Il primo file si chiama *setup_and_run* e come possiamo capire dal nome serve per fare il setup di postgress e il setup del server, creiamo un ambiente virutale .venv dove installeremo le dependencies di cui ha bisogno il progetto.
- Il secondo file si chiama *run.bat* e avvia solamente il server dopo che è stato creato, cosi da non dover fare il setup ogni volta.
- Il file di setup serve anche se si modifica il file sql del database e quindi rifacendo il setup mi aggiorna il database.
- Ad ogni run di entrambi i file `.bat` la pagina iniziale del sito verra visualizzata sul browser dell'utente
- Per ogni eventuale errore e per capire di cosa ha bisogno il progetto inizialmente(es. postgress ecc) abbiamo creato un manuale per l'utente che consigliamo di visualizzare prima di avviare i file `.bat`.