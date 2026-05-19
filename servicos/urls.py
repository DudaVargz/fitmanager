from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_servicos, name='lista_servicos'),
    path('novo/', views.cadastrar_servico, name='cadastrar_servico'),
    path('editar/<int:pk>/', views.editar_servico, name='editar_servico'),
    path('excluir/<int:pk>/', views.excluir_servico, name='excluir_servico'),
]