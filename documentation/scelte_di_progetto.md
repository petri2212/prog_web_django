# Documentation

- Abbiamo scelto di usare come Database PostgreSQL in quanto per ristrutturare il progetto iniziale ci serviva un database relazionale.
- Principalmente abbiamo usato un ambiente virtuale `.venv/Scripts/activate ` dove abbiamo installato django.
- Abbiamo scelto di usare un approccio modulare, percio abbiamo scelto di creare una applicazione museo dove abbiamo i dati, in futuro si può ampliare il progetto creando altre app.
- Negli urls.py abbiamo tutti gli url della nostra applicazione museo, questi vengono ereditati dalla cartella padre `src`
- In views.py sviluppiamo alcune API che ci servono per fare le varie query a PostgreSQL, queste vengono gestite tramite i file fetch_{.....}.js che abbiamo modificato per poter essere compatibili con django.
- Per fare le API non abbiamo utilizzato ORM ma abbiamo preferito riutilizzare le query già create nel primo progetto