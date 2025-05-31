from museo.models import Opera, Tema
from django.http import HttpResponse
from django.shortcuts import render

def lista_opere(request):
   # opere = Opera.objects.filter()#tipo='quadro'
   # titoli = ", ".join([opera.titolo for opera in opere])
   # return HttpResponse(f"Opere di tipo quadro: {titoli}")
    opere = Opera.objects.all()  # prendi tutte le opere
    righe = []
    for opera in opere:
        riga = (
            f"codice: {opera.codice}, "
            f"autore: {opera.autore}, "
            f"titolo: {opera.titolo}, "
            f"annoAcquisto: {opera.annoacquisto}, "
            f"annoRealizzazione: {opera.annorealizzazione}, "
            f"tipo: {opera.tipo}, "
            f"espostaInSala: {opera.espostainsala}"
        )
        righe.append(riga)
    # Unisci tutte le righe con un a capo
    risultato = "<br>".join(righe)
    return HttpResponse(risultato)

def temi_sala(request):
   # opere = Opera.objects.filter()#tipo='quadro'
   # titoli = ", ".join([opera.titolo for opera in opere])
   # return HttpResponse(f"Opere di tipo quadro: {titoli}")
    temi = Tema.objects.all()  # prendi tutte le opere
    righe = []
    for tema in temi:
        riga = (
            f"codice: {tema.codice}, "
            f"descrizione: {tema.descrizione}, "
        )
        righe.append(riga)
    # Unisci tutte le righe con un a capo
    risultato = "<br>".join(righe)
    return HttpResponse(risultato)

def tema(request):
  #  return HttpResponse("Sei in about")
  return render(request, 'tema.html')