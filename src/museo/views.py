from museo.models import Opera
from django.http import HttpResponse

def lista_opere(request):
    opere = Opera.objects.filter(tipo='quadro')
    titoli = ", ".join([opera.titolo for opera in opere])
    return HttpResponse(f"Opere di tipo quadro: {titoli}")
