from django.db import models

class Opera(models.Model):
    codice = models.IntegerField(primary_key=True)
    autore = models.IntegerField()
    titolo = models.TextField()
    annoacquisto = models.IntegerField()
    annorealizzazione = models.IntegerField()
    tipo = models.TextField()
    espostainsala = models.IntegerField()

    class Meta:
        db_table = 'opera'   # nome esatto della tabella in PostgreSQL
        managed = False            # Django NON gestisce questa tabella (no migrazioni)


class Tema(models.Model):
    codice = models.IntegerField(primary_key=True)
    descrizione = models.TextField()

    class Meta:
        db_table = 'tema'   # nome esatto della tabella in PostgreSQL
        managed = False            # Django NON gestisce questa tabella (no migrazioni)
