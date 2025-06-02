@echo off
setlocal

:: Avvia il server
echo Avvio del server Django su http://127.0.0.1:8000
cmd /c start "" http://127.0.0.1:8000/museo/autore
python ..\prog_web_django\src\manage.py runserver

pause