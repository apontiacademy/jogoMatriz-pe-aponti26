from django.urls import path
from . import views

urlpatterns = [
    path("<str:codigo>/", views.painel),
    path("<str:codigo>/entrar/", views.entrar),
    path("<str:codigo>/posicionar/", views.posicionar),
    path("<str:codigo>/estado/", views.estado),
    path("<str:codigo>/atirar/", views.atirar),
]