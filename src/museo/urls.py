from django.urls import path
from . import views

urlpatterns = [
    path('opere-quadro/', views.tema, name='opere_quadro'),
]
