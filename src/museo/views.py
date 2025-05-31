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
