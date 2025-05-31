from django.urls import path
from . import views

urlpatterns = [
    path('tema/', views.tema, name='museo_tema'),
    path('sala/', views.sala, name='museo_sala'),
    path('queries/select_tema/', views.select_tema, name='select_tema'),
    path('queries/select_sala/', views.select_sala, name='select_sala'),
]
