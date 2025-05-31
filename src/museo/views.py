from museo.models import Opera, Tema
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import json
from django.db import connection


def tema(request):
  #  return HttpResponse("Sei in about")
  return render(request, 'tema.html')

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
