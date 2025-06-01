# Documentation

- Abbiamo scelto di usare come Database PostgreSQL in quanto per ristrutturare il progetto iniziale ci serviva un database relazionale.
- Principalmente abbiamo usato un ambiente virtuale `.venv/Scripts/activate ` dove abbiamo installato django.
- Abbiamo scelto di usare un approccio modulare, percio abbiamo creato una applicazione museo dove abbiamo i vari *templates* e i file *statici*, in futuro si può ampliare il progetto creando altre app e farle comunicare tra loro o indipendentemente.
- Negli urls.py abbiamo tutti gli url della nostra applicazione museo, questi vengono inclusi nella cartella padre `src/urls`
- In views.py sviluppiamo alcune API che ci servono per fare le varie query a PostgreSQL, queste vengono gestite tramite i file fetch------.js che abbiamo modificato per poter essere compatibili con django.
- Per fare le API non abbiamo utilizzato ORM ma abbiamo preferito riutilizzare le query già create nel progetto precedente, ovviamente con le opportune modifiche per PostgreSQL e python.
