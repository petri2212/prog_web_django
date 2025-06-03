@echo off
setlocal

:: Verifica che il comando "psql" sia disponibile
where psql >nul 2>&1
if errorlevel 1 (
    echo Errore: il comando "psql" non è stato trovato. Assicurati che PostgreSQL sia installato e che "psql" sia nel PATH.
    pause
    exit /b 1
)

:: CONFIGURAZIONE
set DB_NAME=fadein
set DB_USER=postgres
set /p DB_HOST=Host [localhost]:
if "%DB_HOST%"=="" set DB_HOST=localhost
set /p DB_PORT=Porta [5432]:
if "%DB_PORT%"=="" set DB_PORT=5432
set SQL_FILE=..\prog_web_django\db\fadeIn_postgress_final.sql

:: Crea database se non esiste
echo Creazione database %DB_NAME%...
set /p DB_PASSWORD=Inserisci la password per l'utente postgres: 
set PGPASSWORD=%DB_PASSWORD%
psql -U %DB_USER% -h %DB_HOST% -p %DB_PORT% -c "CREATE DATABASE %DB_NAME%;" || echo Il database potrebbe esistere già.


:: Importa dati nel database
echo Importazione dati nel database...
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
python -m venv .venv
call .venv\Scripts\activate.bat

:: Installa dipendenze se necessario
pip install -r requirements.txt

:: Migrazioni Django
echo Applico le migrazioni Django...
python ..\prog_web_django\src\manage.py migrate

:: Avvia il server
echo Avvio del server Django su http://127.0.0.1:8000
cmd /c start "" http://127.0.0.1:8000/museo/autore
python ..\prog_web_django\src\manage.py runserver


pause
