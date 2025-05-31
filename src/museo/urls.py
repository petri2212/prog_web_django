from django.urls import path
from . import views

urlpatterns = [
    path('tema/', views.tema, name='opere_tema'),
    path('queries/select_tema/', views.select_tema, name='select_tema'),
]
