from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('relatorio/<int:ano>/pdf/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
]