from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_profissionais, name='lista_profissionais'),
    path('novo/', views.cadastrar_profissional, name='cadastrar_profissional'),
    path('editar/<int:pk>/', views.editar_profissional, name='editar_profissional'),
    path('excluir/<int:pk>/', views.excluir_profissional, name='excluir_profissional'),
]