@echo off
setlocal

:: CONFIGURAZIONE
set DB_NAME=fadein
set DB_USER=postgres
set /p DB_PASSWORD=Inserisci la password per l'utente postgres: 
set /p DB_HOST=Host [localhost]:
if "%DB_HOST%"=="" set DB_HOST=localhost
set /p DB_PORT=Porta [5432]:
if "%DB_PORT%"=="" set DB_PORT=5432
set SQL_FILE=..\prog_web_django\db\fadeIn_postgress_clean1.sql

:: Crea database se non esiste
echo Creazione database %DB_NAME%...
set PGPASSWORD=%DB_PASSWORD%
psql -U %DB_USER% -h %DB_HOST% -p %DB_PORT% -c "CREATE DATABASE %DB_NAME%;" || echo Il database potrebbe esistere già.


:: Importa dati nel database
echo Importazione dati nel database...
set /p DB_PASSWORD=Inserisci la password per l'utente %DB_USER%:
set PGPASSWORD=%DB_PASSWORD%
psql -U %DB_USER% -h %DB_HOST% -p %DB_PORT% -d %DB_NAME% -f %SQL_FILE%

:: Crea il file .env (se non esiste)
echo Creazione del file .env...
(
echo DB_NAME=%DB_NAME%
echo DB_USER=%DB_USER%
echo DB_PASSWORD=%DB_PASSWORD%
echo DB_HOST=%DB_HOST%
echo DB_PORT=%DB_PORT%
) > .env

:: Attiva ambiente virtuale (se usi venv)
echo Attivazione ambiente virtuale...
call venv\Scripts\activate

:: Installa dipendenze se necessario
pip install -r requirements.txt

:: Migrazioni Django
echo Applico le migrazioni Django...
python ..\prog_web_django\src\manage.py migrate

:: Avvia il server
echo Avvio del server Django su http://127.0.0.1:8000
python ..\prog_web_django\src\manage.py runserver

pause
