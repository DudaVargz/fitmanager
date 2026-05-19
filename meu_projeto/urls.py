from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('clientes/', include('clientes.urls')),
    path('profissionais/', include('profissionais.urls')),
    path('servicos/', include('servicos.urls')),
    path('agendamentos/', include('agendamentos.urls')),
    path('', include('agendamentos.urls')),
]