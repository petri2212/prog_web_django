from museo.models import Opera, Tema
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import json
from django.db import connection

def tema(request):
  return render(request, 'tema.html')

def sala(request):
  return render(request, 'sala.html')

def autore(request):
  return render(request, 'autore.html')

def opera(request):
  return render(request, 'opera.html')

@csrf_exempt
def select_tema(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            codice = data.get('Codice')
            descrizione = data.get('Descrizione')

            with connection.cursor() as cursor:
                query = """
                SELECT tema.codice, tema.descrizione, COUNT(sala.temaSala) AS conteggio
                FROM tema
                LEFT JOIN  sala ON tema.codice = sala.temaSala
                WHERE 1=1
                """
                params = []

                if descrizione:
                    query += " AND tema.descrizione ILIKE %s"
                    params.append(f"%{descrizione}%")
                if codice:
                    query += " AND tema.codice = %s"
                    params.append(codice)

                query += "GROUP BY tema.codice ORDER BY tema.codice ASC "

                cursor.execute(query, params)
                risultati = cursor.fetchall()

            response_data = []
            for codice, descrizione, conteggio in risultati:
                response_data.append({
                    'codice': codice,
                    'descrizione': descrizione,
                    'conteggio': conteggio,
                })

            return JsonResponse(response_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Metodo non consentito'}, status=405)


@csrf_exempt
def select_sala(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            codice = data.get('Codice')
            nome = data.get('Nome')
            superficie = data.get('Superficie')
            tema_s = data.get('Tema_Sala')

            with connection.cursor() as cursor:
                query = """
                SELECT numero, nome, superficie, temaSala, descrizione, COUNT(espostaInSala) AS Quadri_in_sala
                FROM sala
                JOIN  tema ON codice = temaSala JOIN opera ON sala.numero = opera.espostaInSala 
                WHERE 1=1
                """
                params = []

                if tema_s:
                    query += " AND descrizione ILIKE %s"
                    params.append(f"%{tema_s}%")

                if nome:
                    query += " AND nome ILIKE %s"
                    params.append(f"%{nome}%")

                if superficie:
                    query += " AND superficie = %s"
                    params.append(superficie)
                
                if codice:
                    query += " AND numero = %s"
                    params.append(codice)

                query += "GROUP BY numero, tema.descrizione ORDER BY numero ASC "

                cursor.execute(query, params)
                risultati = cursor.fetchall()

            response_data = []
            for numero, nome, superficie, temaSala, descrizione, Quadri_in_sala  in risultati:
                response_data.append({
                    'numero': numero,
                    'nome': nome,
                    'superficie': superficie,
                    'temaSala': temaSala,
                    'descrizione': descrizione,
                    'Quadri_in_sala': Quadri_in_sala,
                })

            return JsonResponse(response_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Metodo non consentito'}, status=405)


@csrf_exempt
def select_autore(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            codice = data.get('Codice')
            nome = data.get('Nome')
            cognome = data.get('Cognome')
            nazione = data.get('Nazione')
            datanascita = data.get('DataNascita')
            tipo = data.get('VivoMorto')
            datamorte = data.get('DataMorte')
           


            with connection.cursor() as cursor:
                query = """
                SELECT autore.codice, nome, cognome, nazione, datanascita, autore.tipo, datamorte, COUNT(opera.codice) AS num_opere
                FROM autore JOIN opera ON autore.codice = opera.autore 
                WHERE 1=1
                """
                params = []

                if cognome:
                    query += " AND cognome ILIKE %s"
                    params.append(f"%{cognome}%")

                if nome:
                    query += " AND nome ILIKE %s"
                    params.append(f"%{nome}%")

                if nazione:
                    query += " AND nazione ILIKE %s"
                    params.append(f"%{nazione}%")

                if codice:
                    query += " AND autore.codice = %s"
                    params.append(codice)

                if datanascita:
                    query += " AND datanascita = %s"
                    params.append(datanascita)
                
                if datamorte:
                    query += " AND datamorte = %s"
                    params.append(datamorte)
                if tipo:
                    query += " AND autore.tipo = %s"
                    params.append(tipo)

                query += "GROUP BY autore.codice ORDER BY autore.codice ASC "

                cursor.execute(query, params)
                risultati = cursor.fetchall()

            response_data = []
            for codice, nome, cognome, nazione, datanascita,tipo,datamorte, num_opere  in risultati:
                response_data.append({
                    'codice': codice,
                    'nome': nome,
                    'cognome': cognome,
                    'nazione': nazione,
                    'dataNascita': datanascita,
                    'tipo': tipo,
                    'dataMorte': datamorte,
                    'num_opere': num_opere,
                   
                })

            return JsonResponse(response_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Metodo non consentito'}, status=405)

@csrf_exempt
def select_opera(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            autore = data.get('Autore')
            nomeAutore = data.get('NomeAutore')
            titolo = data.get('Titolo')
            annoAquisto = data.get('AnnoAquisto')
            annoRealizzazione = data.get('AnnoRealizzazione')
            tipo = data.get('Tipo')
            numeroSala = data.get('NumeroSala')
            nomeSala = data.get('NomeSala')
           


            with connection.cursor() as cursor:
                query = """
                SELECT opera.codice, autore, CONCAT(autore.nome, ' ', autore.cognome) AS full_name, titolo, annoAcquisto, annoRealizzazione, opera.tipo, espostaInSala, sala.nome AS nome_sala 
                FROM opera JOIN sala ON opera.espostaInSala = sala.numero JOIN autore ON opera.autore = autore.codice 
                WHERE 1=1
                """
                params = []
                if autore:
                    query += " AND autore = %s"
                    params.append(autore)

                if nomeAutore:
                    query += " AND CONCAT(autore.nome, ' ', autore.cognome) ILIKE %s"
                    params.append(f"%{nomeAutore}%")

                if titolo:
                    query += " AND titolo ILIKE %s"
                    params.append(f"%{titolo}%")

                if annoAquisto:
                    query += " AND annoaquisto = %s"
                    params.append(annoAquisto)

                if annoRealizzazione:
                    query += " AND annorealizzazione = %s"
                    params.append(annoRealizzazione)
                
                if tipo:
                    query += " AND opera.tipo = %s"
                    params.append(tipo)

                if numeroSala:
                    query += " AND espostainsala = %s"
                    params.append(numeroSala)  

                if nomeSala:
                    query += " AND sala.nome ILIKE %s"
                    params.append(f"%{nomeSala}%")
                query += "GROUP BY opera.codice, full_name, sala.nome  ORDER BY opera.codice ASC "

                cursor.execute(query, params)
                risultati = cursor.fetchall()

            response_data = []
            for codice, autore, full_name, titolo, annoAcquisto,annoRealizzazione,tipo, espostaInSala, nome_sala  in risultati:
                response_data.append({
                    'codice': codice,
                    'autore': autore,
                    'full_name': full_name,
                    'titolo': titolo,
                    'annoAcquisto': annoAcquisto,
                    'annoRealizzazione': annoRealizzazione,
                    'tipo': tipo,
                    'espostaInSala': espostaInSala,
                    'nome_sala': nome_sala,
                   
                })

            return JsonResponse(response_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Metodo non consentito'}, status=405)


@csrf_exempt
def insert_opera(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            Autore = data.get('autoreSelect')
            Titolo = data.get('titoloSelect')
            AnnoAcquisto = data.get('AnnoAquistoSelect')
            AnnoRealizzazione = data.get('AnnoRealizzazioneSelect')
            Tipo = data.get('tipoSelect')
            NomeSala = data.get('NumeroSalaSelect')

            # Estrai ID Autore (prima del trattino)
            idAutore = Autore.split('-')[0].strip() if Autore else None

            with connection.cursor() as cursor:
                # Trova numero sala
                cursor.execute("SELECT numero FROM sala WHERE nome = %s", [NomeSala])
                row = cursor.fetchone()
                if not row:
                    return JsonResponse({'error': 'Sala non trovata'}, status=400)
                NumeroSala = row[0]

                # Trova max codice
                cursor.execute("SELECT MAX(codice) FROM opera")
                row = cursor.fetchone()
                max_codice = (row[0] or 0) + 1

                # Inserisci nuova opera
                insert_query = """
                    INSERT INTO opera (codice, autore, titolo, annoacquisto, annorealizzazione, tipo, espostainsala)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, [
                    max_codice,
                    idAutore,
                    Titolo,
                    AnnoAcquisto,
                    AnnoRealizzazione,
                    Tipo,
                    NumeroSala
                ])

            return JsonResponse({'success': 'Inserimento riuscito!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Metodo non consentito'}, status=405)

@csrf_exempt
def delete_opera(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Opera = data.get('codiceDelete')

            if not Opera:
                return JsonResponse({'error': 'Parametro mancante: codiceDelete'}, status=400)

            # Separazione: "TitoloOpera - Cognome Nome"
            if '-' not in Opera:
                return JsonResponse({'error': 'Formato codiceDelete non valido'}, status=400)

            titolo_autore = Opera.split('-')
            TitoloOpera = titolo_autore[0].strip()
            AutoreOpera = titolo_autore[1].strip()

            parti = AutoreOpera.split()
            if len(parti) < 2:
                return JsonResponse({'error': 'Formato autore non valido'}, status=400)

            cognome = parti[0]
            nome = " ".join(parti[1:])  # supporto nomi composti

            with connection.cursor() as cursor:
                # Ricava ID opera
                select_query = """
                    SELECT opera.codice
                    FROM opera
                    JOIN autore ON autore.codice = opera.autore
                    WHERE opera.titolo = %s AND autore.nome = %s AND autore.cognome = %s
                """
                cursor.execute(select_query, [TitoloOpera, nome, cognome])
                row = cursor.fetchone()

                if not row:
                    return JsonResponse({'error': 'Opera non trovata'}, status=404)

                codice_opera = row[0]

                # Esegui eliminazione
                delete_query = "DELETE FROM opera WHERE codice = %s"
                cursor.execute(delete_query, [codice_opera])

            return JsonResponse({'success': 'Eliminazione dei dati riuscita!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Metodo non consentito'}, status=405)

@csrf_exempt
def update_opera(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            codice_update = data.get('codiceUpdate')
            nome_autore = data.get('autoreUpdate')
            titolo = data.get('titoloUpdate')
            anno_acquisto = data.get('AnnoAquistoUpdate')
            anno_realizzazione = data.get('AnnoRealizzazioneUpdate')
            tipo = data.get('tipoUpdate')
            nome_sala = data.get('NumeroSalaUpdate')

            if not codice_update or '-' not in codice_update:
                return JsonResponse({'error': 'Parametro codiceUpdate mancante o formato errato'}, status=400)

            # Estrazione titolo e autore
            titolo_opera = codice_update.split('-')[0].strip()
            autore_opera = codice_update.split('-')[1].strip()

            parti = autore_opera.split()
            if len(parti) < 2:
                return JsonResponse({'error': 'Formato autore non valido'}, status=400)

            cognome = parti[0]
            nome = " ".join(parti[1:])

            with connection.cursor() as cursor:
                # Ricava codice opera
                cursor.execute("""
                    SELECT opera.codice
                    FROM opera
                    JOIN autore ON autore.codice = opera.autore
                    WHERE opera.titolo = %s AND autore.nome = %s AND autore.cognome = %s
                """, [titolo_opera, nome, cognome])
                row = cursor.fetchone()

                if not row:
                    return JsonResponse({'error': 'Opera non trovata'}, status=404)

                codice_opera = row[0]

                # Ricava id autore
                autore_id = None
                if nome_autore and '-' in nome_autore:
                    autore_id = nome_autore.split('-')[0].strip()

                # Ricava numero sala
                numero_sala = None
                if nome_sala:
                    cursor.execute("SELECT numero FROM sala WHERE nome = %s", [nome_sala])
                    sala_row = cursor.fetchone()
                    if sala_row:
                        numero_sala = sala_row[0]

                # Costruzione della query dinamica
                update_fields = []
                params = []

                if autore_id:
                    update_fields.append("autore = %s")
                    params.append(autore_id)
                if titolo:
                    update_fields.append("titolo = %s")
                    params.append(titolo)
                if anno_acquisto:
                    update_fields.append("annoacquisto = %s")
                    params.append(anno_acquisto)
                if anno_realizzazione:
                    update_fields.append("annorealizzazione = %s")
                    params.append(anno_realizzazione)
                if tipo:
                    update_fields.append("tipo = %s")
                    params.append(tipo)
                if numero_sala:
                    update_fields.append("espostainsala = %s")
                    params.append(numero_sala)

                if not update_fields:
                    return JsonResponse({'error': 'Nessun campo da aggiornare'}, status=400)

                query = f"UPDATE opera SET {', '.join(update_fields)} WHERE codice = %s"
                params.append(codice_opera)

                cursor.execute(query, params)

            return JsonResponse({'success': 'Aggiornamento dei dati riuscito!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Metodo non consentito'}, status=405)