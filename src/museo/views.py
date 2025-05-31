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
