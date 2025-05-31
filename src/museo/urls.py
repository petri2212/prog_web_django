from django.urls import path
from . import views

urlpatterns = [
    path('tema/', views.tema, name='museo_tema'),
    path('sala/', views.sala, name='museo_sala'),
    path('autore/', views.autore, name='museo_autore'),
    path('opera/', views.opera, name='museo_opera'),
    path('queries/select_opera/', views.select_opera, name='select_opera'),
    path('queries/select_autore/', views.select_autore, name='select_autore'),
    path('queries/select_tema/', views.select_tema, name='select_tema'),
    path('queries/select_sala/', views.select_sala, name='select_sala'),
]
