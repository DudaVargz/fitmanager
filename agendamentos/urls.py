from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('lista/', views.lista_agendamentos, name='lista_agendamentos'),
    path('novo/', views.cadastrar_agendamento, name='cadastrar_agendamento'),
    path('editar/<int:pk>/', views.editar_agendamento, name='editar_agendamento'),
    path('cancelar/<int:pk>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('perfil/', views.perfil, name='perfil'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
]